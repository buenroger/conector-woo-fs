import requests
import schedule
import time
import json
from datetime import datetime, timedelta

# Función para cargar la configuración desde un archivo JSON
def cargar_configuracion():
    with open('config.json', 'r') as archivo:
        return json.load(archivo)

# Carga la configuración
config = cargar_configuracion()

# Configura tus claves de la API de WooCommerce aquí
consumer_key = 'tu_consumer_key'
consumer_secret = 'tu_consumer_secret'
woocommerce_url = 'https://tu-tienda.com/wp-json/wc/v3/'

# Función para obtener pedidos
def obtener_pedidos():
    try:
        # Configura el lapso de tiempo para los pedidos
        # Por ejemplo, los últimos 30 minutos
        tiempo_final = datetime.utcnow()
        tiempo_inicial = tiempo_final - timedelta(minutes=30)

        # Formatea las fechas en el formato correcto
        fecha_inicial = tiempo_inicial.strftime('%Y-%m-%dT%H:%M:%S')
        fecha_final = tiempo_final.strftime('%Y-%m-%dT%H:%M:%S')

        # Endpoint de la API para obtener pedidos
        url = f"{woocommerce_url}orders?after={fecha_inicial}&before={fecha_final}"

        # Realiza la solicitud a la API
        respuesta = requests.get(url, auth=(consumer_key, consumer_secret))

        # Verifica si la solicitud fue exitosa
        if respuesta.status_code == 200:
            pedidos = respuesta.json()
            print("Pedidos obtenidos:")
            for pedido in pedidos:
                print(pedido)
        else:
            print("Error al obtener los pedidos:", respuesta.status_code)

    except Exception as e:
        print("Ocurrió un error:", e)

# Programa la tarea
schedule.every().hour.do(obtener_pedidos)

# Bucle infinito para ejecutar las tareas programadas
while True:
    schedule.run_pending()
    time.sleep(1)