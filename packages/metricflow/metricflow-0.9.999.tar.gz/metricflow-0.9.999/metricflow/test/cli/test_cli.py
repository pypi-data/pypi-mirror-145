from metricflow.test.fixtures.cli_fixtures import MetricFlowCliRunner
from metricflow.cli.main import (
    get_dimension_values,
    list_dimensions,
    list_materializations,
    list_metrics,
    query,
)


def test_query(cli_runner: MetricFlowCliRunner) -> None:  # noqa: D
    resp = cli_runner.run(query, args=["--metrics", "metric1", "--dimensions", "ds"])

    assert "metric1" in resp.output
    assert resp.exit_code == 0


def test_list_dimensions(cli_runner: MetricFlowCliRunner) -> None:  # noqa: D
    resp = cli_runner.run(list_dimensions, args=["--metric-names", "metric1"])

    assert "dim1" in resp.output
    assert resp.exit_code == 0


def test_list_metrics(cli_runner: MetricFlowCliRunner) -> None:  # noqa: D
    resp = cli_runner.run(list_metrics)

    assert "metric1: dim1, dim2, dim3" in resp.output
    assert resp.exit_code == 0


def test_get_dimension_values(cli_runner: MetricFlowCliRunner) -> None:  # noqa: D
    resp = cli_runner.run(get_dimension_values, args=["--metric-name", "metric1", "--dimension-name", "ds"])

    assert "dim_val1" in resp.output
    assert resp.exit_code == 0


def test_list_materializations(cli_runner: MetricFlowCliRunner) -> None:  # noqa: D
    resp = cli_runner.run(list_materializations)

    assert "materialization: details related to materialization" in resp.output
    assert resp.exit_code == 0
