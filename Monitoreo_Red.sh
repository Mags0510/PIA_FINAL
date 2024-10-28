# Ruta del reporte
report="reporte_monitoreo.txt"

# Funcion para mostrar el menu
function menu() {
  clear
  echo "Menú de Monitoreo de Red"
  echo "1. Mostrar puertos abiertos en el host local"
  echo "2. Verificar conectividad a hosts"
  echo "3. Detectar dispositivos y conexiones de red con nmcli"
  echo "4. Generar reporte"
  echo "5. Salir"
  read -p "Selecciona una opcion: " opcion
}

# Función para mostrar puertos abiertos en el host local
function Local_Ports() {
  echo "Puertos abiertos en el host local:" | tee -a $report
  netstat -tuln | tee -a $report
}

# Función para verificar conectividad a hosts
function Connectivity() {
  read -p "Ingrese una lista de hosts separados por comas: " hosts
  for host in $(echo $hosts | tr "," "\n"); do
    echo "Verificando conectividad con $host..." | tee -a $report
    ping -c 4 $host | tee -a $report
    echo "" | tee -a $report
  done
}

# Función para detectar dispositivos y conexiones de red usando nmcli
function New_Devices() {
  echo "Conexiones activas y dispositivos de red:" | tee -a $report
  nmcli device status | tee -a $report
  echo "" | tee -a $report
  echo "Lista de dispositivos WiFi detectados (si aplica):" | tee -a $report
  nmcli dev wifi list | tee -a $report
}

# Función para generar un reporte
function Generate_Report() {
  echo "Generando reporte..." 
  echo "Reporte de Monitoreo de Red - $(date)" > $report
  echo "===================================" >> $report
  echo "" >> $report

  Local_Ports
  Connectivity
  New_Devices

  echo "Reporte generado en $report"
}

function main() {
  while true; do
    menu
    case $opcion in
      1)
        Local_Ports
        ;;
      2)
        Connectivity
        ;;
      3)
        New_Devices
        ;;
      4)
        Generate_Report
        ;;
      5)
        echo "Saliendo..."
        return
        ;;
      *)
        echo "Opción inválida"
        ;;
    esac
    read -p "Presiona Enter para continuar..." # Pausa antes de volver al menú
  done
}

main
