# Derived from https://confluence.ecmwf.int/display/ECC/grib_nearest.
#
# Copyright 2005-2018 ECMWF.
# Copyright 2020 Andreas Motl.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from __future__ import print_function

import operator
import traceback
import sys

from eccodes import codes_grib_new_from_file, codes_grib_find_nearest, codes_release, CodesInternalError
from scipy.constants import convert_temperature

VERBOSE = 1  # verbose error reporting


def example(INPUT, point, use_celsius=False):

    f = open(INPUT, 'rb')
    lat, lon = point

    gid = codes_grib_new_from_file(f)

    print(f"Nearest grid point to location lat={lat}, lon={lon}")
    item = codes_grib_find_nearest(gid, lat, lon)[0]
    if use_celsius:
        convert_item(item)
    print(dict(item))
    print()

    print(f"Nearest four grid points to location lat={lat}, lon={lon}")
    items = codes_grib_find_nearest(gid, lat, lon, is_lsm=False, npoints=4)
    for item in sorted(items, key=operator.itemgetter("distance")):
        if use_celsius:
            convert_item(item)
        print(dict(item))

    codes_release(gid)
    f.close()


def convert_item(item):
    kelvin = item["value"]
    celsius = convert_temperature(kelvin, "Kelvin", "Celsius")
    item["value"] = celsius


def main():
    point = (52.52437, 13.41053)
    use_celsius = True
    try:
        example(sys.argv[1], point, use_celsius)
    except CodesInternalError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            sys.stderr.write(err.msg + '\n')

        return 1


if __name__ == "__main__":
    sys.exit(main())
