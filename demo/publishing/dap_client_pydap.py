# https://github.com/pydap/pydap
import sys
import pydap.client


def dap_client_pydap(url):

    dataset = pydap.client.open_url(url)

    print("# Metadata")
    print(dataset)
    print(dataset.name)
    print(dataset.attributes)
    print()

    print("# Data")
    var = dataset["t2m"]
    # This will download data from the server.
    data = var[0, 10:14, 10:14]
    print(data.data)


if __name__ == "__main__":
    url = sys.argv[1]
    dap_client_pydap(url)
