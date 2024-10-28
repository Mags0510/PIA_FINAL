Set-StrictMode -Version Latest

function main {
    param (
        [string]$Path,
        [string]$ReportPath = "reporte_archivos_ocultos.txt"  # Ruta por defecto del reporte
    )

    # Verificar si se proporcionó una ruta
    if ([string]::IsNullOrWhiteSpace($Path)) {
        Write-Error "No se ha proporcionado una ruta válida."
        return
    }

    # Mostrar la ruta proporcionada para verificación
    Write-Host "Ruta proporcionada: $Path"

    # Verificar si la ruta existe
    if (-Not (Test-Path -Path $Path)) {
        Write-Error "La ruta especificada no existe."
        return
    }

    # Buscar archivos ocultos
    $hiddenFiles = Get-ChildItem -Path $Path -Force | Where-Object { $_.Attributes -match "Hidden" }

    if ($hiddenFiles) {
        # Mostrar archivos ocultos en la consola
        $hiddenFiles | ForEach-Object { Write-Output "Archivo oculto: $($_.FullName)" }

        # Generar un reporte
        $hiddenFiles | Select-Object FullName | Out-File -FilePath $ReportPath -Encoding utf8
        Write-Host "Reporte generado en: $ReportPath"
    } else {
        Write-Host "No se encontraron archivos ocultos en la ruta especificada."
    }
}

# Ejemplo de llamada a la función main
# Puedes descomentar la línea siguiente y proporcionar la ruta deseada
# main -Path "C:\ruta\del\directorio"
