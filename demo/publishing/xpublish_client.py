# https://pypi.org/project/xpublish/
import xarray as xr
import zarr
from fsspec.implementations.http import HTTPFileSystem


def xpublish_client():
    fs = HTTPFileSystem()
    http_map = fs.get_mapper('http://localhost:9000')

    # Open as a Zarr group.
    print("Opening as Zarr group")
    zg = zarr.open_consolidated(http_map, mode='r')
    print(zg)
    print()

    # Open as Xarray dataset.
    print("Opening as Xarray dataset")
    ds = xr.open_zarr(http_map, consolidated=True)
    print(ds)


if __name__ == "__main__":
    xpublish_client()
