import os
import psycopg
from flask import Flask, request, render_template, redirect, url_for
from markupsafe import escape
from lib.pig_latin import pig_latin

def get_database_url():
  if os.environ.get("APP_ENV") == "PRODUCTION":
    password = os.environ.get("POSTGRES_PASSWORD")
    hostname = os.environ.get("POSTGRES_HOSTNAME")
    return f"postgres://postgres:{password}@{hostname}:5432/postgres"
  else:
    return "postgres://localhost:5432/postgres"

def setup_database(url):
    # We connect using the URL
    connection = psycopg.connect(url)

    # Get a 'cursor' object that we can use to run SQL
    cursor = connection.cursor()

    # Execute some SQL to create the table
    cursor.execute("CREATE TABLE IF NOT EXISTS piglatin (translation TEXT);")

    # And commit the changes to ensure that they 'stick' in the database.
    connection.commit()

POSTGRES_URL = get_database_url()
setup_database(POSTGRES_URL)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_home():
    connection = psycopg.connect(POSTGRES_URL)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM piglatin;")
    rows = cursor.fetchall()
    translations = format_translations(rows)
    return render_template("index.html", translations=translations)

def format_translations(translations):
    output = []
    for translation in translations:
        # We escape the message to avoid the user sending us HTML and tricking
        # us into rendering it.
        escaped_translation = escape(translation[0])
        output.append(escaped_translation)
    return output
  

@app.route('/', methods=['POST'])
def pig_generate():
    string = request.form['sentence']
    if string == "":
      result = "onay inputay"
    else: 
      result = pig_latin(string)
    connection = psycopg.connect(POSTGRES_URL)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO piglatin (translation) VALUES (%s);", (result,))
    connection.commit()
    return render_template("generated_latin.html", result=result)

# @app.route("/result", methods=['POST'])
# def get_latin(result):
#     return render_template("generated_latin.html", result=result)

if __name__ == '__main__':
    if os.environ.get("APP_ENV") == "PRODUCTION":
        app.run(port=5000, host='0.0.0.0')
    else:
        app.run(debug=True, port=5000, host='0.0.0.0')