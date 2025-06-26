# Запуск бэкенда и фронтенда одновременно
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python app.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"