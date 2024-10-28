import os
import subprocess
import argparse

# Establecer la ruta a la carpeta donde están los scripts
script_path = os.path.dirname(os.path.abspath(__file__))

# Función para ejecutar scripts de PowerShell
def run_powershell_script(script_name):
    script = os.path.join(script_path, script_name)
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script], check=True)

# Función para ejecutar scripts de Python
def run_python_script(script_name):
    script = os.path.join(script_path, script_name)
    subprocess.run(["python", script], check=True)

# Función para ejecutar scripts de Bash
def run_bash_script(script_name):
    script = os.path.join(script_path, script_name)
    subprocess.run(["bash", script], check=True)

def execute_module(option):
    commands = {
        1: "API_IPABUSE.py",
        2: "Complejo.py",
        3: "deteccion.py",
        4: "escaneo_puertos.sh",
        5: "ListadoDeArchivosOcultos.psm1",
        6: "modulo2.psm1",
        7: "Modulo_UsoRecursos.psm1",
        8: "Monitoreo_Red.sh",
        9: "trafico.py",
        10: "virus.psm1",
    }

    if 1 <= option <= 10:
        script_name = commands.get(option)
        script_path_full = os.path.join(script_path, script_name)

        print(f"Ruta completa del script: {script_path_full}")  # Depuración: muestra la ruta completa

        if os.path.exists(script_path_full):
            try:
                print(f"Ejecutando: {script_name}")
                # Determinamos el tipo de script y ejecutamos la función correspondiente
                if script_name.endswith('.py'):
                    run_python_script(script_name)
                elif script_name.endswith('.ps1'):
                    run_powershell_script(script_name)
                elif script_name.endswith('.sh'):
                    run_bash_script(script_name)
                elif script_name.endswith('.psm1'):
                    print(f"Importando el módulo: {script_name}")  # Cambiar la ejecución directa a importación
                    run_powershell_script(script_name)  # Para scripts de módulo de PowerShell
                else:
                    print("Tipo de script no soportado.")
            except subprocess.CalledProcessError as e:
                print(f"Error al ejecutar {script_name}: {e}")
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")  # Manejo de errores inesperados
        else:
            print(f"El archivo no existe: {script_path_full}")  # Mensaje de error
    else:
        print("Opción no válida. Debe ser un número entre 1 y 10.")

def show_menu():
    print("Seleccione una opción:")
    print("1: API_IPABUSE.py - Analiza IPs en relación con abusos conocidos.")
    print("2: Complejo.py - Calcula la complejidad de un conjunto de datos.")
    print("3: deteccion.py - Realiza detección de patrones en datos.")
    print("4: escaneo_puertos.sh - Escanea puertos en una red específica.")
    print("5: ListadoDeArchivosOcultos.psm1 - Lista archivos ocultos en el sistema.")
    print("6: modulo2.psm1 - Ejecuta funciones del segundo módulo de PowerShell.")
    print("7: Modulo_UsoRecursos.psm1 - Monitorea el uso de recursos del sistema.")
    print("8: Monitoreo_Red.sh - Realiza monitoreo de tráfico de red.")
    print("9: trafico.py - Analiza el tráfico de red en tiempo real.")
    print("10: virus.psm1 - Proporciona funciones para gestionar virus y malware.")
    print("0: Salir - Cierra el programa.")

def main():
    # Mis comentarios de uso como tal
    """
    Este script ejecuta diferentes scripts de Python, PowerShell y Bash según la opción elegida.

    Uso:
        -o OPCION : Especifica el número del script a ejecutar (1-10).
        -i : Muestra información sobre el script seleccionado.
        -r : Genera un reporte de ejecución.

    Ejemplo:
        python menu_principal.py -h # Muestra informacion del menu principal.
        python prueba.py -o 1     # Ejecuta el script 1.
        python prueba.py -o 2 -i  # Muestra información sobre el script 2.
        python menu_principal.py -o 2 -i -r # Genera un reporte de el script 2.
        
    """
    
    
    # Configuración de argparse
    parser = argparse.ArgumentParser(description='Script de ejecución de módulos.')
    parser.add_argument('-o', '--option', type=int, help='Número de la opción deseada (1-10)', required=False)
    parser.add_argument('-i', '--info', action='store_true', help='Muestra información sobre el script seleccionado.')
    parser.add_argument('-r', '--report', action='store_true', help='Genera un reporte de ejecución.')

    args = parser.parse_args()

    # Si se pasa una opción por argumentos, ejecuta esa opción
    if args.option is not None:
        if args.info:
            print(f"Información sobre la opción {args.option}: {args.option} - {commands.get(args.option)}")
        execute_module(args.option)
    else:
        # Muestra el menú y solicita la opción si no se pasa como argumento
        while True:
            show_menu()
            try:
                option = int(input("Ingrese el número de la opción deseada: "))
                if option == 0:
                    print("Saliendo del programa...")
                    break
                execute_module(option)
            except ValueError:
                print("Por favor, ingrese un número válido.")  # Manejo de errores de entrada
            except Exception as e:
                print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
