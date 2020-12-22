# https://pypi.org/project/skinnywms/
import os
import sys

# This code is weird because SkinnyWMS has all code
# of ``skinnywms.wmssvr`` on the global module scope.
# Will have to send a pull request to get things straight.
#
# So, maybe better use ``skinny-wms --path=$BASE_STORE_DIR/tmp``.


def wms_server(filepath=None):
    if filepath:
        os.environ["SKINNYWMS_DATA_PATH"] = filepath
    from skinnywms.wmssvr import application
    application.run(debug=True, threaded=False)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv.pop()
        wms_server(filepath)
    else:
        wms_server()
