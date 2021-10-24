import dataclasses as dataclasses
import logging
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Callable, List

from setuptools import glob

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class ProcessingResult:
    """
    This holds information about the
    result from processing a single file.
    """

    input: Path
    output: Path = None
    plot: Path = None


def json_serializer(obj):
    """
    JSON serializer for custom objects not serializable by default json code
    """

    if isinstance(obj, ProcessingResult):
        return dataclasses.asdict(obj)
    elif isinstance(obj, Path):
        return str(obj)


@dataclasses.dataclass
class FileProcessor:

    input: List[Path]
    method: Callable

    def resolve(self) -> List[Path]:
        """
        Resolve wildcards from list of input files.

        :return: List of resolved Path items.
        """
        input_paths = []
        for path_raw in self.input:
            paths = glob.glob(str(path_raw), recursive=True)
            input_paths += paths
        self.input = list(map(Path, input_paths))
        return self

    def run(self) -> List[ProcessingResult]:
        """
        Process all input files.

        :return: List of ``ProcessingResult`` instances
        """
        results: List[ProcessingResult] = []
        for infile in self.input:
            logger.info(f"Processing file {infile}")
            item = ProcessingResult(input=infile)
            with redirect_stdout(sys.stderr):
                self.method(item)
            results.append(item)

        return results
