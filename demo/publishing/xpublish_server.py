# https://pypi.org/project/xpublish/
import sys
import xarray as xr
import xpublish


def xpublish_server(filepath=None):

    if filepath is None:
        ds = xr.tutorial.open_dataset(
            "air_temperature", chunks=dict(lat=5, lon=5),
        )
    else:
        ds = xr.open_dataset(filepath, engine="cfgrib")
        #ds = xr.open_dataset(filepath, engine="cfgrib", chunks=dict(latitude=5, longitude=5))

    rest = xpublish.Rest(ds)
    rest.serve(host="localhost")


if __name__ == "__main__":
    try:
        filepath = sys.argv[1]
    except IndexError:
        filepath = None
    xpublish_server(filepath)
