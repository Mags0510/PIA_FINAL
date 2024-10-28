#!/bin/bash

# Ruta del reporte
report="reporte_escaneo.txt"

# Menú
show_menu() {
  clear
  echo "Escaneo de puertos"
  echo "1. Escaneo de puertos locales"
  echo "2. Escaneo rápido"
  echo "3. Escaneo detallado"
  echo "4. Escanear puertos abiertos específicos"
  echo "5. Generar reporte"
  echo "6. Salir"
}

# Función principal para el menú
main() {
  while true; do
    show_menu
    read -p "Elige una opción: " opcion  
    case $opcion in
      1) 
          scan_puertos_local 
          ;;  
      2) 
          scan_fast 
          ;;      
      3) 
          scan_detailed 
          ;;   
      4) 
          scan_puertos_abiertos 
          ;;  
      5) 
          function_report 
          ;;     
      6) 
          echo "Saliendo..."; return
          ;;   
      *) 
          echo "Opción no válida" 
          ;;    
    esac
    read -p "Presiona Enter para continuar"  
  done
}

# Función para realizar el escaneo de puertos locales aquí uso lsof
scan_puertos_local() {
  echo "Mostrando puertos abiertos locales..."
  sudo lsof -i -P -n | grep LISTEN || echo "No se encontraron puertos abiertos."
  echo "Escaneo de puertos locales terminado."
}

# Usando ping podemos hacer un escaneo rápido
scan_fast() {
  local_ip=$(hostname -I | awk '{print $1}')
  read -p "Ponga la IP o dominio a escanear (presione Enter para usar la IP de esta computadora: ${local_ip}): " ip
  ip=${ip:-$local_ip}

  echo "Iniciando el escaneo rápido (ping) en $ip..."
  if ping -c 4 $ip > /dev/null 2>&1; then
      echo "El host $ip está activo."
  else
      echo "El host $ip no está respondiendo."
  fi
  echo "Escaneo rápido terminado."
}

# Crear función para hacer un escaneo detallado de las conexiones usando ss de BASH 
scan_detailed() {
  echo "Mostrando todas las conexiones de red activas (TCP, VPN)..."
  ss -tuln || echo "Error al obtener conexiones."
  echo "Escaneo detallado finalizado."
}

# Función para escanear puertos específicos usando lsof de BASH
scan_puertos_abiertos() {
  puertos_predeterminados=("80" "443" "22")
  read -p "Escribe los puertos específicos separados por comas (dejar vacío para usar predeterminados 80, 443, 22): " puertos_usuario

  while ! [[ "$puertos_usuario" =~ ^[0-9,]*$ ]]; do
      echo "Entrada no válida. Por favor, ingresa solo números separados por comas."
      read -p "Escribe los puertos específicos separados por comas (dejar vacío para usar predeterminados 80, 443, 22): " puertos_usuario
  done

  if [ -z "$puertos_usuario" ]; then
      puertos=("${puertos_predeterminados[@]}")
  else
      IFS=',' read -r -a puertos <<< "$puertos_usuario"
  fi

  echo "Iniciando el escaneo de puertos específicos..."
  for puerto in "${puertos[@]}"; do
      echo "Escaneando puerto $puerto..."
      sudo lsof -i :$puerto -P -n | grep LISTEN || echo "No se encontraron servicios en el puerto $puerto."
  done
  echo "El escaneo de puertos específicos ha terminado."
}

# Crear función para hacer el reporte de la red
function_report() {
  read -p "Ponga el rango de IPs (ejemplo: 192.168.2.): " red
  echo "Haciendo el escaneo de red para la red $red..." > "$report"
  
  for ip in {1..254}; do 
      ping -c 1 -W 1 "${red}$ip" > /dev/null 2>&1
      if [ $? -eq 0 ]; then
          echo "Host activo: ${red}$ip" >> "$report"
      fi 
  done
  echo "Reporte generado en $report"
}

# Iniciar el menú
main
