import intake


def main():
    url = "https://raw.githubusercontent.com/NCAR/intake-esm-datastore/master/catalogs/pangeo-cmip6.json"
    col = intake.open_esm_datastore(url)
    print(col.df.head())


if __name__ == "__main__":
    main()
