#!/usr/bin/env python
# coding: utf-8

import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import csv

# Calculamos el tiempo de respuesta para introducir retrasos en las peticiones consecutivas
print("Calculando el tiempo de respuesta ...")
delay = 0
for term in ["acidos-grasos-esenciales", "anti-alergia", "antioxidantes"]:
    try:
        t0 = time.time()
        requests.get("https://www.hsnstore.com/salud-bienestar/", params=dict(query=term))
        delay += (time.time() - t0) / 3  # Promedio del tiempo de respuesta en segundos
    except requests.RequestException as e:
        print(f"Error: no se pudo realizar la solicitud. {str(e)}")

print(f"Tiempo de retraso promedio estimado: {delay} segundos")
if delay < 5:
     delay = 10 # Así en el caso de que fuera menor seguiríamos cumpliendo con el fichero robots.txt de la web
else:
     delay = delay*2

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
}

# Inicializa el controlador del navegador
driver = webdriver.Chrome()

# Abre la pagina web
driver.get("https://www.hsnstore.com/")

try:
    # Busca el campo de las cookies y las acepta
    accept_cookies = driver.find_element(By.XPATH, '//*[@id="cookiebar-outer"]/div/div/div[2]/div[2]/a[2]')
    accept_cookies.click()
    print("Cookies aceptadas")
except Exception as e:
    # Maximiza la ventana del navegador
    driver.maximize_window()
    print(f"Error: no se pudo realizar la solicitud. {str(e)}")
   
    

try:
    # Encuentra el campo de búsqueda y envía una consulta
    search_box = driver.find_element(By.ID, "search")
    search_query = "multivitaminicos"  # "*" busca todos los registros
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.ENTER)
    print("Búsqueda realizada")

    # Espera a que los resultados se carguen
    driver.implicitly_wait(10)  # Espera un máximo de 10 segundos

    # Se desplaza hacia abajo para cargar más resultados
    scroll_pause_time = 1  # Pausa entre cada desplazamiento en segundos
    screen_height = driver.execute_script("return window.screen.height;")  # Altura de la pantalla

    i = 1
    while True:
        # Calcula la posición actual de desplazamiento
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Realiza el desplazamiento hacia abajo
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)
        # Comprueba si se ha llegado al final de la página
        if screen_height * i > scroll_height:
            break
    print("Productos cargados")

except Exception as e:
    print(f"Error: no se pudo realizar la solicitud. {str(e)}")

# Encuentra y extrae los resultados
li_elements = driver.find_elements('css selector', 'li.item.sqr-resultItem')

urls = []
codigos = []
nombres = []

for li in li_elements:
    codigo = li.get_attribute('data-id')

    # Obtiene el link (href) y el título del elemento <a>
    elemento_a = li.find_element(By.CSS_SELECTOR, ".product-image")
    url = elemento_a.get_attribute('href')
    nombre = elemento_a.get_attribute('title')

    urls.append(url)
    codigos.append(codigo)
    nombres.append(nombre)

print(len(urls))

