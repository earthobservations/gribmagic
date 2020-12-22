import sys
import xarray as xr


def dap_client_xarray(url):
    ds = xr.open_dataset(url, decode_times=False)
    print(ds)


if __name__ == "__main__":
    url = sys.argv[1]
    dap_client_xarray(url)
