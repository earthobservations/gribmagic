# https://pypi.org/project/Magics/
from Magics import macro as magics


def magics_demo():

    # Setting of the output file name
    output = magics.output(output_name="magics",
                           output_formats=['png'],
                           output_name_first_page_number="off")

    # Import the  data
    data = magics.mgrib(grib_input_file_name="2m_temperature.grib")

    # Apply an automatic styling
    contour = magics.mcont(contour_automatic_setting="ecmwf")
    coast = magics.mcoast()
    magics.plot(output, data, contour, coast)


if __name__ == "__main__":
    magics_demo()