# Creación del archivo CSV
with open("multivitaminicos_HSN.csv", "w", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    # Cabecera
    writer.writerow(['Codigo', 'Nombre', 'Clasificación', 'Grupo', 'Dosificación', 'Precio', 'Precio_descuento',
                     '%_Descuento', 'Rating', 'Numero_valoraciones', 'Serie', 'Descripcion', 'Edulcorantes', 'Veganos',
                     'Vegetarianos', 'OMG', 'Gluten', 'Lactosa', 'Lacteos', 'Soja', 'Huevo', 'Conservantes',
                     'Colorantes', 'Frutos_cascara', 'Pescado'])

n = 0
for url, codigo, nombre in zip(urls, codigos, nombres):
    n += 1
    print(n)
    print(f"Scrapping: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            price_div_list = [soup.find("div", class_="final-price").text.strip()]
            old_price_div_list = [soup.find("div", class_="regular-price").text.strip()]
            discount_div_list = [soup.find("div", class_="discount-percentage").text.strip()]                  
            size_div_list = [""]
            
            driver.get(url)
            
            try:
                product_size_selector = driver.find_element(By.CLASS_NAME, "peso-tamano-product").find_elements(By.CLASS_NAME, "weight-buttons-label")
                size_div_list = [product_size_selector[0].text.strip()]
                for x in product_size_selector[1::]:
                    time.sleep(2)
                    x.click()
                    size_div_list.append(x.text.strip())
                    soupProductSize = BeautifulSoup(driver.page_source, 'html.parser')
                    price_div_list.append(soupProductSize.find("div", class_="final-price").text.strip())
                    old_price_div_list.append(soupProductSize.find("div", class_="regular-price").text.strip())
                    discount_div_list.append(soupProductSize.find("div", class_="discount-percentage").text.strip())
            
            #Si no ha encontrado el selector de tamaños, es que el producto solo tiene una dosis, por lo que se añade una fila con el precio de la dosis única
            except selenium.common.exceptions.NoSuchElementException:
                pass
            
            clasificacion_div = soup.find("div", class_="class container")
            clasificacion_elements = clasificacion_div.find_all("li")
            clasificacion = clasificacion_elements[1].get_text(strip=True)
            grupo = clasificacion_elements[2].get_text(strip=True)
            
            rating_div = soup.find("div", class_="rating")
            span_rating = rating_div.find('span', class_='trustedshop_up_rating')
            rating_value = span_rating.get_text(strip=True)
            
            span_valoraciones = soup.find('span', class_='amount')
            valoraciones = span_valoraciones.get_text(strip=True)
            
            serie_div = soup.find("div", class_="col-xs-12 no-gutter brand_link brand")
            span_serie = serie_div.find('span', itemprop='name')
            serie = span_serie.get_text(strip=True)
            
            descripcion_div = soup.find("div", class_="col-xs-12 no-padding-lat product_desc")
            descripcion = descripcion_div.find('p').text.strip()
            
            
            try: 
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.ID, "product_characteristics")))
            
                icon_elements = driver.find_elements(By.CSS_SELECTOR, '.product_images_icon[title]')

                caracteristicas=[]
               
                # Itera a través de los elementos <i> y obtiene el valor del atributo title
                for icon_element in icon_elements:
                    title = icon_element.get_attribute("title")
                    caracteristicas.append(title)

                def caracteristica_pos(lista, caracteristica):
                    return caracteristica in lista

                def caracteristica_neg(lista, caracteristica):
                    return not(caracteristica in lista)
    

                edulcorantes = caracteristica_neg(caracteristicas, "Sin Edulcorantes")
                veganos = caracteristica_pos(caracteristicas, "Apto para Veganos")
                vegetarianos = caracteristica_pos(caracteristicas, "Apto para Vegetarianos")
                omg = caracteristica_neg(caracteristicas, "Sin OMG")
                gluten = caracteristica_neg(caracteristicas, "Sin Gluten")
                lactosa = caracteristica_neg(caracteristicas, "Sin Lactosa")
                lacteos = caracteristica_neg(caracteristicas, "Sin Lacteos")
                soja = caracteristica_neg(caracteristicas, "Sin Soja")
                huevo = caracteristica_neg(caracteristicas, "Sin Huevo")
                conservantes = caracteristica_neg(caracteristicas, "Sin Conservantes")
                colorantes = caracteristica_neg(caracteristicas, "Sin Colorantes Artificiales")
                frutos_cascara = caracteristica_neg(caracteristicas, "Sin Frutos de Cascara")
                pescado = caracteristica_neg(caracteristicas, "Sin Pescado")
                
            #Si no ha encontrado las características (el producto está agotado en todas sus dosis), no se incluye el producto en el csv pasa a la siguiente url     
            except selenium.common.exceptions.TimeoutException:
                continue
           
            with open("multivitaminicos_HSN.csv","a", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=',') 
                for(price_div, old_price_div, discount_div, size_div) in zip(price_div_list, old_price_div_list, discount_div_list, size_div_list):
                    writer.writerow([codigo, nombre, clasificacion, grupo, size_div, old_price_div.strip(), price_div, discount_div, rating_value, valoraciones, serie, descripcion, edulcorantes, veganos, vegetarianos, omg, gluten, lactosa, lacteos, soja, huevo, conservantes, colorantes, frutos_cascara, pescado])
            print("Producto guardado en el fichero")
            time.sleep(delay)
            
    except requests.RequestException as e:
        print(f"Error: no se pudo realizar la solicitud. {str(e)}")
        break

# Cierra el navegador
driver.quit()

print(headers["User-Agent"])
