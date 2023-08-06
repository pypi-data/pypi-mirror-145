import pytest
from _pytest.fixtures import FixtureRequest

from metricflow.dataflow.sql_table import SqlTable
from metricflow.sql.optimizer.rewriting_sub_query_reducer import SqlRewritingSubQueryReducer
from metricflow.sql.sql_exprs import (
    SqlColumnReferenceExpression,
    SqlColumnReference,
    SqlComparisonExpression,
    SqlComparison,
    SqlStringLiteralExpression,
    SqlFunctionExpression,
    SqlFunction,
    SqlStringExpression,
)
from metricflow.sql.sql_plan import (
    SqlSelectStatementNode,
    SqlSelectColumn,
    SqlTableFromClauseNode,
    SqlOrderByDescription,
    SqlJoinDescription,
    SqlJoinType,
)
from metricflow.test.fixtures.setup_fixtures import MetricFlowTestSessionState
from metricflow.test.sql.compare_sql_plan import assert_default_rendered_sql_equal


@pytest.fixture
def base_select_statement() -> SqlSelectStatementNode:
    """SELECT statement used to build test cases.

    -- src3
    SELECT
      SUM(src2.col0) AS bookings
      src2.col1 AS ds
      -- src2
      SELECT
        src1.bookings AS bookings
        , src1.ds AS ds
      FROM (
        -- src1
        SELECT
          1 AS bookings
          , src0.ds AS ds
        FROM demo.fct_bookings src0
        LIMIT 2
      ) src1
      WHERE src1.ds >= "2020-01-01"
      LIMIT 1
    ) src2
    WHERE src2.ds <= "2020-01-05"
    GROUP BY src2.ds
    ORDER BY src2.ds
    """
    return SqlSelectStatementNode(
        description="src3",
        select_columns=(
            SqlSelectColumn(
                expr=SqlFunctionExpression(
                    sql_function=SqlFunction.SUM,
                    sql_function_args=[
                        SqlColumnReferenceExpression(
                            col_ref=SqlColumnReference(table_alias="src2", column_name="bookings")
                        )
                    ],
                ),
                column_alias="bookings",
            ),
            SqlSelectColumn(
                expr=SqlColumnReferenceExpression(col_ref=SqlColumnReference(table_alias="src2", column_name="ds")),
                column_alias="ds",
            ),
        ),
        from_source=SqlSelectStatementNode(
            description="src2",
            select_columns=(
                SqlSelectColumn(
                    expr=SqlColumnReferenceExpression(
                        col_ref=SqlColumnReference(table_alias="src1", column_name="bookings")
                    ),
                    column_alias="bookings",
                ),
                SqlSelectColumn(
                    expr=SqlColumnReferenceExpression(col_ref=SqlColumnReference(table_alias="src1", column_name="ds")),
                    column_alias="ds",
                ),
            ),
            from_source=SqlSelectStatementNode(
                description="src1",
                select_columns=(
                    SqlSelectColumn(
                        expr=SqlColumnReferenceExpression(
                            col_ref=SqlColumnReference(
                                table_alias="src0",
                                column_name="bookings",
                            )
                        ),
                        column_alias="bookings",
                    ),
                    SqlSelectColumn(
                        expr=SqlColumnReferenceExpression(
                            col_ref=SqlColumnReference(
                                table_alias="src0",
                                column_name="ds",
                            )
                        ),
                        column_alias="ds",
                    ),
                ),
                from_source=SqlTableFromClauseNode(sql_table=SqlTable(schema_name="demo", table_name="fct_bookings")),
                from_source_alias="src0",
                joins_descs=(),
                group_bys=(),
                order_bys=(),
                limit=2,
            ),
            from_source_alias="src1",
            joins_descs=(),
            where=SqlComparisonExpression(
                left_expr=SqlColumnReferenceExpression(
                    SqlColumnReference(
                        table_alias="src1",
                        column_name="ds",
                    )
                ),
                comparison=SqlComparison.GREATER_THAN_OR_EQUALS,
                right_expr=SqlStringLiteralExpression("2020-01-01"),
            ),
            group_bys=(),
            order_bys=(),
            limit=1,
        ),
        from_source_alias="src2",
        joins_descs=(),
        group_bys=(
            SqlSelectColumn(
                expr=SqlColumnReferenceExpression(
                    SqlColumnReference(
                        table_alias="src2",
                        column_name="ds",
                    )
                ),
                column_alias="ds",
            ),
        ),
        where=SqlComparisonExpression(
            left_expr=SqlColumnReferenceExpression(
                SqlColumnReference(
                    table_alias="src2",
                    column_name="ds",
                )
            ),
            comparison=SqlComparison.LESS_THAN_OR_EQUALS,
            right_expr=SqlStringLiteralExpression("2020-01-05"),
        ),
        order_bys=(
            SqlOrderByDescription(
                expr=SqlColumnReferenceExpression(
                    SqlColumnReference(
                        table_alias="src2",
                        column_name="ds",
                    )
                ),
                desc=False,
            ),
        ),
        limit=None,
    )


