# flake8: noqa
# There's no way to ignore "F401 '...' imported but unused" warnings in this
# module, but to preserve other warnings. So, don't check this module at all.

import os

import warnings
from typing import Any, Dict, Optional, Union, Tuple, List
from onnxruntime import GraphOptimizationLevel, InferenceSession, SessionOptions

from transformers.configuration_utils import PretrainedConfig
from transformers.feature_extraction_utils import PreTrainedFeatureExtractor
from transformers.file_utils import is_tf_available, is_torch_available
from transformers.models.auto.configuration_auto import AutoConfig
from transformers.models.auto.feature_extraction_auto import FEATURE_EXTRACTOR_MAPPING, AutoFeatureExtractor
from transformers.models.auto.tokenization_auto import TOKENIZER_MAPPING, AutoTokenizer
from transformers.tokenization_utils import PreTrainedTokenizer
from transformers.utils import logging
from transformers.pipelines import get_task, check_task

from transformers import pipeline as default_pipeline

from optimum.onnxruntime import ORTConfig, ORTQuantizer

from transformers.pipelines.base import (
    Pipeline,
    get_default_model,
    infer_framework_load_model,
)

from .feature_extraction import OptimumFeatureExtractionPipeline
from .fill_mask import OptimumFillMaskPipeline

from .question_answering import OptimumQuestionAnsweringPipeline
from .text_classification import OptimumTextClassificationPipeline
from .text_generation import OptimumTextGenerationPipeline
from .token_classification import (
    OptimumTokenClassificationPipeline,
)
from .zero_shot_classification import OptimumZeroShotClassificationPipeline

from .base import (
    _warmup_onnx_graph,
    _forward_onnx,
    create_model_for_providers,
    _create_quantized_graph,
    _export_onnx_graph,
)

if is_tf_available():
    import tensorflow as tf

    from transformers.models.auto.modeling_tf_auto import (
        TFAutoModel,
        TFAutoModelForCausalLM,
        TFAutoModelForMaskedLM,
        TFAutoModelForQuestionAnswering,
        TFAutoModelForSequenceClassification,
        TFAutoModelForTokenClassification,
    )

if is_torch_available():
    import torch

    from transformers.models.auto.modeling_auto import (
        AutoModel,
        AutoModelForCausalLM,
        AutoModelForMaskedLM,
        AutoModelForQuestionAnswering,
        AutoModelForSequenceClassification,
        AutoModelForTokenClassification,
    )

from pathlib import Path

logger = logging.get_logger(__name__)
ONNX_CACHE_DIR = Path(os.path.dirname(__file__)).parent.joinpath("onnx")

# Register all the supported tasks here
TASK_ALIASES = {
    "sentiment-analysis": "text-classification",
    "ner": "token-classification",
}

