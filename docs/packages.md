# Poetry

poetry init

## Add API dependencies

poetry add fastapi psycopg2-binary sqlalchemy uvicorn influxdb-client \
pandas numpy geopy peakutils pyproj python-dotenv utm bcrypt \
python-multipart loguru "pydantic[email]" --group api

## Add Notebook dependencies

poetry add numpy pandas plotly peakutils geopy pyproj utm seaborn pyarrow \
python-dotenv panel ipywidgets import-ipynb --group notebook

//added this later to save the plots into images
poetry add kaleido==0.2.1 --group notebook

poetry add keplergl mapboxgl --group notebook

## Add Scraper dependencies

poetry add selenium --group scraper

## Commands

poetry env info
poetry env list
poetry shell

poetry update -> to apply changes

exit - deactivate

## Visualization packages

- matplotlib
- seaborn
- plotly
- mapbox/mapboxgl -> fucking AWESOME
- leafmap
- pydeck
- keplergl
- folium
- cesium

## Used in this project

- plotly
- mapbox