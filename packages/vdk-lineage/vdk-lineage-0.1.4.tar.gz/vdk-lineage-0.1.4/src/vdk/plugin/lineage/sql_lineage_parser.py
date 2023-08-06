# Copyright 2021 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import logging
from typing import Optional

from sqllineage.core.models import Table
from sqllineage.runner import LineageRunner
from vdk.api.lineage.sql.data import LineageData
from vdk.api.lineage.sql.data import LineageTable

log = logging.getLogger(__name__)


def get_table_lineage_from_query(
    query: str, schema: Optional[str], catalog: Optional[str]
) -> LineageData:
    """
    This method parses the sql query. If and only if it is a rename table query,
    the method returns the names of the source and destination table.
    :param query: The SQL query potentially containing a RENAME TABLE operation
    :param schema: The schema which is queried
    :param catalog: The catalog which is queried
    :return: A tuple with (table_from, table_to) if it is a RENAME TABLE query, None otherwise.
    """
    runner = LineageRunner(query)

    if len(runner.statements_parsed) == 0:
        # log.debug("No statement passed")
        return None

    if len(runner.statements_parsed) > 1:
        raise RuntimeError(
            "Query with more than one statement is passed. "
            "Make sure that multiple query statements (separated) are not passed to this method."
            f"Query passed is '{query}' "
        )

    input_tables = [
        _lineage_table_from_name(source_table, schema, catalog)
        for source_table in runner.source_tables
    ]
    output_table = None
    if len(runner.target_tables) == 1:
        output_table = _lineage_table_from_name(
            runner.target_tables[0], schema, catalog
        )
    elif len(runner.target_tables) > 1:
        raise RuntimeError(
            "Query with more than one target table should not be possible. "
            "Make sure that multiple queries (separated) are not passed accidentally."
            f"Query is '{query}' "
        )

    return LineageData(
        query=query,
        query_type=runner.statements_parsed[0].get_type(),
        query_status="",
        input_tables=input_tables,
        output_table=output_table,
    )


def _lineage_table_from_name(table: Table, schema: str, catalog: str) -> LineageTable:
    tokens = []
    if table.schema:
        tokens = table.schema.raw_name.split(".")

    if len(tokens) == 0:
        return LineageTable(catalog, schema, table.raw_name)
    elif len(tokens) == 1:
        return LineageTable(catalog, tokens[0], table.raw_name)
    elif len(tokens) == 2:
        return LineageTable(tokens[0], tokens[1], table.raw_name)
    else:
        return None
