import logging
import os
import pathlib
import yaml

from typing import Dict, Optional

from metricflow.cli.constants import (
    CONFIG_DWH_DB,
    CONFIG_DWH_DIALECT,
    CONFIG_DWH_HOST,
    CONFIG_DWH_PASSWORD,
    CONFIG_DWH_PORT,
    CONFIG_DWH_SCHEMA,
    CONFIG_DWH_USER,
    CONFIG_DWH_WAREHOUSE,
    CONFIG_MODEL_PATH,
    CONFIG_PATH_KEY,
)
from metricflow.cli.exceptions import SqlClientException, MetricFlowInitException, ModelCreationException
from metricflow.cli.utils import ServerTimeSource
from metricflow.engine.metricflow_engine import MetricFlowEngine
from metricflow.model.parsing.dir_to_model import parse_directory_of_yaml_files_to_model
from metricflow.model.semantic_model import SemanticModel
from metricflow.plan_conversion.column_resolver import DefaultColumnAssociationResolver
from metricflow.plan_conversion.time_spine import TimeSpineSource
from metricflow.protocols.sql_client import SqlClient, SupportedSqlEngine
from metricflow.sql_clients.common_client import not_empty
from metricflow.sql_clients.big_query import BigQuerySqlClient
from metricflow.sql_clients.redshift import RedshiftSqlClient
from metricflow.sql_clients.snowflake import SnowflakeSqlClient


# Avoid logs from being outputted to stdout
logging.getLogger("metricflow").setLevel(logging.CRITICAL)


class CLIContext:
    """Context for MetricFlow CLI."""

    def __init__(self) -> None:  # noqa: D
        self.verbose = False
        self._mf: Optional[MetricFlowEngine] = None
        self._sql_client: Optional[SqlClient] = None
        self._semantic_model: Optional[SemanticModel] = None
        self._mf_system_schema: Optional[str] = None
        self.config = ConfigHandler()

    @property
    def mf_system_schema(self) -> str:  # noqa: D
        if self._mf_system_schema is None:
            self._mf_system_schema = self.config._get_config_value(CONFIG_DWH_SCHEMA)
        assert self._mf_system_schema
        return self._mf_system_schema

    def __initialize_sql_client(self) -> None:
        """Initializes the SqlClient given the credentials."""
        try:
            dialect = self.config._get_config_value(CONFIG_DWH_DIALECT).upper()

            if dialect == SupportedSqlEngine.BIGQUERY.name:
                path_to_creds = not_empty(self.config._get_config_value(CONFIG_DWH_PASSWORD), "password", "config")
                if not pathlib.Path(path_to_creds).exists:
                    raise ValueError(f"`{path_to_creds}` does not contain the BigQuery credential file.")
                with open(path_to_creds, "r") as cred_file:
                    creds = cred_file.readline()
                self._sql_client = BigQuerySqlClient(password=creds)
            elif dialect == SupportedSqlEngine.SNOWFLAKE.name:
                host = not_empty(self.config._get_config_value(CONFIG_DWH_HOST), "host", "config")
                user = not_empty(self.config._get_config_value(CONFIG_DWH_USER), "user", "config")
                password = self.config._get_config_value(CONFIG_DWH_PASSWORD)
                database = not_empty(self.config._get_config_value(CONFIG_DWH_DB), "database", "config")
                warehouse = not_empty(self.config._get_config_value(CONFIG_DWH_WAREHOUSE), "warehouse", "config")
                self._sql_client = SnowflakeSqlClient(
                    host=host,
                    username=user,
                    password=password,
                    database=database,
                    url_query_params={"warehouse": warehouse},
                )
            elif dialect == SupportedSqlEngine.REDSHIFT.name:
                host = not_empty(self.config._get_config_value(CONFIG_DWH_HOST), "host", "config")
                port = int(self.config._get_config_value(CONFIG_DWH_PORT))
                user = not_empty(self.config._get_config_value(CONFIG_DWH_USER), "user", "config")
                password = self.config._get_config_value(CONFIG_DWH_PASSWORD)
                database = not_empty(self.config._get_config_value(CONFIG_DWH_DB), "database", "config")
                self._sql_client = RedshiftSqlClient(
                    host=host,
                    port=port,
                    username=user,
                    password=password,
                    database=database,
                )
            else:
                raise ValueError(f"Invalid dialect `{dialect}`, must be one of `bigquery`, `snowflake`, `redshift`")
        except Exception as e:
            raise SqlClientException from e

    @property
    def sql_client(self) -> SqlClient:  # noqa: D
        if self._sql_client is None:
            # Initialize the SqlClient if not set
            self.__initialize_sql_client()
        assert self._sql_client is not None
        return self._sql_client

    def run_health_checks(self) -> Dict[str, Dict[str, str]]:
        """Execute the DB health checks."""
        try:
            return self.sql_client.health_checks(self.mf_system_schema)
        except Exception:
            raise SqlClientException

    def _initialize_metricflow_engine(self) -> None:
        """Initialize the MetricFlowEngine."""
        try:
            self._mf = MetricFlowEngine(
                semantic_model=self.semantic_model,
                sql_client=self.sql_client,
                column_association_resolver=DefaultColumnAssociationResolver(self.semantic_model),
                time_source=ServerTimeSource(),
                time_spine_source=TimeSpineSource(self.sql_client, schema_name=self.mf_system_schema),
                system_schema=self.mf_system_schema,
            )
        except Exception as e:
            raise MetricFlowInitException from e

    @property
    def mf(self) -> MetricFlowEngine:  # noqa: D
        if self._mf is None:
            self._initialize_metricflow_engine()
        assert self._mf is not None
        return self._mf

    def _build_semantic_model(self) -> None:
        """Get the path to the models and create a corresponding SemanticModel."""
        path_to_models = self.config._get_config_value(CONFIG_MODEL_PATH)
        try:
            model = parse_directory_of_yaml_files_to_model(path_to_models).model
            assert model is not None
        except Exception as e:
            raise ModelCreationException from e
        self._semantic_model = SemanticModel(model)

    @property
    def semantic_model(self) -> SemanticModel:  # noqa: D
        if self._semantic_model is None:
            self._build_semantic_model()
        assert self._semantic_model is not None
        return self._semantic_model


class ConfigHandler:
    """Class to handle all config file retrieval/insertion actions."""

    def __init__(self) -> None:  # noqa: D
        # Create config directory if not exist
        if not os.path.exists(self.dir_path):
            dir_path = pathlib.Path(self.dir_path)
            dir_path.mkdir(parents=True)

    @property
    def dir_path(self) -> str:
        """Retrieve MetricFlow config directory from $MF_CONFIG_DIR, default config dir is ~/.metricflow"""
        config_dir_env = os.getenv(CONFIG_PATH_KEY)
        return config_dir_env if config_dir_env else f"{str(pathlib.Path.home())}/.metricflow"

    @property
    def file_path(self) -> str:
        """Config file can be found at <config_dir>/config.yml"""
        return os.path.join(self.dir_path, "config.yml")

    def _get_config_value(self, key: str) -> str:
        """Attempt to get a corresponding value from the config file. Throw an error if not exists or None."""
        config_file = open(self.file_path, "r")

        config = yaml.load(config_file, Loader=yaml.Loader)
        if key not in config:
            raise KeyError(f"{key} is missing in the configuration file.")

        value = config[key]
        if value is None:
            raise ValueError(f"value for {key} cannot be None.")
        return value
