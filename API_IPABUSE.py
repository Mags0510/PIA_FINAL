import requests
from datetime import datetime
import json

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Reporte guardado en: {filename}")

def generate_report(action, data, filename="reporte_final.txt"):
    with open(filename, "a") as report:
        report.write(f"\n=== {action} ===\n")
        report.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write("Datos:\n")
        json.dump(data, report, indent=4)
        report.write("\n")

def menu1():
    print("Escoge una categoría para la IP a denunciar:")
    print(""" ... """)  # Mantener la lista de categorías

    while True:
        try:
            z = int(input("Ingrese el número de la categoría: "))
            if 1 <= z <= 23:
                return z
            else:
                print("Número inválido. Por favor, ingrese un número entre 1 y 23.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def days(y):
    return y if y else "30"

def ip(x):
    return x if x else requests.get('http://checkip.amazonaws.com').text.strip()

def CheckIP(API_KEY):
    X = input("Digite la dirección IP: ")
    IP = ip(X)
    y = input("Digite los días (por defecto: 30): ")
    DAYS = days(y)

    URL = f"https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": API_KEY, "Accept": "application/json"}
    params = {"ipAddress": IP, "maxAgeInDays": DAYS}

    response = requests.get(URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Información de IP:", data)

        save = input("¿Deseas guardar los resultados? (si/no): ").strip().lower()
        if save == 'si':
            filename = f"CheckIP_{IP}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_to_file(data, filename)
        
        # Generar reporte
        generate_report("Verificación de IP", data)
    else:
        print(f"Error al consultar IP: {response.status_code} - {response.text}")

def CheckCIDR(API_KEY):
    Z = input("Digite la dirección en formato CIDR: ")
    y = input("Digite los días (por defecto: 30): ")
    DAYS = days(y)

    URL = f"https://api.abuseipdb.com/api/v2/check-block"
    headers = {"Key": API_KEY, "Accept": "application/json"}
    params = {"network": Z, "maxAgeInDays": DAYS}

    response = requests.get(URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Información de bloque CIDR:", data)

        save = input("¿Deseas guardar los resultados? (si/no): ").strip().lower()
        if save == 'si':
            filename = f"CheckCIDR_{Z.replace('/', '-')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_to_file(data, filename)
        
        # Generar reporte
        generate_report("Verificación de CIDR", data)
    else:
        print(f"Error al consultar CIDR: {response.status_code} - {response.text}")

def ReportIP(API_KEY):
    X = input("Digite la dirección IP: ")
    IP = ip(X)
    CATEGORIES = menu1()
    COMMENT = input("¿Quieres agregar algún comentario sobre esta IP?: ")

    URL = "https://api.abuseipdb.com/api/v2/report"
    headers = {"Key": API_KEY, "Accept": "application/json"}
    data = {"ip": IP, "categories": CATEGORIES, "comment": COMMENT}

    response = requests.post(URL, headers=headers, data=data)

    if response.status_code == 200:
        print("IP reportada exitosamente.")
        
        # Generar reporte
        generate_report("Reporte de IP", {"ip": IP, "categories": CATEGORIES, "comment": COMMENT})
    else:
        print(f"Error al reportar IP: {response.status_code} - {response.text}")

def main():
    API_KEY = input("Digite su API key: ")

    while True:
        print("""
        1) Verificar IP
        2) Verificar bloque CIDR
        3) Reportar IP
        4) Salir
        """)
        option = input("Seleccione una opción: ")

        if option == "1":
            CheckIP(API_KEY)
        elif option == "2":
            CheckCIDR(API_KEY)
        elif option == "3":
            ReportIP(API_KEY)
        elif option == "4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    main()

