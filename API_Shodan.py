import shodan
from datetime import datetime

def generate_report(data, filename="reporte_shodan.txt"):
    with open(filename, "a") as report:
        report.write(f"\n=== Reporte de búsqueda en Shodan ===\n")
        report.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write("Datos:\n")
        report.write(data)
        report.write("\n")

APIKEY = input("Introduce tu API Key de Shodan: ")
API = shodan.Shodan(APIKEY)
consulta = 'apache 2.4.49'

try:
    resultados = API.search(consulta)
    resultado_info = f'Resultados para la consulta "{consulta}": {resultados["total"]} encontrados\n\n'
    print(resultado_info)
    
    with open("resultados_shodan.txt", "w") as archivo:
        archivo.write(resultado_info)
        
        for resultado in resultados["matches"]:
            ip = resultado.get('ip_str', 'N/A')
            puerto = resultado.get('port', 'N/A')
            organizacion = resultado.get('org', 'N/A')
            pais = resultado.get('location', {}).get('country_name', 'N/A')
            
            info = (
                f"IP: {ip}\n"
                f"Puerto: {puerto}\n"
                f"Organizacion: {organizacion}\n"
                f"Ubicacion: {pais}\n"
                f"- - - - - - - - - - - - -\n"
            )
            print(info)
            archivo.write(info)

    print("Informacion guardada en resultados_shodan.txt")

    # Generar reporte
    report_content = resultado_info + ''.join([
        f"IP: {res.get('ip_str', 'N/A')}, Puerto: {res.get('port', 'N/A')}, "
        f"Organizacion: {res.get('org', 'N/A')}, Ubicacion: {res.get('location', {}).get('country_name', 'N/A')}\n"
        for res in resultados["matches"]
    ])
    generate_report(report_content)

except shodan.APIError as e:
    print(f"Error: {e}")