SUPPORTED_TASKS = {
    "text-classification": {
        "impl": OptimumTextClassificationPipeline,
        "tf": (TFAutoModelForSequenceClassification,) if is_tf_available() else (),
        "pt": (AutoModelForSequenceClassification,) if is_torch_available() else (),
        "default": {
            "model": {
                "pt": "distilbert-base-uncased-finetuned-sst-2-english",
                "tf": "distilbert-base-uncased-finetuned-sst-2-english",
            },
        },
        "type": "text",
        "feature": "sequence-classification",
        "example": {
            "inputs": "My name is Clara and I live in Berkeley, California."
        },
    },
    "feature-extraction": {
        "impl": OptimumFeatureExtractionPipeline,
        "tf": (TFAutoModel,) if is_tf_available() else (),
        "pt": (AutoModel,) if is_torch_available() else (),
        "default": {"model": {"pt": "distilbert-base-cased", "tf": "distilbert-base-cased"}},
        "type": "multimodal",
        "feature": "default",
        "example": {
            "inputs": "Hello, I am Bert from ONNX Transformers."
        },
    },
    "question-answering": {
        "impl": OptimumQuestionAnsweringPipeline,
        "tf": (TFAutoModelForQuestionAnswering,) if is_tf_available() else (),
        "pt": (AutoModelForQuestionAnswering,) if is_torch_available() else (),
        "default": {
            "model": {"pt": "distilbert-base-cased-distilled-squad", "tf": "distilbert-base-cased-distilled-squad"},
        },
        "type": "text",
        "feature": "question-answering",
        "example": {
            "question": "Where was HuggingFace founded ?",
            "context": "HuggingFace was founded in Paris.",
        },
    },
    "token-classification": {
        "impl": OptimumTokenClassificationPipeline,
        "tf": (TFAutoModelForTokenClassification,) if is_tf_available() else (),
        "pt": (AutoModelForTokenClassification,) if is_torch_available() else (),
        "default": {
            "model": {
                "pt": "dbmdz/bert-large-cased-finetuned-conll03-english",
                "tf": "dbmdz/bert-large-cased-finetuned-conll03-english",
            },
        },
        "type": "text",
        "feature": "token-classification",
        "example": {
            "inputs": "My name is Wolfgang and I live in Berlin."
        },
    },
    "zero-shot-classification": {
        "impl": OptimumZeroShotClassificationPipeline,
        "tf": (TFAutoModelForSequenceClassification,) if is_tf_available() else (),
        "pt": (AutoModelForSequenceClassification,) if is_torch_available() else (),
        "default": {
            "model": {"pt": "typeform/distilbert-base-uncased-mnli", "tf": "typeform/distilbert-base-uncased-mnli"},
            "config": {"pt": "typeform/distilbert-base-uncased-mnli", "tf": "typeform/distilbert-base-uncased-mnli"},
            "tokenizer": {"pt": "typeform/distilbert-base-uncased-mnli", "tf": "typeform/distilbert-base-uncased-mnli"},
        },
        "type": "text",
        "feature": "sequence-classification",
        "example": {
            "sequences": "Who are you voting for in 2020?",
            "candidate_labels": ["politics", "public health", "science"],
        },
    },
    "fill-mask": {
        "impl": OptimumFillMaskPipeline,
        "tf": (TFAutoModelForMaskedLM,) if is_tf_available() else (),
        "pt": (AutoModelForMaskedLM,) if is_torch_available() else (),
        "default": {"model": {"pt": "distilroberta-base", "tf": "distilroberta-base"}},
        "type": "text",
        "feature": "masked-lm",
        "example": {
            "inputs": "HuggingFace is creating a <mask> that the community uses to solve NLP tasks."
        },
    },
    "text-generation": {
        "impl": OptimumTextGenerationPipeline,
        "tf": (TFAutoModelForCausalLM,) if is_tf_available() else (),
        "pt": (AutoModelForCausalLM,) if is_torch_available() else (),
        "default": {"model": {"pt": "gpt2", "tf": "gpt2"}},
        "type": "text",
        "feature": "causal-lm",
        "example": {
            "text_inputs": "HuggingFace is creating a tool that the community uses to solve NLP tasks."
        },
    },
}


def get_supported_tasks() -> List[str]:
    """
    Returns a list of supported task strings.
    """
    supported_tasks = list(SUPPORTED_TASKS.keys()) + list(TASK_ALIASES.keys())
    supported_tasks.sort()
    return supported_tasks


def check_task(task: str) -> Tuple[Dict, Any]:
    """
    Checks an incoming task string, to validate it's correct and return the default Pipeline and Model classes, and
    default models if they exist.

    Args:
        task (`str`):
            The task defining which pipeline will be returned. Currently accepted tasks are:

            - `"audio-classification"`
            - `"automatic-speech-recognition"`
            - `"conversational"`
            - `"feature-extraction"`
            - `"fill-mask"`
            - `"image-classification"`
            - `"question-answering"`
            - `"table-question-answering"`
            - `"text2text-generation"`
            - `"text-classification"` (alias `"sentiment-analysis"` available)
            - `"text-generation"`
            - `"token-classification"` (alias `"ner"` available)
            - `"translation"`
            - `"translation_xx_to_yy"`
            - `"summarization"`
            - `"zero-shot-classification"`

    Returns:
        (task_defaults`dict`, task_options: (`tuple`, None)) The actual dictionary required to initialize the pipeline
        and some extra task options for parametrized tasks like "translation_XX_to_YY"


    """
    if task in TASK_ALIASES:
        task = TASK_ALIASES[task]
    if task in SUPPORTED_TASKS:
        targeted_task = SUPPORTED_TASKS[task]
        return targeted_task, None

    if task.startswith("translation"):
        tokens = task.split("_")
        if len(tokens) == 4 and tokens[0] == "translation" and tokens[2] == "to":
            targeted_task = SUPPORTED_TASKS["translation"]
            return targeted_task, (tokens[1], tokens[3])
        raise KeyError(f"Invalid translation task {task}, use 'translation_XX_to_YY' format")

    raise KeyError(f"Unknown task {task}, available tasks are {get_supported_tasks() + ['translation_XX_to_YY']}")


