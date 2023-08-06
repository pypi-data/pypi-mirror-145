from flask import Flask, render_template, render_template_string, request
from flask_migrate import Migrate

from models import UserDatabaseInterfase
from calculation import calculate

import config as settings


app = Flask(__name__)
db = UserDatabaseInterfase(
    settings.DB_USER,
    settings.DB_PASS,
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_NAME
)
migrate = Migrate(app, db)


@app.route('/', methods=['GET'])
def main():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>MathServer</title>
        </head>
        <body>
            <p>Input a string with format: {operator} {num1} {num2}</p>
            <form action="answer" method="POST">
                <input type="text" name="data">
                <input type="submit" value="Calculate">
            </form>
        </body>
        </html>"""
    )


@app.route('/answer', methods=['POST', 'GET'])
def get_answer():
    data = calculate(request.form['data'])
    if isinstance(data, dict):
        db.insert_data(data)
        return data['result']
    else:
        return data


@app.route('/database', methods=['POST', 'GET'])
def get_database():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>MathServer</title>
        </head>
        <body>
            <p>Input integer values of limit and offset (0 = all):</p>
            <form action="database/answer" method="POST">
                <input type="text" name="operator" value="">
                <input type="text" name="limit" value="0">
                <input type="text" name="offset" value="0">
                <input type="submit" value="Send">
            </form>
        </body>
        </html>
        """
    )


@app.route('/database/answer', methods=['POST', 'GET'])
def get_database_by_operator():
    limit = offset = 0
    operator = request.form['operator']
    try:
        limit = int(request.form['limit'])
    except ValueError:
        result = 'Bad values'
    try:
        offset = int(request.form['offset'])
    except ValueError:
        result = 'Bad values'

    result = db.get_data(op=operator, limit=limit, offset=offset)

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>MathServer</title>
        </head>
        <body>
            <div>
                ------------
                {% for dict_item in result_list %}
                    {% for key, value in dict_item.items() %}
                        <p>{{key}}: {{value}}</p>
                    {% endfor %}
                    ------------
                {% endfor %}
            </div>
        </body>
        </html>
        """, 
        result_list=result
    )


def run_server():
    db.create_database()
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    run_server()