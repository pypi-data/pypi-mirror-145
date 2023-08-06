import inspect
import logging
import os.path
from dataclasses import dataclass
from string import Template
from typing import Optional, Dict, List, Union, Type, Any, Tuple

import yaml
from jsonschema import exceptions
from yaml.scanner import ScannerError

from metricflow.errors.errors import ParsingException
from metricflow.model.model_transformer import ModelTransformer
from metricflow.model.objects.common import Version
from metricflow.model.objects.data_source import DataSource
from metricflow.model.objects.materialization import Materialization
from metricflow.model.objects.metric import Metric
from metricflow.model.objects.user_configured_model import UserConfiguredModel
from metricflow.model.objects.utils import ParseableObject, ParseableField
from metricflow.model.parsing.validation import (
    validate_config_structure,
    VERSION_KEY,
    METRIC_TYPE,
    DATA_SOURCE_TYPE,
    MATERIALIZATION_TYPE,
    DOCUMENT_TYPES,
    DERIVED_GROUP_BY_ELEMENT_TYPE,
)
from metricflow.model.parsing.yaml_loader import ParsingContext, SafeLineLoader, PARSING_CONTEXT_KEY
from metricflow.model.validations.validator_helpers import ValidationIssueType

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class YamlFile:  # noqa: D
    file_path: str
    contents: str


@dataclass(frozen=True)
class ModelBuildResult:  # noqa: D
    model: Optional[UserConfiguredModel] = None
    # Issues found in the model.
    issues: Optional[Tuple[ValidationIssueType, ...]] = None


def parse_directory_of_yaml_files_to_model(
    directory: str,
    template_mapping: Optional[Dict[str, str]] = None,
    apply_pre_transformations: Optional[bool] = True,
    apply_post_transformations: Optional[bool] = True,
) -> ModelBuildResult:
    """Parse files in the given directory to a TMdoModel.

    Strings in the file following the Python string template format are replaced according to the template_mapping dict.
    """
    template_mapping = template_mapping or {}
    yaml_config_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if not (file.endswith(".yaml") or file.endswith(".yml")):
                continue
            file_path = os.path.join(root, file)
            with open(file_path) as f:
                contents = Template(f.read()).substitute(template_mapping)
                yaml_config_files.append(
                    YamlFile(file_path=file_path, contents=contents),
                )
    model = parse_yaml_files_to_model(yaml_config_files)

    if apply_pre_transformations:
        model = ModelTransformer.pre_validation_transform_model(model)

    if apply_post_transformations:
        model = ModelTransformer.post_validation_transform_model(model)

    return ModelBuildResult(model=model)


def parse_yaml_files_to_model(files: List[YamlFile]) -> UserConfiguredModel:
    """Builds UserConfiguredModel from list of config files (as strings).

    Persistent storage connection may be passed to write parsed objects=
    to storage and populate object metadata

    Note: this function does not finalize the model
    """
    data_sources = []
    metrics = []
    materializations: List[Materialization] = []
    for config_file in files:
        objects = parse_config_yaml(config_file)  # parse config file
        for obj in objects:
            if isinstance(obj, DataSource):
                data_sources.append(obj)
            elif isinstance(obj, Metric):
                metrics.append(obj)
            elif isinstance(obj, Materialization):
                materializations.append(obj)
            else:
                raise ValueError(
                    f"Unexpected model object parsed from file at path: {config_file.file_path}. "
                    f"Expected internal versions of Metric, DataSource, Materialization, or DerivedGroupByElement"
                )

    return UserConfiguredModel(
        data_sources=data_sources,
        materializations=materializations,
        metrics=metrics,
    )


