@echo off
call env\Scripts\activate
py manage.py runserver 0.0.0.0:2001
pause