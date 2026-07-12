# ============================
# TotoFra Launcher Avanzato
# ============================

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logFile = "logs\totofra_$timestamp.log"
$backupDir = "output_storico\$timestamp"

# Crea cartelle se non esistono
if (!(Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" | Out-Null }
if (!(Test-Path "output_storico")) { New-Item -ItemType Directory -Path "output_storico" | Out-Null }

Write-Host "=== TotoFra Launcher ===" -ForegroundColor Cyan
Write-Host "Inizio esecuzione: $timestamp" -ForegroundColor Yellow

# Backup output precedente
if (Test-Path "output") {
    Copy-Item "output" $backupDir -Recurse
    Write-Host "Backup output precedente → $backupDir" -ForegroundColor DarkGray
}

# Esecuzione del motore
Write-Host "Esecuzione main.py..." -ForegroundColor Green
try {
    python main.py 2>&1 | Tee-Object -FilePath $logFile
    Write-Host "Esecuzione completata." -ForegroundColor Green
}
catch {
    Write-Host "Errore durante l'esecuzione di TotoFra." -ForegroundColor Red
    $_ | Tee-Object -FilePath $logFile
}

# Copia risultati nel log
Write-Host "Log salvato in: $logFile" -ForegroundColor DarkGray

# Notifica finale
Write-Host "=== TotoFra completato ===" -ForegroundColor Cyan
Write-Host "Risultati aggiornati in /output (sincronizzati sul telefono)" -ForegroundColor Yellow