def test_reduce_sub_query(
    request: FixtureRequest,
    mf_test_session_state: MetricFlowTestSessionState,
    base_select_statement: SqlSelectStatementNode,
) -> None:
    """Tests a case where an outer query should be reduced into its inner query with merged LIMIT expressions"""
    assert_default_rendered_sql_equal(
        request=request,
        mf_test_session_state=mf_test_session_state,
        sql_plan_node=base_select_statement,
        plan_id="before_reducing",
    )

    sub_query_reducer = SqlRewritingSubQueryReducer()

    assert_default_rendered_sql_equal(
        request=request,
        mf_test_session_state=mf_test_session_state,
        sql_plan_node=sub_query_reducer.optimize(base_select_statement),
        plan_id="after_reducing",
    )


@pytest.fixture
def join_select_statement() -> SqlSelectStatementNode:
    """SELECT statement with a join used to build test cases.

    SELECT
      SUM(bookings_src.bookings) AS bookings
      listings_src.country_latest AS listing__country_latest
      bookings_src.ds AS ds
    FROM (
      SELECT
        fct_bookings_src.booking AS bookings
        , 1 AS ds
        , fct_bookings_src.listing_id AS listing
      FROM demo.fct_bookings fct_bookings_src
      WHERE fct_bookings_src.ds >= "2020-01-01"
    ) bookings_src
    JOIN (
      SELECT
        dim_listings_src.country_latest AS country_latest
        , dim_listings_src.listing_id AS listing
      FROM demo.dim_listings dim_listings_src
    ) listings_src
    ON bookings_src.listing = listings_src.listing
    GROUP BY bookings_src.ds
    """
    return SqlSelectStatementNode(
        description="query",
        select_columns=(
            SqlSelectColumn(
                expr=SqlFunctionExpression(
                    sql_function=SqlFunction.SUM,
                    sql_function_args=[
                        SqlColumnReferenceExpression(
                            col_ref=SqlColumnReference(table_alias="bookings_src", column_name="bookings")
                        )
                    ],
                ),
                column_alias="bookings",
            ),
            SqlSelectColumn(
                expr=SqlColumnReferenceExpression(
                    col_ref=SqlColumnReference(table_alias="listings_src", column_name="listing__country_latest")
                ),
                column_alias="ds",
            ),
            SqlSelectColumn(
                expr=SqlColumnReferenceExpression(
                    col_ref=SqlColumnReference(table_alias="bookings_src", column_name="ds")
                ),
                column_alias="ds",
            ),
        ),
        from_source=SqlSelectStatementNode(
            description="bookings_src",
            select_columns=(
                SqlSelectColumn(
                    expr=SqlColumnReferenceExpression(
                        col_ref=SqlColumnReference(table_alias="fct_bookings_src", column_name="booking")
                    ),
                    column_alias="bookings",
                ),
                SqlSelectColumn(
                    expr=SqlStringExpression(sql_expr="1", requires_parenthesis=False, used_columns=()),
                    column_alias="ds",
                ),
                SqlSelectColumn(
                    expr=SqlColumnReferenceExpression(
                        col_ref=SqlColumnReference(table_alias="fct_bookings_src", column_name="listing_id")
                    ),
                    column_alias="listing",
                ),
            ),
            from_source=SqlTableFromClauseNode(sql_table=SqlTable(schema_name="demo", table_name="fct_bookings")),
            from_source_alias="fct_bookings_src",
            joins_descs=(),
            where=None,
            group_bys=(),
            order_bys=(),
            limit=None,
        ),
        from_source_alias="bookings_src",
        joins_descs=(
            SqlJoinDescription(
                right_source=SqlSelectStatementNode(
                    description="listings_src",
                    select_columns=(
                        SqlSelectColumn(
                            expr=SqlColumnReferenceExpression(
                                col_ref=SqlColumnReference(table_alias="dim_listings_src", column_name="country")
                            ),
                            column_alias="country_latest",
                        ),
                        SqlSelectColumn(
                            expr=SqlColumnReferenceExpression(
                                col_ref=SqlColumnReference(table_alias="dim_listings_src", column_name="listing_id")
                            ),
                            column_alias="listing",
                        ),
                    ),
                    from_source=SqlTableFromClauseNode(
                        sql_table=SqlTable(schema_name="demo", table_name="dim_listings")
                    ),
                    from_source_alias="dim_listings_src",
                    joins_descs=(),
                    where=None,
                    group_bys=(),
                    order_bys=(),
                    limit=None,
                ),
                right_source_alias="listings_src",
                on_condition=SqlComparisonExpression(
                    left_expr=SqlColumnReferenceExpression(
                        SqlColumnReference(table_alias="bookings_src", column_name="listing"),
                    ),
                    comparison=SqlComparison.EQUALS,
                    right_expr=SqlColumnReferenceExpression(
                        SqlColumnReference(table_alias="listings_src", column_name="listing"),
                    ),
                ),
                join_type=SqlJoinType.LEFT_OUTER,
            ),
        ),
        group_bys=(
            SqlSelectColumn(
                expr=SqlColumnReferenceExpression(
                    SqlColumnReference(
                        table_alias="bookings_src",
                        column_name="ds",
                    )
                ),
                column_alias="ds",
            ),
        ),
        where=SqlComparisonExpression(
            left_expr=SqlColumnReferenceExpression(
                SqlColumnReference(
                    table_alias="bookings_src",
                    column_name="ds",
                )
            ),
            comparison=SqlComparison.LESS_THAN_OR_EQUALS,
            right_expr=SqlStringLiteralExpression("2020-01-05"),
        ),
        order_bys=(),
        limit=None,
    )


