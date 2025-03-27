# Webscraping: multivitaminicos HSN Scraper
Este proyecto tiene como objetivo extraer información de productos multivitamínicos de la página web de HSNstore utilizando técnicas de web scraping con Selenium y BeautifulSoup en Python.

## Integrantes del Grupo
- María Amparo Blanch Ruiz
- Noelia Pérez Benavent

## Estructura del Repositorio
El repositorio consta de los siguientes archivos y carpetas:

- `requirements.txt`: Un archivo de texto que contiene las dependencias necesarias para ejecutar el código.
- `LICENSE`: Un archivo con la licencia del proyecto.
- `dataset`
  - `multivitaminicos_hsn.csv`: Archivo CSV con los datos extraídos de la página web. Incluye campos como Código, Nombre, Clasificación, Grupo, Dosificación, Precio, Precio con descuento, % Descuento, Rating, Número de valoraciones, Serie, Descripción, Edulcorantes, Veganos, Vegetarianos, OMG, Gluten, Lactosa, Lácteos, Soja, Huevo, Conservantes, Colorantes, Frutos de cáscara y Pescado.
- `source`
  - `scraper.py`: El código fuente en Python que realiza el web scraping.
    
## Librerías y versiones
- Python 3.12
- selenium 4.15.2
- requests 2.31.0
- bs4 0.0.1
- beautifulsoup4 4.12.2
  
## Uso del Código
Para ejecutar el código, se necesita tener instalado Python y las dependencias listadas en `requirements.txt`. Se pueden instalar ejecutando el siguiente comando en la terminal:

`pip3 install -r requirements.txt`

Una vez instaladas las dependencias, se puede ejecutar el script con el siguiente comando:

`python3 scraper.py`

## DOI de Zenodo
El dataset generado tiene el siguiente DOI de Zenodo: https://doi.org/10.5281/zenodo.10067284



