from flask import Flask, session, request, redirect, url_for, render_template
from db_scripts import get_question_after, get_quizes
import os
 
def start_quiz(quiz_id):
    '''створює потрібні значення у словнику session'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
 
def end_quiz():
    session.clear()

def quiz_form():
    q_list = get_quizes()
    return render_template('start.html', q_list=q_list)
       
def index():
    ''' Перша сторінка: якщо прийшли запитом GET, то вибрати вікторину,
     якщо POST - то запам'ятати id вікторини та відправляти на запитання
'''
    if request.method == 'GET':
        # вікторина не обрана, скидаємо id вікторини та показуємо форму вибору
        start_quiz(-1)
        return quiz_form()
    else:
        # отримали додаткові дані у запиті! Використовуємо їх:
        quest_id = request.form.get('quiz') # вибраний номер вікторини 
        start_quiz(quest_id)
        return redirect(url_for('test'))
 
def test():
    '''повертає сторінку питання'''
    # якщо користувач без вибору вікторини пішов відразу на адресу '/test'? 
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        # тут поки що стара версія функції:
        result = get_question_after(session['last_question'], session['quiz'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            session['last_question'] = result[0]

            return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'
 
def result():
    end_quiz()
    return "that's all folks!"
 
# Створюємо об'єкт веб-програми:
folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder) 


app.add_url_rule('/', 'index', index)   # створює правило для URL '/'
app.add_url_rule('/index', 'index', index, methods=['post', 'get']) # правило для '/index' 
app.add_url_rule('/test', 'test', test) # створює правило для URL '/test'
app.add_url_rule('/result', 'result', result) # створює правило для URL'/test'
# Встановлюємо ключ шифрування:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'
 
if __name__ == "__main__":
    # Запускаємо веб-сервер:
    app.run()
