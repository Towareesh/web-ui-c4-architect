# run.ps1 - Запуск бэкенда и фронтенда

# Переходим в папку backend и запускаем Python-приложение
Write-Host "Запуск бэкенда..." -ForegroundColor Green
Set-Location -Path ".\backend"
# Start-Process -NoNewWindow -FilePath "python" -ArgumentList "app.py" -PassThru

# Возвращаемся в корень и переходим в frontend, запускаем npm run dev
Write-Host "Запуск фронтенда..." -ForegroundColor Green
Set-Location -Path "..\"
# Start-Process -NoNewWindow -FilePath "npm" -ArgumentList "run", "dev" -PassThru

Write-Host "Оба сервера запущены!" -ForegroundColor Cyan