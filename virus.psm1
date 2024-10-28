function Get-VirusTotal {
    param(
        [parameter(mandatory)][string]$key,
        $dic = @{},
        $ve2 = [System.Collections.ArrayList]@(Get-ChildItem -name)
    )

    process {
        foreach ($item in $ve2) {
            $filePath = ".\$item"
            Write-Host "Procesando archivo: $filePath"  # Depuración: archivo procesado
            $fileHash = (Get-FileHash -Path $filePath).Hash
            Write-Host "Hash del archivo: $fileHash"  # Depuración: hash del archivo

            $body = @{
                resource = $fileHash
                apikey   = $key
            }

            try {
                # Invocar el método REST con POST
                $result = Invoke-RestMethod -Method Post -Uri 'https://www.virustotal.com/vtapi/v2/file/report' -Body $body -ContentType 'application/x-www-form-urlencoded'
                Write-Host "Resultado de la API: $($result | ConvertTo-Json)"  # Depuración: resultado de la API

                if ($result.response_code -eq 1) {
                    if ($result.positives -eq 0) {
                        $dic[$item] = 'No se encontró ninguna anomalía'
                    } else {
                        $dic[$item] = "Se encontraron $($result.positives) anomalías"
                    }
                } else {
                    $dic[$item] = 'No funcionó, intenta hacerlo manualmente'
                }
            } catch {
                # Manejar cualquier error durante la solicitud
                $dic[$item] = 'Error al procesar la solicitud'
                Write-Host "Error: $_"  # Depuración: error durante la solicitud
            }
        }

        # Generar el reporte al final de la ejecución
        Generate-Report -results $dic
    }
}

function Generate-Report {
    param (
        [hashtable]$results
    )

    $reportPath = "reporte_virus_total.txt"

    # Crear el reporte
    Add-Content -Path $reportPath -Value "Reporte de VirusTotal"
    Add-Content -Path $reportPath -Value "====================="
    foreach ($key in $results.Keys) {
        Add-Content -Path $reportPath -Value "$key: $($results[$key])"
    }

    Write-Host "Reporte generado en '$reportPath'."
}

function main {
    # Solicitar la clave API
    $apiKey = Read-Host "Introduce tu clave API de VirusTotal"
    $result = Get-VirusTotal -key $apiKey
    $result | Format-Table -AutoSize
}

main