def test_reduce_join(
    request: FixtureRequest,
    mf_test_session_state: MetricFlowTestSessionState,
    join_select_statement: SqlSelectStatementNode,
) -> None:
    """Tests a case where reducing occurs on a JOIN"""
    assert_default_rendered_sql_equal(
        request=request,
        mf_test_session_state=mf_test_session_state,
        sql_plan_node=join_select_statement,
        plan_id="before_reducing",
    )

    sub_query_reducer = SqlRewritingSubQueryReducer()

    assert_default_rendered_sql_equal(
        request=request,
        mf_test_session_state=mf_test_session_state,
        sql_plan_node=sub_query_reducer.optimize(join_select_statement),
        plan_id="after_reducing",
    )


@pytest.fixture
def colliding_select_statement() -> SqlSelectStatementNode:
    """SELECT statement that would cause a collision of table aliases if reduced.

    SELECT
      SUM(bookings_src.bookings) AS bookings
      listings_src.country_latest AS listing__country_latest
      bookings_src.ds AS ds
    FROM (
      SELECT
        colliding_alias.booking AS bookings
        , colliding_alias.ds AS ds
        , colliding_alias.listing_id AS listing
      FROM demo.fct_bookings colliding_alias
      WHERE fct_bookings_src.ds >= "2020-01-01"
    ) bookings_src
    JOIN (
      SELECT
        colliding_alias.country_latest AS country_latest
        , colliding_alias.listing_id AS listing
      FROM demo.dim_listings colliding_alias
    ) listings_src
    ON bookings_src.listing = listings_src.listing
    GROUP BY bookings_src.ds
    """
    return SqlSelectStatementNode(
        description="query",
        select_columns=(
            SqlSelectColumn(
                expr=SqlFunctionExpression(
                    sql_function=SqlFunction.SUM,
                    sql_function_args=[
                        SqlColumnReferenceExpression(
                            col_ref=SqlColumnReference(table_alias="bookings_src", column_name="bookings")
                        )
                    ],
                ),
                column_alias="bookings",
            ),
            SqlSelectColumn(
                expr=SqlColumnReferenceExpression(
                    col_ref=SqlColumnReference(table_alias="listings_src", column_name="listing__country_latest")
                ),
                column_alias="ds",
            ),
            SqlSelectColumn(
                expr=SqlColumnReferenceExpression(
                    col_ref=SqlColumnReference(table_alias="bookings_src", column_name="ds")
                ),
                column_alias="ds",
            ),
        ),
        from_source=SqlSelectStatementNode(
            description="bookings_src",
            select_columns=(
                SqlSelectColumn(
                    expr=SqlColumnReferenceExpression(
                        col_ref=SqlColumnReference(table_alias="colliding_alias", column_name="booking")
                    ),
                    column_alias="bookings",
                ),
                SqlSelectColumn(
                    expr=SqlColumnReferenceExpression(
                        col_ref=SqlColumnReference(table_alias="colliding_alias", column_name="ds")
                    ),
                    column_alias="ds",
                ),
                SqlSelectColumn(
                    expr=SqlColumnReferenceExpression(
                        col_ref=SqlColumnReference(table_alias="colliding_alias", column_name="listing_id")
                    ),
                    column_alias="listing",
                ),
            ),
            from_source=SqlTableFromClauseNode(sql_table=SqlTable(schema_name="demo", table_name="fct_bookings")),
            from_source_alias="colliding_alias",
            joins_descs=(),
            where=None,
            group_bys=(),
            order_bys=(),
            limit=None,
        ),
        from_source_alias="bookings_src",
        joins_descs=(
            SqlJoinDescription(
                right_source=SqlSelectStatementNode(
                    description="listings_src",
                    select_columns=(
                        SqlSelectColumn(
                            expr=SqlColumnReferenceExpression(
                                col_ref=SqlColumnReference(table_alias="colliding_alias", column_name="country")
                            ),
                            column_alias="country_latest",
                        ),
                        SqlSelectColumn(
                            expr=SqlColumnReferenceExpression(
                                col_ref=SqlColumnReference(table_alias="colliding_alias", column_name="listing_id")
                            ),
                            column_alias="listing",
                        ),
                    ),
                    from_source=SqlTableFromClauseNode(
                        sql_table=SqlTable(schema_name="demo", table_name="dim_listings")
                    ),
                    from_source_alias="colliding_alias",
                    joins_descs=(),
                    where=None,
                    group_bys=(),
                    order_bys=(),
                    limit=None,
                ),
                right_source_alias="listings_src",
                on_condition=SqlComparisonExpression(
                    left_expr=SqlColumnReferenceExpression(
                        SqlColumnReference(table_alias="bookings_src", column_name="listing"),
                    ),
                    comparison=SqlComparison.EQUALS,
                    right_expr=SqlColumnReferenceExpression(
                        SqlColumnReference(table_alias="listings_src", column_name="listing"),
                    ),
                ),
                join_type=SqlJoinType.LEFT_OUTER,
            ),
        ),
        group_bys=(
            SqlSelectColumn(
                expr=SqlColumnReferenceExpression(
                    SqlColumnReference(
                        table_alias="bookings_src",
                        column_name="ds",
                    )
                ),
                column_alias="ds",
            ),
        ),
        where=SqlComparisonExpression(
            left_expr=SqlColumnReferenceExpression(
                SqlColumnReference(
                    table_alias="bookings_src",
                    column_name="ds",
                )
            ),
            comparison=SqlComparison.LESS_THAN_OR_EQUALS,
            right_expr=SqlStringLiteralExpression("2020-01-05"),
        ),
        order_bys=(),
        limit=None,
    )


def test_colliding_alias(
    request: FixtureRequest,
    mf_test_session_state: MetricFlowTestSessionState,
    colliding_select_statement: SqlSelectStatementNode,
) -> None:
    """Tests a case where reducing occurs on a JOIN"""
    assert_default_rendered_sql_equal(
        request=request,
        mf_test_session_state=mf_test_session_state,
        sql_plan_node=colliding_select_statement,
        plan_id="before_reducing",
    )

    sub_query_reducer = SqlRewritingSubQueryReducer()

    assert_default_rendered_sql_equal(
        request=request,
        mf_test_session_state=mf_test_session_state,
        sql_plan_node=sub_query_reducer.optimize(colliding_select_statement),
        plan_id="after_reducing",
    )
