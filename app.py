import os
from flask import Flask, render_template, request
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.streamshare

    @app.route('/', methods=['GET', 'POST'])
    def first_page():

        if request.method == 'POST':
            entry = request.form.get('content')

            formatted_date = datetime.datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert({"content": entry, "date": formatted_date})

        entries_with_date = [
            (entry["content"], entry["date"], datetime.datetime.strptime(entry["date"], '%Y-%m-%d').strftime('%b %d'))

            for entry in app.db.entries.find({})
        ]

        return render_template('home.html', entries=entries_with_date)

    return app
