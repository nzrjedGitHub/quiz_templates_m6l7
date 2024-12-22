# questions = [
#     ('Яка тварина є найбільшим сухопутним ссавцем?', 'Слон', 'Жирафа', 'Ведмідь', 'Конь'),
#     ('Яка тварина є символом Австралії?', 'Кенгуру', 'Коала', 'Ему', 'Пінгвін'),
#     ('Яка тварина може спати до 20 годин на день?', 'Лев', 'Коала', 'Мишка', 'Зебра'),
#     ('Яка тварина відома своєю здатністю змінювати колір?', 'Хамелеон', 'Змія', 'Жаба', 'Летючий дракон'),
#     ('Яка тварина є найбільшим морським ссавцем?', 'Кит', 'Акула', 'Дельфін', 'Морж'),
#     ('Яка тварина може літати, але не є птахом?', 'Летюча миша', 'Кажан', 'Крилатий змій', 'Комар')
# ]


import sqlite3
db_name = 'quiz.sqlite'
conn = None
curor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' видаляє всі таблиці '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

    
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')


    do('''CREATE TABLE IF NOT EXISTS quiz (
           id INTEGER PRIMARY KEY,
           name VARCHAR)''')
    
    do('''CREATE TABLE IF NOT EXISTS question (
               id INTEGER PRIMARY KEY,
               question VARCHAR,
               answer VARCHAR,
               wrong1 VARCHAR,
               wrong2 VARCHAR,
               wrong3 VARCHAR)''')
    
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
               id INTEGER PRIMARY KEY,
               quiz_id INTEGER,
               question_id INTEGER,
               FOREIGN KEY (quiz_id) REFERENCES quiz (id),
               FOREIGN KEY (question_id) REFERENCES question (id) )''')
    close()

def add_questions():
    questions = [
    ('Яка тварина є найбільшим сухопутним ссавцем?', 'Слон', 'Жирафа', 'Ведмідь', 'Конь'),
    ('Яка тварина є символом Австралії?', 'Кенгуру', 'Коала', 'Ему', 'Пінгвін'),
    ('Яка тварина може спати до 20 годин на день?', 'Лев', 'Коала', 'Мишка', 'Зебра'),
    ('Яка тварина відома своєю здатністю змінювати колір?', 'Хамелеон', 'Змія', 'Жаба', 'Летючий дракон'),
    ('Яка тварина є найбільшим морським ссавцем?', 'Кит', 'Акула', 'Дельфін', 'Морж'),
    ('Яка тварина може літати, але не є птахом?', 'Летюча миша', 'Кажан', 'Крилатий змій', 'Комар')
]
    open()
    cursor.executemany('''INSERT INTO question
                        (question, answer, wrong1, wrong2, wrong3)
                        VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()

def add_quiz():
    quizes = [
        ('Своя гра', ),
        ('Хто хоче стати мільйонером?', ),
        ('Найрозумніший', )
    ]
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()

def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    cursor.execute(query, [1, 1])
    cursor.execute(query, [1, 2])
    cursor.execute(query, [1, 3])
    cursor.execute(query, [2, 3])
    cursor.execute(query, [3, 1])
    cursor.execute(query, [3, 2])
    conn.commit()
    # answer = input("Додати зв'язок (y / n)?")
    # while answer != 'n':
    #     quiz_id = int(input("id вікторини: "))
    #     question_id = int(input("id питання: "))
    #     cursor.execute(query, [quiz_id, question_id])
    #     conn.commit()
    #     answer = input("Додати зв'язок (y / n)?")
    close()
    
def get_all_questions_for_quiz(quiz_id):
    """
    Повертає список всіх питань для конкретної вікторини за її quiz_id
    """
    open()  # Відкриваємо підключення до бази даних
    query = '''
    SELECT quiz_content.id, question.question, question.answer 
    FROM quiz_content, question
    WHERE quiz_content.question_id == question.id 
    AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id
    '''
    cursor.execute(query, (quiz_id,))  # Підставляємо quiz_id у запит
    results = cursor.fetchall()  # Отримуємо всі результати
    close()  # Закриваємо підключення до бази
    return results  # Повертаємо список питань

def get_question_after(question_id = 0, quiz_id=1):
    ''' повертає наступне питання після запитання з переданим id
    для першого запитання передається значення за замовчуванням '''
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id '''
    cursor.execute(query, [question_id, quiz_id] )
    result = cursor.fetchone()
    close()
    return result

def get_quizes():
    ''' повертає список вікторин (id, name)
     можна брати тільки вікторини, в яких є питання, але поки що простий    варіант '''
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result


def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
    show_tables()
    quiz1 = get_all_questions_for_quiz(1)
    print(quiz1)

if __name__ == "__main__":
    main()
