import pandas as pd
import os
from string import Template
from typing import Dict

from metricflow.dataflow.sql_table import SqlTable
from metricflow.protocols.sql_client import SqlClient
from metricflow.sql_clients.sql_utils import make_df


COUNTRIES = [("US", "NA"), ("MX", "NA"), ("CA", "NA"), ("BR", "SA"), ("GR", "EU"), ("FR", "EU")]
TRANSACTION_TYPE = ["cancellation", "alteration", "quick-buy", "buy"]

CUSTOMERS_TABLE = "mf_demo_customers"
TRANSACTIONS_TABLE = "mf_demo_transactions"
COUNTRIES_TABLE = "mf_demo_countries"

TRANSACTIONS_YAML_FILE = os.path.join(os.path.dirname(__file__), "sample_models/transactions.yaml")
CUSTOMERS_YAML_FILE = os.path.join(os.path.dirname(__file__), "sample_models/customers.yaml")
COUNTRIES_YAML_FILE = os.path.join(os.path.dirname(__file__), "sample_models/countries.yaml")


def build_dataframe(sql_client: SqlClient) -> Dict[str, pd.DataFrame]:
    """Builds random data with some logic.

    Args:
        sql_client: SqlClient used to format the dataframe

    Returns:
        A dict containing {table_name: dataframe of data}
    """
    transaction_data = [
        ("s59936437", "o1005", "c500003", 497.23, "quick-buy", "2022-03-12"),
        ("s59936438", "o1006", "c500000", 73.03, "quick-buy", "2022-04-04"),
        ("s59936439", "o1005", "c500002", 183.15, "alteration", "2022-03-17"),
        ("s59936440", "o1005", "c500003", 460.31, "cancellation", "2022-03-17"),
        ("s59936441", "o1005", "c500003", 331.47, "buy", "2022-03-21"),
        ("s59936442", "o1003", "c500001", 91.35, "alteration", "2022-03-30"),
        ("s59936443", "o1006", "c500001", 5.96, "quick-buy", "2022-03-08"),
        ("s59936444", "o1001", "c500001", 412.35, "cancellation", "2022-03-06"),
        ("s59936445", "o1009", "c500000", 343.14, "buy", "2022-03-21"),
        ("s59936446", "o1009", "c500001", 207.55, "alteration", "2022-03-13"),
        ("s59936447", "o1009", "c500002", 326.52, "buy", "2022-03-28"),
        ("s59936448", "o1006", "c500003", 449.6, "quick-buy", "2022-03-25"),
        ("s59936449", "o1004", "c500003", 416.47, "quick-buy", "2022-03-27"),
        ("s59936450", "o1006", "c500001", 495.58, "buy", "2022-03-25"),
        ("s59936451", "o1003", "c500000", 86.87, "quick-buy", "2022-03-17"),
        ("s59936452", "o1009", "c500003", 284.51, "alteration", "2022-03-08"),
        ("s59936453", "o1007", "c500000", 304.44, "alteration", "2022-04-03"),
        ("s59936454", "o1003", "c500003", 375.79, "cancellation", "2022-03-19"),
        ("s59936455", "o1003", "c500001", 425.3, "quick-buy", "2022-03-18"),
        ("s59936456", "o1010", "c500001", 228.79, "alteration", "2022-03-24"),
        ("s59936457", "o1006", "c500001", 177.31, "alteration", "2022-03-22"),
        ("s59936458", "o1010", "c500002", 134.38, "alteration", "2022-03-20"),
        ("s59936459", "o1010", "c500001", 429.93, "alteration", "2022-03-31"),
        ("s59936460", "o1008", "c500003", 403.52, "quick-buy", "2022-03-13"),
        ("s59936461", "o1006", "c500003", 199.05, "alteration", "2022-03-23"),
        ("s59936462", "o1005", "c500000", 32.01, "buy", "2022-04-04"),
        ("s59936463", "o1004", "c500000", 193.74, "cancellation", "2022-03-13"),
        ("s59936464", "o1007", "c500003", 98.54, "buy", "2022-03-24"),
        ("s59936465", "o1001", "c500001", 369.47, "cancellation", "2022-03-17"),
        ("s59936466", "o1007", "c500002", 259.75, "cancellation", "2022-04-04"),
        ("s59936467", "o1002", "c500000", 401.01, "quick-buy", "2022-03-18"),
        ("s59936468", "o1007", "c500001", 158.19, "cancellation", "2022-04-01"),
        ("s59936469", "o1006", "c500000", 9.7, "cancellation", "2022-03-20"),
        ("s59936470", "o1004", "c500002", 65.76, "buy", "2022-04-03"),
        ("s59936471", "o1006", "c500002", 487.92, "alteration", "2022-03-11"),
        ("s59936472", "o1009", "c500002", 32.83, "cancellation", "2022-03-28"),
        ("s59936473", "o1003", "c500000", 117.37, "quick-buy", "2022-03-15"),
        ("s59936474", "o1003", "c500002", 224.41, "alteration", "2022-04-01"),
        ("s59936475", "o1003", "c500003", 347.77, "quick-buy", "2022-04-03"),
        ("s59936476", "o1001", "c500002", 232.42, "quick-buy", "2022-03-09"),
        ("s59936477", "o1002", "c500003", 88.93, "alteration", "2022-03-14"),
        ("s59936478", "o1003", "c500003", 443.22, "buy", "2022-03-18"),
        ("s59936479", "o1008", "c500003", 129.91, "quick-buy", "2022-03-24"),
        ("s59936480", "o1007", "c500003", 59.2, "buy", "2022-03-13"),
        ("s59936481", "o1004", "c500000", 25.92, "quick-buy", "2022-03-08"),
        ("s59936482", "o1006", "c500000", 319.83, "cancellation", "2022-03-18"),
        ("s59936483", "o1002", "c500003", 95.07, "alteration", "2022-03-15"),
        ("s59936484", "o1006", "c500002", 366.55, "buy", "2022-03-10"),
        ("s59936485", "o1006", "c500000", 224.35, "alteration", "2022-03-28"),
        ("s59936486", "o1000", "c500000", 163.59, "alteration", "2022-04-02"),
    ]

    customer_data = [
        ("c500003", "FR", "2022-04-30"),
        ("c500000", "GR", "2022-04-23"),
        ("c500002", "MX", "2022-06-01"),
        ("c500001", "GR", "2022-05-21"),
    ]
    return {
        CUSTOMERS_TABLE: make_df(
            sql_client=sql_client, columns=["id_customer", "country", "ds"], time_columns={"ds"}, data=customer_data
        ),
        TRANSACTIONS_TABLE: make_df(
            sql_client=sql_client,
            columns=[
                "id_transaction",
                "id_order",
                "id_customer",
                "transaction_amount_usd",
                "transaction_type_name",
                "ds",
            ],
            time_columns={"ds"},
            data=transaction_data,
        ),
        COUNTRIES_TABLE: make_df(sql_client=sql_client, columns=["country", "region"], data=COUNTRIES),
    }


