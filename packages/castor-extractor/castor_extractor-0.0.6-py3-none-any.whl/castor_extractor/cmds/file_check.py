import logging
from argparse import ArgumentParser
from typing import Set

from castor_extractor.file_checker import (
    FileCheckerRun,
    FileTemplate,
    GenericWarehouseFileTemplate,
)
from castor_extractor.utils import LocalStorage

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


Ids = Set[str]
_ID_KEY = "id"


def process(directory: str, verbose: bool):
    """
    Checks all files necessary to push Generic Warehouse
    """
    storage = LocalStorage(directory=directory, with_timestamp=False)

    def _check(
        file_name: str,
        template: FileTemplate,
        *,
        with_ids: bool = True,
    ) -> Ids:
        content = storage.get(file_name)
        checker = FileCheckerRun(content, template, file_name, verbose)
        checker.validate()
        if not with_ids:
            return set()
        return checker.occurrences(_ID_KEY)

    database_template = GenericWarehouseFileTemplate.database()
    database_ids = _check("database", database_template)

    schema_template = GenericWarehouseFileTemplate.schema(database_ids)
    schema_ids = _check("schema", schema_template)

    table_template = GenericWarehouseFileTemplate.table(schema_ids)
    table_ids = _check("table", table_template)

    column_template = GenericWarehouseFileTemplate.column(table_ids)
    _check("column", column_template, with_ids=False)

    user_template = GenericWarehouseFileTemplate.user()
    user_ids = _check("user", user_template)

    view_ddl_template = GenericWarehouseFileTemplate.view_ddl(database_ids)
    _check("view_ddl", view_ddl_template, with_ids=False)

    query_template = GenericWarehouseFileTemplate.query(database_ids, user_ids)
    _check("query", query_template, with_ids=False)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-d", "--directory", help="Directory containing the files to be checked"
    )
    parser.add_argument(
        "--verbose",
        dest="display_issues",
        action="store_true",
        help="Show detailed logs",
    )
    args = parser.parse_args()
    process(args.directory, args.display_issues)
