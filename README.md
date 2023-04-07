# ТЕСТОВОЕ ЗАДАНИЕ 

# django-quiz
## Установка
Создайте clone:
```
git clone https://github.com/EXTRAS12/django-quiz.git
```
Перейдите в папку:
cd django-quiz

Создайте виртуальное окружение и запустите:
python3 -m venv venv
source venv/bin/activate

Перейдите в корневой каталог проекта:
``` 
cd quizapp
```

И установите зависимости: 
```
pip install -r requirements.txt
```


Вы можете протестировать возможности проекта на предоставленной **тестовой** базе данных
(**Суперюзер**: Логин:admin Пароль:admin или Логин: guest Пароль: admin)

Для **теста** функционала с тестовой базой данных:
```
python manage.py runserver
```

После подключения **своей или новой** базы данных:
```
python manage.py migrate
python manage.py createsuperuser
```
В случае **ошибки** удалите файл main/migrations/0001_inital.py:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
Или просто запустите команду
```
docker-compose up