def create_sample_data(sql_client: SqlClient, system_schema: str) -> bool:
    """Create tables with sample data into data warehouse."""

    if any(
        [
            sql_client.table_exists(SqlTable.from_string(f"{system_schema}.{CUSTOMERS_TABLE}")),
            sql_client.table_exists(SqlTable.from_string(f"{system_schema}.{TRANSACTIONS_TABLE}")),
            sql_client.table_exists(SqlTable.from_string(f"{system_schema}.{COUNTRIES_TABLE}")),
        ]
    ):
        # Do not create sample data if any of the table exists
        return False

    dummy_data = build_dataframe(sql_client)
    for table_name in dummy_data:
        sql_table = SqlTable.from_string(f"{system_schema}.{table_name}")
        sql_client.create_table_from_dataframe(sql_table=sql_table, df=dummy_data[table_name])
    return True


def remove_sample_tables(sql_client: SqlClient, system_schema: str) -> None:
    """Drop sample tables."""
    sql_client.drop_table(SqlTable.from_string(f"{system_schema}.{CUSTOMERS_TABLE}"))
    sql_client.drop_table(SqlTable.from_string(f"{system_schema}.{TRANSACTIONS_TABLE}"))
    sql_client.drop_table(SqlTable.from_string(f"{system_schema}.{COUNTRIES_TABLE}"))


def gen_sample_model_configs(dir_path: str, system_schema: str) -> None:
    """Generates the sample model configs to a specified directory."""

    with open(CUSTOMERS_YAML_FILE) as f:
        contents = Template(f.read()).substitute({"customers_table": f"{system_schema}.{CUSTOMERS_TABLE}"})
    with open(f"{dir_path}/{CUSTOMERS_TABLE}.yaml", "w") as file:
        file.write(contents)

    with open(TRANSACTIONS_YAML_FILE) as f:
        contents = Template(f.read()).substitute({"transactions_table": f"{system_schema}.{TRANSACTIONS_TABLE}"})
    with open(f"{dir_path}/{TRANSACTIONS_TABLE}.yaml", "w") as file:
        file.write(contents)

    with open(COUNTRIES_YAML_FILE) as f:
        contents = Template(f.read()).substitute({"countries_table": f"{system_schema}.{COUNTRIES_TABLE}"})
    with open(f"{dir_path}/{COUNTRIES_TABLE}.yaml", "w") as file:
        file.write(contents)
