import re
import geopy
from geopy.geocoders import Nominatim
import time
import pandas as pd
from src.processing.dist import calculate_bearing
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import string
import unicodedata

nltk.download('punkt')
nltk.download('stopwords')

def obtener_lat_long():
    codigos_postales = [str(48000 + x) for x in range(1,16)]
    geolocator = Nominatim(user_agent='nlp')
    resultados = {}

    for codigo in codigos_postales:
        location = geolocator.geocode(f"{codigo}, España")
        if location:
            resultados[codigo] = [location.latitude, location.longitude]
        else:
            resultados[codigo] = [None, None]
        time.sleep(1)

    direcciones = {}
    lat1, lon1 = 43.263386002871265, -2.9371692887362872
    for codigo, (lat2, lon2) in resultados.items():
        direccion = calculate_bearing(lat1, lon1, lat2, lon2)
        direcciones[codigo] = direccion 
    return direcciones

def asignar_valor_por_cp(df, diccionario):
    df['direction'] = None
    for index, row in df.iterrows():
        direccion = row['street']
        if isinstance(direccion, str):
            cp_encontrado = re.search(r'\b\d{5}\b', direccion)
            if cp_encontrado:
                cp = cp_encontrado.group(0)
                if cp in diccionario:
                    df.at[index, 'direction'] = diccionario[cp]
    return df


def limpiar_texto(texto):
    texto = texto.lower()
    tokens = word_tokenize(texto, language='spanish')
    tabla = str.maketrans('', '', string.punctuation)
    tokens = [palabra.translate(tabla) for palabra in tokens]
    tokens = [unicodedata.normalize('NFKD', palabra).encode('ASCII', 'ignore').decode('utf-8') for palabra in tokens]
    return ' '.join(tokens)


def procesar_y_graficar(df, colname, num_terminos=10):
    df['description'] = df['description'].fillna('')
    df[colname] = df['title'].astype(str) + ' ' + df['description'].astype(str)
    df['texto_limpio'] = df[colname].apply(limpiar_texto)
    texto_total = ' '.join(df['texto_limpio'].dropna())

    # Tokenizar el texto
    tokens = word_tokenize(texto_total, language='spanish')

    # Filtrar stopwords en español
    palabras_ignoradas = set(stopwords.words('spanish'))
    tokens = [palabra for palabra in tokens if palabra not in palabras_ignoradas and palabra.isalpha()]

    # Calcular la frecuencia de cada palabra
    freq = FreqDist(tokens)

    # Obtener las palabras más frecuentes
    palabras_comunes = freq.most_common(num_terminos)

    # Preparar datos para el gráfico
    palabras = [palabra for palabra, _ in palabras_comunes]
    frecuencias = [frecuencia for _, frecuencia in palabras_comunes]

    # Crear gráfico de barras
    plt.figure(figsize=(10, 8))
    plt.bar(palabras, frecuencias, color='blue')
    plt.xlabel('Términos')
    plt.ylabel('Frecuencia')
    plt.title('Términos más frecuentes en el texto')
    plt.xticks(rotation=45)
    plt.show()
    return palabras_comunes,df


def encontrar_coincidencias(texto):
    terminos_hosteleria = ['bar', 'restaurante', 'taberna', 'cafe', 'hamburguesa']
    encontrados = [termino for termino in terminos_hosteleria if termino in texto]
    return encontrados if encontrados else ['otros']


def tipo_establecimiento_direccion(df):
    df['tipo_establecimiento'] = df['texto_limpio'].apply(encontrar_coincidencias)
    df = pd.concat([df, pd.get_dummies(df['direction'])], axis=1)
    df['tipo_establecimiento'] = df['texto_limpio'].apply(encontrar_coincidencias) 
    df = pd.concat([df, pd.get_dummies(df['tipo_establecimiento'].explode())], axis=1)
    df.drop(columns=['tipo_establecimiento','direction','TD', 'texto_limpio'], inplace=True)
    return df