NO_FEATURE_EXTRACTOR_TASKS = set()
NO_TOKENIZER_TASKS = set()
for task, values in SUPPORTED_TASKS.items():
    if values["type"] == "text":
        NO_FEATURE_EXTRACTOR_TASKS.add(task)
    elif values["type"] in {"audio", "image"}:
        NO_TOKENIZER_TASKS.add(task)
    elif values["type"] != "multimodal":
        raise ValueError(f"SUPPORTED_TASK {task} contains invalid type {values['type']}")


def pipeline(
        task: str = None,
        model: Optional = None,
        config: Optional[Union[str, PretrainedConfig]] = None,
        tokenizer: Optional[Union[str, PreTrainedTokenizer]] = None,
        feature_extractor: Optional[Union[str, PreTrainedFeatureExtractor]] = None,
        framework: Optional[str] = None,
        revision: Optional[str] = None,
        use_fast: bool = True,
        use_auth_token: Optional[Union[str, bool]] = None,
        model_kwargs: Dict[str, Any] = None,
        pipeline_class: Optional[Any] = None,
        use_onnx: bool = True,
        optimize: bool = False,
        ort_config: Optional[ORTConfig] = None,
        **kwargs
) -> Pipeline:
    """
    Utility factory method to build a [`Pipeline`].
    Pipelines are made of:
        - A [tokenizer](tokenizer) in charge of mapping raw textual input to token.
        - A [model](model) to make predictions from the inputs.
        - Some (optional) post processing for enhancing model's output.
    Args:
        task (`str`):
            The task defining which pipeline will be returned. Currently accepted tasks are:
            - `"audio-classification"`: will return a [`AudioClassificationPipeline`].
            - `"automatic-speech-recognition"`: will return a [`AutomaticSpeechRecognitionPipeline`].
            - `"conversational"`: will return a [`ConversationalPipeline`].
            - `"feature-extraction"`: will return a [`FeatureExtractionPipeline`].
            - `"fill-mask"`: will return a [`FillMaskPipeline`]:.
            - `"image-classification"`: will return a [`ImageClassificationPipeline`].
            - `"question-answering"`: will return a [`QuestionAnsweringPipeline`].
            - `"table-question-answering"`: will return a [`TableQuestionAnsweringPipeline`].
            - `"text2text-generation"`: will return a [`Text2TextGenerationPipeline`].
            - `"text-classification"` (alias `"sentiment-analysis"` available): will return a
              [`TextClassificationPipeline`].
            - `"text-generation"`: will return a [`TextGenerationPipeline`]:.
            - `"token-classification"` (alias `"ner"` available): will return a [`TokenClassificationPipeline`].
            - `"translation"`: will return a [`TranslationPipeline`].
            - `"translation_xx_to_yy"`: will return a [`TranslationPipeline`].
            - `"summarization"`: will return a [`SummarizationPipeline`].
            - `"zero-shot-classification"`: will return a [`ZeroShotClassificationPipeline`].
        model (`str` or [`PreTrainedModel`] or [`TFPreTrainedModel`], *optional*):
            The model that will be used by the pipeline to make predictions. This can be a model identifier or an
            actual instance of a pretrained model inheriting from [`PreTrainedModel`] (for PyTorch) or
            [`TFPreTrainedModel`] (for TensorFlow).
            If not provided, the default for the `task` will be loaded.
        config (`str` or [`PretrainedConfig`], *optional*):
            The configuration that will be used by the pipeline to instantiate the model. This can be a model
            identifier or an actual pretrained model configuration inheriting from [`PretrainedConfig`].
            If not provided, the default configuration file for the requested model will be used. That means that if
            `model` is given, its default configuration will be used. However, if `model` is not supplied, this
            `task`'s default model's config is used instead.
        tokenizer (`str` or [`PreTrainedTokenizer`], *optional*):
            The tokenizer that will be used by the pipeline to encode data for the model. This can be a model
            identifier or an actual pretrained tokenizer inheriting from [`PreTrainedTokenizer`].
            If not provided, the default tokenizer for the given `model` will be loaded (if it is a string). If `model`
            is not specified or not a string, then the default tokenizer for `config` is loaded (if it is a string).
            However, if `config` is also not given or not a string, then the default tokenizer for the given `task`
            will be loaded.
        feature_extractor (`str` or [`PreTrainedFeatureExtractor`], *optional*):
            The feature extractor that will be used by the pipeline to encode data for the model. This can be a model
            identifier or an actual pretrained feature extractor inheriting from [`PreTrainedFeatureExtractor`].
            Feature extractors are used for non-NLP models, such as Speech or Vision models as well as multi-modal
            models. Multi-modal models will also require a tokenizer to be passed.
            If not provided, the default feature extractor for the given `model` will be loaded (if it is a string). If
            `model` is not specified or not a string, then the default feature extractor for `config` is loaded (if it
            is a string). However, if `config` is also not given or not a string, then the default feature extractor
            for the given `task` will be loaded.
        framework (`str`, *optional*):
            The framework to use, either `"pt"` for PyTorch or `"tf"` for TensorFlow. The specified framework must be
            installed.
            If no framework is specified, will default to the one currently installed. If no framework is specified and
            both frameworks are installed, will default to the framework of the `model`, or to PyTorch if no model is
            provided.
        revision (`str`, *optional*, defaults to `"main"`):
            When passing a task name or a string model identifier: The specific model version to use. It can be a
            branch name, a tag name, or a commit id, since we use a git-based system for storing models and other
            artifacts on huggingface.co, so `revision` can be any identifier allowed by git.
        use_fast (`bool`, *optional*, defaults to `True`):
            Whether or not to use a Fast tokenizer if possible (a [`PreTrainedTokenizerFast`]).
        use_auth_token (`str` or *bool*, *optional*):
            The token to use as HTTP bearer authorization for remote files. If `True`, will use the token generated
            when running `transformers-cli login` (stored in `~/.huggingface`).
        model_kwargs:
            Additional dictionary of keyword arguments passed along to the model's `from_pretrained(...,
            **model_kwargs)` function.
        pipeline_class (`Any`):
            The pipeline that will be used.
            If not provided, the default for the `task` will be loaded.
        use_onnx (`bool`, *optional*, defaults to `True`):
            Whether or not to use ONNX graph instead of Pytorch. ONNX will be loaded from cache if possible. Otherwise,
            graph will be exported.
        optimize (`bool`, *optional*, defaults to `False`):
            Whether or not to optimize ONNX graph. ORTConfig will be used.
        ort_config (`ORTConfig`, *optional*, defaults to `None`):
            ORTConfig will be used to optimize ONNX graph if `optimize` set to `True`.
        kwargs:
            Additional keyword arguments passed along to the specific pipeline init (see the documentation for the
            corresponding pipeline class for possible values).
    Returns:
        [`Pipeline`]: A suitable pipeline for the task.
    Examples:
    ```python
    >>> from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
    >>> # Sentiment analysis pipeline
    >>> pipeline("sentiment-analysis")
    >>> # Question answering pipeline, specifying the checkpoint identifier
    >>> pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="bert-base-cased")
    >>> # Named entity recognition pipeline, passing in a specific model and tokenizer
    >>> model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
    >>> tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    >>> pipeline("ner", model=model, tokenizer=tokenizer)
    ```"""
    if not use_onnx:
        return default_pipeline(task,
                                model,
                                config,
                                tokenizer,
                                feature_extractor,
                                framework,
                                revision,
                                use_fast,
                                use_auth_token,
                                model_kwargs,
                                pipeline_class
                                )

    if ort_config is None:
        ort_config = ORTConfig(quantization_approach="dynamic")

    if model_kwargs is None:
        model_kwargs = {}

    if task is None and model is None:
        raise RuntimeError(
            "Impossible to instantiate a pipeline without either a task or a model"
            "being specified."
            "Please provide a task class or a model"
        )

    if model is None and tokenizer is not None:
        raise RuntimeError(
            "Impossible to instantiate a pipeline with tokenizer specified but not the model "
            "as the provided tokenizer may not be compatible with the default model. "
            "Please provide a PreTrainedModel class or a path/identifier to a pretrained model when providing tokenizer."
        )
    if model is None and feature_extractor is not None:
        raise RuntimeError(
            "Impossible to instantiate a pipeline with feature_extractor specified but not the model "
            "as the provided feature_extractor may not be compatible with the default model. "
            "Please provide a PreTrainedModel class or a path/identifier to a pretrained model when providing feature_extractor."
        )

    if task is None and model is not None:
        if not isinstance(model, str):
            raise RuntimeError(
                "Inferring the task automatically requires to check the hub with a model_id defined as a `str`."
                f"{model} is not a valid model_id."
            )
        task = get_task(model, use_auth_token)

    # Retrieve the task
    targeted_task, task_options = check_task(task)
    if pipeline_class is None:
        pipeline_class = targeted_task["impl"]

    # Use default model/config/tokenizer for the task if no model is provided
    if model is None:
        # At that point framework might still be undetermined
        model = get_default_model(targeted_task, framework, task_options)
        logger.warning(f"No model was supplied, defaulted to {model} (https://huggingface.co/{model})")

    graph_path = ONNX_CACHE_DIR.joinpath(model, "model.onnx")

    # Retrieve use_auth_token and add it to model_kwargs to be used in .from_pretrained
    model_kwargs["use_auth_token"] = model_kwargs.get("use_auth_token", use_auth_token)

    # Config is the primordial information item.
    # Instantiate config if needed
    if isinstance(config, str):
        config = AutoConfig.from_pretrained(config, revision=revision, _from_pipeline=task, **model_kwargs)
    elif config is None and isinstance(model, str):
        config = AutoConfig.from_pretrained(model, revision=revision, _from_pipeline=task, **model_kwargs)

    model_name = model if isinstance(model, str) else None

    # Infer the framework from the model
    # Forced if framework already defined, inferred if it's None
    # Will load the correct model if possible
    model_classes = {"tf": targeted_task["tf"], "pt": targeted_task["pt"]}
    framework, model = infer_framework_load_model(
        model,
        model_classes=model_classes,
        config=config,
        framework=framework,
        revision=revision,
        task=task,
        **model_kwargs,
    )

    model_config = model.config

    load_tokenizer = type(model_config) in TOKENIZER_MAPPING or model_config.tokenizer_class is not None
    load_feature_extractor = type(model_config) in FEATURE_EXTRACTOR_MAPPING or feature_extractor is not None

    if task in NO_TOKENIZER_TASKS:
        # These will never require a tokenizer.
        # the model on the other hand might have a tokenizer, but
        # the files could be missing from the hub, instead of failing
        # on such repos, we just force to not load it.
        load_tokenizer = False
    if task in NO_FEATURE_EXTRACTOR_TASKS:
        load_feature_extractor = False

    if load_tokenizer:
        # Try to infer tokenizer from model or config name (if provided as str)
        if tokenizer is None:
            if isinstance(model_name, str):
                tokenizer = model_name
            elif isinstance(config, str):
                tokenizer = config
            else:
                # Impossible to guess what is the right tokenizer here
                raise Exception(
                    "Impossible to guess which tokenizer to use. "
                    "Please provide a PreTrainedTokenizer class or a path/identifier to a pretrained tokenizer."
                )

        # Instantiate tokenizer if needed
        if isinstance(tokenizer, (str, tuple)):
            if isinstance(tokenizer, tuple):
                # For tuple we have (tokenizer name, {kwargs})
                use_fast = tokenizer[1].pop("use_fast", use_fast)
                tokenizer_identifier = tokenizer[0]
                tokenizer_kwargs = tokenizer[1]
            else:
                tokenizer_identifier = tokenizer
                tokenizer_kwargs = model_kwargs

            tokenizer = AutoTokenizer.from_pretrained(
                tokenizer_identifier, revision=revision, use_fast=use_fast, _from_pipeline=task, **tokenizer_kwargs
            )

    if load_feature_extractor:
        # Try to infer feature extractor from model or config name (if provided as str)
        if feature_extractor is None:
            if isinstance(model_name, str):
                feature_extractor = model_name
            elif isinstance(config, str):
                feature_extractor = config
            else:
                # Impossible to guess what is the right feature_extractor here
                raise Exception(
                    "Impossible to guess which feature extractor to use. "
                    "Please provide a PreTrainedFeatureExtractor class or a path/identifier "
                    "to a pretrained feature extractor."
                )

        # Instantiate feature_extractor if needed
        if isinstance(feature_extractor, (str, tuple)):
            feature_extractor = AutoFeatureExtractor.from_pretrained(
                feature_extractor, revision=revision, _from_pipeline=task, **model_kwargs
            )

            if (
                    feature_extractor._processor_class
                    and feature_extractor._processor_class.endswith("WithLM")
                    and isinstance(model_name, str)
            ):
                try:
                    import kenlm  # to trigger `ImportError` if not installed
                    from pyctcdecode import BeamSearchDecoderCTC

                    if os.path.isdir(model_name) or os.path.isfile(model_name):
                        decoder = BeamSearchDecoderCTC.load_from_dir(model_name)
                    else:
                        language_model_glob = os.path.join(
                            BeamSearchDecoderCTC._LANGUAGE_MODEL_SERIALIZED_DIRECTORY, "*"
                        )
                        alphabet_filename = BeamSearchDecoderCTC._ALPHABET_SERIALIZED_FILENAME
                        allow_regex = [language_model_glob, alphabet_filename]
                        decoder = BeamSearchDecoderCTC.load_from_hf_hub(model_name, allow_regex=allow_regex)

                    kwargs["decoder"] = decoder
                except ImportError as e:
                    logger.warning(
                        f"Could not load the `decoder` for {model_name}. Defaulting to raw CTC. Try to install `pyctcdecode` and `kenlm`: (`pip install pyctcdecode`, `pip install https://github.com/kpu/kenlm/archive/master.zip`): Error: {e}"
                    )

    if task == "translation" and model.config.task_specific_params:
        for key in model.config.task_specific_params:
            if key.startswith("translation"):
                task = key
                warnings.warn(
                    f'"translation" task was used, instead of "translation_XX_to_YY", defaulting to "{task}"',
                    UserWarning,
                )
                break

    if tokenizer is not None:
        kwargs["tokenizer"] = tokenizer

    if feature_extractor is not None:
        kwargs["feature_extractor"] = feature_extractor

    quantizer = ORTQuantizer(ort_config)

    if not graph_path.exists():
        _export_onnx_graph(quantizer, model, graph_path, targeted_task["feature"])

    logger.info(f"Loading onnx graph from {graph_path.as_posix()}")

    framework = "pt"
    if optimize:
        onnx_opt_model_path = graph_path.parent.joinpath(
            f"{graph_path.stem}-opt.onnx")
        quantized_model_path = graph_path.parent.joinpath(
            f"{graph_path.stem}-quantized.onnx")
        if not quantized_model_path.exists() or not onnx_opt_model_path.exists():
            _create_quantized_graph(quantizer, model, graph_path, targeted_task["feature"])
        graph_path = quantized_model_path

    onnx_model = create_model_for_providers(graph_path.as_posix())

    return pipeline_class(
        model=model,
        framework=framework,
        task=task,
        example=targeted_task["example"],
        onnx_model=onnx_model,
        **kwargs
    )
