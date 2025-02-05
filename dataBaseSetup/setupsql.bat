@echo off
echo Setting up MariaDB database...
mysql -u root -p1234 < setup.sql
echo Database setup completed!
pause
