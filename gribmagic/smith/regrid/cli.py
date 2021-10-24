import json
import logging
from pathlib import Path
from typing import List

import click

from gribmagic.smith.regrid.engine import GridTransformationLibrary, RegridTransformer
from gribmagic.smith.util import ProcessingResult, json_serializer
from gribmagic.util import setup_logging


@click.command(help=RegridTransformer.__doc__)
@click.argument("input", type=click.Path(file_okay=True, dir_okay=True), required=True, nargs=-1)
@click.option(
    "--output",
    envvar="GM_DATA_PATH",
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
    help="The output directory",
    required=True,
)
@click.option(
    "--kind", help="Which grid kind to select. Use `global`", required=False, default="global"
)
@click.option(
    "--resolution",
    type=float,
    help="Which resolution to select. Use `0.125` or `0.250`",
    required=False,
    default=0.250,
)
@click.option(
    "--dry-run", is_flag=True, help="Whether to simulate processing", required=False, default=False
)
def main(
    input: List[Path],
    output: Path,
    kind: str,
    resolution: float,
    dry_run: bool,
):

    # Setup logging.
    setup_logging(level=logging.DEBUG)

    # Invoke the machinery.

    # Load grid transformation asset files.
    gridlib = GridTransformationLibrary()
    gridinfo = gridlib.get_info(kind=kind, resolution_dw=resolution)

    # Extend output path with resolution.
    resolution_label = str(int(resolution * 1000))
    output = Path(output).joinpath(resolution_label)

    # Transform grid / regrid.
    transformer = RegridTransformer(gridinfo=gridinfo, input=input, output=output, dry_run=dry_run)
    transformer.setup()
    results: List[ProcessingResult] = transformer.process()

    # Report about the outcome.
    print(json.dumps(results, default=json_serializer, indent=4))


if __name__ == "__main__":  # pragma: nocover
    main()
