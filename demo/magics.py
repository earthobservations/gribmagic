# https://pypi.org/project/Magics/
import sys

from Magics import macro as magics


def magics_demo(filepath):

    # Setting of the output file name
    output = magics.output(output_name="magics",
                           output_formats=['png'],
                           output_name_first_page_number="off")

    # Import the data
    data = magics.mgrib(grib_input_file_name=filepath)

    # Apply an automatic styling
    contour = magics.mcont(contour_automatic_setting="ecmwf")
    coast = magics.mcoast()
    magics.plot(output, data, contour, coast)


if __name__ == "__main__":
    #filepath = "2m_temperature.grib"
    filepath = sys.argv[1]
    magics_demo(filepath)
