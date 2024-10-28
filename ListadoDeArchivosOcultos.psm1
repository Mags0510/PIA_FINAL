function main {
    param (
        [string]$Path,
        [string]$ReportPath = "reporte_archivos_ocultos.txt"  # Ruta del archivo de reporte
    )

    if (-Not (Test-Path -Path $Path)) {
        Write-Error "La ruta especificada no existe."
        return
    }

    $hiddenFiles = Get-ChildItem -Path $Path -Force | Where-Object { $_.Attributes -match "Hidden" }

    if ($hiddenFiles.Count -eq 0) {
        Write-Output "No se encontraron archivos ocultos en la ruta especificada."
        return
    }

    # Escribir los resultados en la consola y en el archivo de reporte
    $reportContent = "Archivos ocultos en la ruta: $Path`n`n"
    foreach ($file in $hiddenFiles) {
        $output = "Archivo oculto: $($file.FullName)"
        Write-Output $output
        $reportContent += "$output`n"
    }

    # Guardar el reporte en el archivo
    $reportContent | Out-File -FilePath $ReportPath -Encoding utf8
    Write-Output "Reporte generado en $ReportPath"
}

Export-ModuleMember -Function main
