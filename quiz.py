from flask import Flask, session, request, redirect, url_for, render_template
from db_scripts import get_question_after, get_quizes, check_answer
from random import shuffle
import os
 
def start_quiz(quiz_id):
    '''створює потрібні значення у словнику session'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def save_answers():
    '''Зберігає відповідь користувача:
    - Отримує відповідь і ID питання з форми.
    - Оновлює останнє питання в сесії.
    - Збільшує загальну кількість запитань.
    - Якщо відповідь правильна (перевірка через `check_answer`), збільшує кількість правильних відповідей.'''
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] 
    if check_answer(quest_id, answer):
        session['answers'] += 1

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
        if request.method == 'POST':
            save_answers()
        # тут поки що стара версія функції:
        result = get_question_after(session['last_question'], session['quiz'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(result)
        
def question_form(question):
    '''Формує сторінку для конкретного питання:
    - Приймає дані питання (`question`) із бази:
        - [0]: ID питання
        - [1]: текст питання
        - [2]: правильна відповідь
        - [3], [4], [5]: неправильні відповіді.
    - Перемішує відповіді у випадковому порядку.
    - Використовує шаблон `test.html` для генерації сторінки.'''
    answers_list = [question[2], question[3], question[4], question[5]]
    shuffle(answers_list)
    return render_template('test.html', question=question[1], quest_id=question[0], answers_list=answers_list)

def result():
    '''Відображає сторінку з результатами вікторини:
    - Використовує шаблон `result.html` для формування результатів.
    - Очищає сесію після завершення.'''
    html = render_template('result.html', right=session['answers'], total=session['total'])
    end_quiz()
    return html
 
 
# Створюємо об'єкт веб-програми:
folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder) 


app.add_url_rule('/', 'index', index, methods=['post', 'get'])   # створює правило для URL '/'
app.add_url_rule('/test', 'test', test, methods=['post', 'get'])
app.add_url_rule('/result', 'result', result) # створює правило для URL'/test'
# Встановлюємо ключ шифрування:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'
 
if __name__ == "__main__":
    # Запускаємо веб-сервер:
    app.run()
