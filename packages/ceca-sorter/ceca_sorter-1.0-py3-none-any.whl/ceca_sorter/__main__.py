from .ceca_sorter_base import CecaSorter
import ast
import click
import io
from typing import Tuple, Optional


def _get_last_import_expression_from_beginning(
    parsed: ast.Module
) -> Optional[ast.stmt]:
    start = False
    last: Optional[ast.stmt] = None

    for exp in parsed.body:
        if (
            not isinstance(exp, ast.Import)
            and not isinstance(exp, ast.ImportFrom) # noqa
            and not start # noqa
        ):
            continue

        start = True

        if (
            not isinstance(exp, ast.ImportFrom)
            and not isinstance(exp, ast.Import) # noqa
        ):
            return last

        last = exp

    return last


def _update_file(f: io.TextIOWrapper) -> None:
    contents = f.read()
    lines = contents.split('\n')
    parsed = ast.parse(contents)
    last_import = _get_last_import_expression_from_beginning(parsed)

    if not last_import:
        return

    to_sort = "\n".join(lines[:last_import.end_lineno])
    sorter = CecaSorter(to_sort, '\n', [])
    result = sorter.reorganize().strip()
    no_imports_contents = "\n".join(lines[last_import.end_lineno:])
    new_contents = f'{result}\n{no_imports_contents}'
    f.seek(0)
    f.write(new_contents)


@click.command()
@click.argument(
    'file_paths',
    nargs=-1,
    type=click.Path(exists=True, dir_okay=False, writable=True)
)
def _main(file_paths: Tuple[str, ...]) -> None:
    for file_path in file_paths:
        with open(file_path, 'r+', encoding='utf-8') as file:
            _update_file(file)


_main()
