# https://pypi.org/project/OWSLib/
from owslib.wms import WebMapService


def wms_client():
    wms = WebMapService('http://localhost:5000/wms')

    print(wms.identification)
    print(wms.contents)


if __name__ == "__main__":
    wms_client()
