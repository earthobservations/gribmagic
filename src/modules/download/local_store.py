""" functions to decompress dowloaded files """
import bz2, shutil
from io import BytesIO
from pathlib import Path


def bunzip_store(file: BytesIO, local_intermediate_file: Path):
    with bz2.BZ2File(file) as fr, local_intermediate_file.open(mode="wb") as fw:
        shutil.copyfileobj(fr, fw)


def store(file: BytesIO, local_intermediate_file: Path):
    with file as in_stream, local_intermediate_file.open('wb') as out_file:
        shutil.copyfileobj(in_stream, out_file)