Set-StrictMode -Version Latest

# Funciones para revisar el uso de recursos del sistema

function Get-UsoMemoria {
    $memoria = Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
    [PSCustomObject]@{
        'Memoria Total (MB)'   = [math]::round($memoria.TotalVisibleMemorySize / 1KB, 2)
        'Memoria Libre (MB)'   = [math]::round($memoria.FreePhysicalMemory / 1KB, 2)
        'Memoria Usada (MB)'   = [math]::round(($memoria.TotalVisibleMemorySize - $memoria.FreePhysicalMemory) / 1KB, 2)
    }
}

function Get-UsoDisco {
    Get-PSDrive -PSProvider FileSystem | Select-Object Name, Used, Free, 
        @{Name='Total (GB)'; Expression={[math]::round(($_.Used + $_.Free) / 1GB, 2)}}, 
        @{Name='Usado (GB)'; Expression={[math]::round($_.Used / 1GB, 2)}}, 
        @{Name='Libre (GB)'; Expression={[math]::round($_.Free / 1GB, 2)}}
}

function Get-UsoProcesador {
    $totalCPU = (Get-Process | Measure-Object -Property CPU -Sum).Sum
    [PSCustomObject]@{
        'TotalCPUTime (s)' = [math]::round($totalCPU, 2)
    }
}

function Get-UsoRed {
    Get-NetAdapterStatistics | Select-Object Name, ReceivedBytes, SentBytes, 
        @{Name='Recibido (MB)'; Expression={[math]::round($_.ReceivedBytes / 1MB, 2)}}, 
        @{Name='Enviado (MB)'; Expression={[math]::round($_.SentBytes / 1MB, 2)}}
}

# Llamadas a las funciones y generación de reporte

function main {
    $reporte = "reporte_recursos.txt"  # Ruta del archivo de reporte

    # Inicializar el contenido del reporte
    $reporteContent = "===== Uso de Memoria =====`n"
    $memoria = Get-UsoMemoria
    $reporteContent += $memoria | Out-String

    $reporteContent += "`n===== Uso de Disco =====`n"
    $disco = Get-UsoDisco
    $reporteContent += $disco | Out-String

    $reporteContent += "`n===== Uso del Procesador =====`n"
    $cpu = Get-UsoProcesador
    $reporteContent += $cpu | Out-String

    $reporteContent += "`n===== Uso de la Red =====`n"
    $red = Get-UsoRed
    $reporteContent += $red | Out-String

    # Mostrar en consola
    Write-Host $reporteContent

    # Guardar el reporte en un archivo
    $reporteContent | Out-File -FilePath $reporte -Encoding utf8
    Write-Host "Reporte generado en $reporte"
}

main
