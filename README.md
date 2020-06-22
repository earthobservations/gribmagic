# weather_forecast_downloader
Project to handle download of public weather forecast data. 


# Setting up and installation

### Environement Variables
To use this project you have to define the following environment variables:
```
MODEL_CONFIG={PATH_TO_PROJECT}/config/model_config.yml"
MODEL_VARIABLES_MAPPING={PATH_TO_PROJECT}/config/model_variables_mapping.yml"
MODEL_VARIABLES_LEVELS_MAPPING={PATH_TO_PROJECT}/config/model_variables_levels_mapping.yml"

BASE_STORE_DIR={PATH_TO_PROJECT}/data
```
The **BASE_STORE_DIR** points to the project intern **data** directory per default. 
 

### Using Docker

To use the weather_forecast_downloader in a Docker container, you just have to build the image from this project

```
docker build -t "weather_forecast_downloader" .
```

To run the tests in the given environment, just call 

```
docker run -ti -v $(pwd):/app weather_forecast_downloader:latest pytest tests/
```
from the main directory. To work in an iPython shell you just have to change the command `pytest tests/` to `ipython`.

 
