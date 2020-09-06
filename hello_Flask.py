from flask import Flask#Импортирование класса Flask из модуля flask

from search import search4letters

app = Flask(__name__)  #Создание объекта и присвание его переменной app

@app.route('/')#Декоратор с URL
def hello() ->str: #Стандартная функция
    return 'Hello world from Flask!'

@app.route('/123')
def do_search() ->str:
    return str(search4letters('life,the universe, and everything','eiru,!'))
app.run() #Запуск веб сервера