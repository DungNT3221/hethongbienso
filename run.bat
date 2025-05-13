@echo off
echo Starting Hệ thống quản lý biển số xe...

echo Starting Docker containers...
docker-compose up -d
timeout /t 5 > nul

echo.
echo Services:
echo - Frontend: http://localhost:8080
echo - API Gateway: http://localhost:3000
echo - Auth Service: http://localhost:3001
echo - Vehicle Service: http://localhost:3002
echo.
echo Please open http://localhost:8080/index.html in your browser
echo.
echo Thông tin đăng nhập:
echo - Admin: username: admin, password: admin123
echo - Police: username: police, password: police123
echo.
echo Database information:
echo - Auth Database: localhost:13306, user: auth_user, password: auth_password
echo - Vehicle Database: localhost:13307, user: vehicle_user, password: vehicle_password
echo.
echo Press any key to stop the server...
pause > nul

echo Stopping all services...
docker-compose down
echo All services stopped!
