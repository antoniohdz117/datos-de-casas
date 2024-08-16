#CODIGO PARA PRODUCCION

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
            
service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", exp_opt)
options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = "https://propiedades.com/df/casas?pagina=1"

link = []
pag = 1
while True:
    
    #consegui el primer driver para extraer el codigo
    driver.get(url)
    contenido = driver.page_source
    soup = bs(contenido)
    
    #extraccion del link de cada casa
    divs = soup.find_all("div", class_="sc-402fc8bf-3 btXdmE pcom-property-card-body-main-info-street-id")    
    for div in divs:
        pagina = div.find("a")
        if pagina and "href" in pagina.attrs:
            if pagina in link:
                continue
            else:
                link.append(pagina["href"])
                
    #valor = randrange(1,3)           
    time.sleep(3)
    for n in range(len(link)):
        print(f"casa {n}")
        
        #segundo driver para scrapear cada casa
        driver2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver2.get(link[n])
        contenido2 = driver2.page_source
        for seguro in range(2):
            contenido2 = driver2.page_source
            soup2 = bs(contenido2)    
       
        #PARAMETROS
        idInmueble = []
        tipoVenta = []
        ubicacion = []
        precio = []
        precioxMetro = []
        recamaras = []
        baños = []
        estacionamiento = []
        edadInmueble = []
        areaTerreno = []
        areaConstruida = []
        jardin = []
        descripcion = []
        
        #ubicacion
        dato = soup2.find("div",class_="text-design").find('h1').text
        ubicacion.append(dato)
        
        #tipoventa
        dato = soup2.find_all("div",attrs=({"class":"sc-5f12f68d-0 kWLa-dc"}))
        tipoVenta.append(dato[1].text)
        
        #precio    
        dato = soup2.find('div',class_='sc-623147a8-1 xPkUE price-text').find('h2')
        precio.append(dato.text)
        
        #descripcion
        dato = soup2.find("p",class_='description-text')
        descripcion.append(dato.text.replace("\n",""))
        
        #precio por metro
        dato = soup2.find("div",attrs=({"class":"price"}))
        precioxMetro.append(dato.text)

        #EXTRACCION DE LAS CARACTERISTICAS DE LA CASA
        propiedades = soup2.find_all(class_="characteristic")
        for caracteristica in propiedades:
            text = caracteristica.find('div', class_='description-text').get_text(strip=True)
            dato = caracteristica.find('div', class_='description-number').get_text(strip=True)     
            if text == "ID DEL INMUEBLE":
                idInmueble.append(dato)
            if text == "RECÁMARAS":
                recamaras.append(dato)
            if text == "BAÑOS":
                baños.append(dato)
            if text == "ESTACIONAMIENTOS":
                estacionamiento.append(dato)
            if text == "Edad del inmueble":
                edadInmueble.append(dato)
            if text == "ÁREA TERRENO":
                areaTerreno.append(dato)
            if text == "ÁREA CONSTRUIDA":
                areaConstruida.append(dato)
            if text == "Jardín":
                jardin.append(dato)
        
        
        #condisionadores para agregar elementos en caso de no encontrarlos
        if len(recamaras)<1:
            recamaras.append("")

        if len(estacionamiento)<1:
            estacionamiento.append("")

        if len(jardin)<1:
            jardin.append("")

        
        #dataframe
        df = pd.DataFrame({"idInmueble":idInmueble,"tipoVenta":tipoVenta,"precio":precio,"precioxMetro":precioxMetro,"tipoVenta":tipoVenta,"recamaras":recamaras,"baños":baños,"estacionamiento":estacionamiento,"edadInmueble":edadInmueble,"areaConstruida":areaConstruida,"areaTerreno":areaTerreno,"jardin":jardin, "descripcion":descripcion,"link":link[n]})

        #print(df)
        #print(tipoVenta)
    
    #ITERADOR PARA AVANZAR DE PAGINA SOLO AGREGA LAS PAGINAS QUE GUSTES QUE ITERE
    if pag < 3:
        pag+=1
        url = f"https://propiedades.com/df/casas?pagina={pag}"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        link = []
    else:
        break
        