def parse_config_yaml(
    config_yaml: YamlFile,
) -> List[Union[DataSource, Metric, Materialization]]:
    """Parses transform config file passed as string - Returns list of model objects"""
    results: List[Union[DataSource, Metric, Materialization]] = []
    filename: str = os.path.split(config_yaml.file_path)[-1]
    ctx: Optional[ParsingContext] = None
    errors = []
    try:
        # Validates that config yaml conforms to json schema
        validate_config_structure(config_yaml.contents)

        for config_document in yaml.load_all(config_yaml.contents, Loader=SafeLineLoader):
            # The config document can be None if there is nothing but white space between two `---`
            # this isn't really an issue, so lets just swallow it
            if config_document is None:
                continue
            if not isinstance(config_document, dict):
                errors.append(
                    str(
                        ParsingException(
                            f"Transform object YAML must be a dict. Got `{type(config_document)}`: {config_document}",
                        )
                    )
                )
                continue
            keys = config_document.keys()
            if PARSING_CONTEXT_KEY not in keys:
                raise RuntimeError(f"No parsing ctx present, expected key `{PARSING_CONTEXT_KEY}`. Cannot parse yaml.")

            ctx = config_document.pop(PARSING_CONTEXT_KEY)
            assert ctx
            ctx.filename = filename

            if VERSION_KEY in config_document:
                version = Version.parse(config_document.pop(VERSION_KEY))
                major_version = version.major

                if major_version != 0:
                    raise RuntimeError(f"Unsupported version {version} in config document")

            if len(keys) != 1:
                errors.append(
                    str(
                        ParsingException(
                            f"Transform config document should have one type of key, but this has {len(keys)}. "
                            f"Found keys: {keys} in {config_yaml.file_path}",
                            ctx,
                        )
                    )
                )
                continue

            # retrieve last top-level key as type
            document_type = next(iter(config_document.keys()))
            object_cfg = config_document[document_type]
            if document_type == METRIC_TYPE:
                results.append(parse(Metric, ctx, object_cfg, config_yaml.file_path, config_yaml.contents))
            elif document_type == DATA_SOURCE_TYPE:
                results.append(parse(DataSource, ctx, object_cfg, config_yaml.file_path, config_yaml.contents))
            elif document_type == MATERIALIZATION_TYPE:
                results.append(parse(Materialization, ctx, object_cfg, config_yaml.file_path, config_yaml.contents))
            elif document_type == DERIVED_GROUP_BY_ELEMENT_TYPE:
                logger.warning(f"{DERIVED_GROUP_BY_ELEMENT_TYPE} is not supported in {config_yaml.file_path}")
            else:
                errors.append(
                    str(
                        ParsingException(
                            message=f"Invalid document type: {document_type}. Expected {DOCUMENT_TYPES}",
                            ctx=ctx,
                        )
                    )
                )

        if len(errors) > 0:
            raise ParsingException(message=f"Found {len(errors)} errors parsing configs. Errors: {errors}")
    except exceptions.ValidationError as e:
        logger.exception(f"Config yaml did not conform to metric spec\nError: {e}")
        raise ParsingException(
            message=f"Config yaml did not conform to metric spec\nError: {e}",
            ctx=ctx,
        ) from e
    except ScannerError as e:
        logger.exception(f"Failed parsing invalid yaml.\nParsing context: {ctx}")
        raise ParsingException(message=f"Failed to parse yaml in file. Error: {e}", ctx=ctx) from e
    except Exception as e:
        logger.exception(f"Failed parsing yaml.\nParsing context: {ctx}")
        raise ParsingException(
            message=f"Failed to parse yaml in file. Error: {e}",
            ctx=ctx,
        ) from e

    return results


def parse(  # type: ignore[misc]
    _type: Type[Union[DataSource, Metric, Materialization]],
    ctx: ParsingContext,
    yaml_dict: Dict[str, Any],
    filename: str,
    contents: str,
) -> Any:
    """Parses a model object from (jsonschema-validated) yaml into python object"""

    #  Only - add MdoMetadata
    yaml_dict["metadata"] = {
        "repo_file_path": filename,
        "file_slice": {
            "filename": ctx.filename,
            "content": contents,
            "start_line_number": ctx.start_line,
            "end_line_number": ctx.end_line,
        },
    }

    for field_name, field_value in _type.__fields__.items():
        if field_name in yaml_dict:
            if not inspect.isclass(field_value.type_):  # this handles the nested generic-type case (eg List[List[str]])
                continue
            if issubclass(field_value.type_, ParseableObject):
                if isinstance(yaml_dict[field_name], list):
                    objects = []
                    for obj in yaml_dict[field_name]:
                        objects.append(parse(field_value.type_, ctx, obj, filename, contents))  # type: ignore
                    yaml_dict[field_name] = objects
                else:
                    yaml_dict[field_name] = parse(field_value.type_, ctx, yaml_dict[field_name], filename, contents)  # type: ignore
            elif issubclass(field_value.type_, ParseableField):
                if isinstance(yaml_dict[field_name], list):
                    objects = []
                    for obj in yaml_dict[field_name]:
                        objects.append(field_value.type_.parse(obj))
                    yaml_dict[field_name] = objects
                else:
                    yaml_dict[field_name] = field_value.type_.parse(yaml_dict[field_name])

    return _type(**yaml_dict)
