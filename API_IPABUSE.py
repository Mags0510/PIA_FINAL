import requests
import subprocess

def menu1():
    print("Escoge una categoría para la IP a denunciar:")
    print("""
    1)  DNS Compromise
    2)  DNS Poisoning
    3)  Fraud Orders
    4)  DDoS Attack
    5)  FTP Brute-Force
    6)  Ping of Death
    7)  Phishing
    8)  Fraud VoIP
    9)  Open Proxy
    10) Web Spam
    11) Email Spam
    12) Blog Spam
    13) VPN IP
    14) Port Scan
    15) Hacking
    16) SQL Injection
    17) Spoofing
    18) Brute-Force
    19) Bad Web Bot
    20) Exploited Host
    21) Web App Attack
    22) SSH
    23) IoT Targeted
    """)
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

def cidr (z):
    if z == "":
        lineaps1 = subprocess.check_output(
            "powershell -ExecutionPolicy Bypass -Command \"ipconfig | Select-String -Pattern 'subred'\"",
            shell=True, text=True
        )
 
        lineaps2 = [line.split(":")[1].strip() for line in lineaps1.splitlines() if "subred" in line]
 
        CIDR = lineaps2[0] + "/24"
 
    return CIDR

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
    else:
        print(f"Error al consultar IP: {response.status_code} - {response.text}")


def CheckCIDR(API_KEY):
    Z = input("Digite la dirección en formato CIDR: ")
    CIDR = cidr(Z)
    y = input("Digite los días (por defecto: 30): ")
    DAYS = days(y)
    URL = f"https://api.abuseipdb.com/api/v2/check-block"
    headers = {"Key": API_KEY, "Accept": "application/json"}
    params = {"network": CIDR, "maxAgeInDays": DAYS}

    response = requests.get(URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Información de bloque CIDR:", data)
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
