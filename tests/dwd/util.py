import operator
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from gribmagic.dwd.pipeline import process
from gribmagic.util import load_module


def nearest_multiple(number, base=10):
    return base * round(number / base)


def previous_modelrun():
    timestamp = datetime.utcnow() - timedelta(hours=6)
    hour = nearest_multiple(timestamp.hour, base=6)
    timestamp = timestamp.replace(hour=hour, minute=0, second=0, microsecond=0)
    modelrun = timestamp.strftime("%Y%m%d%H")
    return modelrun


def load_recipe(filename):
    HERE = Path(__file__).parent
    recipe_file = HERE / filename
    recipe_module = load_module("gribmagic.recipe", recipe_file)
    recipe_instance = recipe_module.recipe
    return recipe_instance


def run_icon_d2_vmax_recipe(modelrun):

    recipe_instance = load_recipe("recipe_icon_d2_vmax10m.py")

    with tempfile.TemporaryDirectory() as tmpdirname:
        output = Path(tmpdirname)

        results = process(recipe=recipe_instance, timestamp=modelrun, output=output)
        results = next(results)

        assert len(results) == 3

        results = sorted(results, key=operator.itemgetter("url"))
        url = results[0]["url"]
        assert (
            f"icon-d2_germany_regular-lat-lon_single-level_{modelrun}_000_2d_vmax_10m.grib2.bz2"
            in url
        ), url

        return results


def run_icon_global_temp2m_recipe(modelrun):

    recipe_instance = load_recipe("recipe_icon_global_temp2m.py")

    with tempfile.TemporaryDirectory() as tmpdirname:
        output = Path(tmpdirname)

        results = process(recipe=recipe_instance, timestamp=modelrun, output=output)
        results = next(results)

        assert len(results) == 3

        results = sorted(results, key=operator.itemgetter("url"))
        url = results[0]["url"]
        assert f"icon_global_icosahedral_single-level_{modelrun}_000_T_2M.grib2.bz2" in url, url

        return results
