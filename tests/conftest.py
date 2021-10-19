import os

if "GM_DATA_PATH" in os.environ:
    del os.environ["GM_DATA_PATH"]
