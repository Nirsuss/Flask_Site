from flask import Flask, render_template, request, escape #Импортирование класса Flask из модуля flask
import mysql.connector
from search import search4letters
app = Flask(__name__)  #Создание объекта и присвание его переменной app
dbconfig = {'host': '127.0.0.1',
                          'user': 'vsearh',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB', }#Словарь с параметрами соедининения
def log_request(req: 'flask_request', res: str) -> None:
    """Журналирует веб-запрос и возвращает результаты"""
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert into log
        (phrase, letters, ip, browser_string, results)
        values
        (%s, %s, %s, %s, %s)"""#Создание строки с текстом запроса для записи в BD
    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res, ))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/123', methods=['POST'])
def do_search() ->'html':
    phrase = request.form['phrase']
    letters =  request.form['letters']
    title = 'Твои результаты: '
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('Result.html', the_phrase=phrase, the_letters=letters, the_results=results, the_title=title,)

@app.route('/')#Декоратор с URL

@app.route('/entry')
def entry_pages() ->'html':
    return render_template('entry.html', The_Title='Welcome to search4letters on the web! ')

@app.route('/viewlog')#Просмотр лог файла в браузере
def view_the_log() ->'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Result')
    return  render_template('viewlog.html',
                            The_Title='View Log',
                            the_row_titles=titles,
                            the_data=contents,)
logged_in = False
if __name__ == '__main__':#Заготовка под pythonanywhere
    app.run(debug=True)