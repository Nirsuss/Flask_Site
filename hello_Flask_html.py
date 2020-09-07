from flask import Flask, render_template, request, escape, session #Импортирование класса Flask из модуля flask
from DBcm import UseDatabase,ConnectionError
from search import search4letters
from checker import check_logged_in
app = Flask(__name__)  #Создание объекта и присвание его переменной app
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearh',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB', }#Словарь с параметрами соедининения
app.secret_key = 'YouGenius'
@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out'

def log_request(req: 'flask_request', res: str) -> None:
    """Журналирует веб-запрос и возвращает результаты"""
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
                     (phrase, letters, ip, browser_string, results)
                      values
                      (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res,))

@app.route('/123', methods=['POST'])
def do_search() ->'html':

    phrase = request.form['phrase']
    letters =  request.form['letters']
    title = 'Твои результаты: '
    results = str(search4letters(phrase, letters))
    try:
        log_request(request, results)
    except Exception as err:
        print('*****Login failed with this error:', str(err)) #Универсальный обработчик исключений
    return render_template('Result.html', the_phrase=phrase, the_letters=letters, the_results=results, the_title=title,)

@app.route('/')#Декоратор с URL

@app.route('/entry')
@check_logged_in
def entry_pages() ->'html':
    return render_template('entry.html', The_Title='Welcome to search4letters on the web! ')

@app.route('/viewlog')#Просмотр лог файла в браузере
@check_logged_in
def view_the_log() ->'html':
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results
                         from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
            titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                                   The_Title='View Log',
                                   the_row_titles=titles,
                                   the_data=contents, )
    except ConnectionError as err:
        print('Is your DataBase switched on? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'
logged_in = False
if __name__ == '__main__':#Заготовка под pythonanywhere
    app.run(debug=True)