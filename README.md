# Как развернуть проект

Скачиваем проект
Необходим питон актуальной версии (3.10.7)
Создаем виртуальное окружение
`python -m venv venv`
Активируем его

- Для windows: `venv\Scripts\activate.bat`
- Для unix: `source venv\Scripts\activate`

Устанавливаем зависимости `pip install -r requirements.txt`

Заходим в папке staff-vtb и запускаем проект: `python3 manage.py runserver`
Пепереходим на `http://localhost:8000/admin`
Логин: `admin`
Пароль `adminadmin`
