import io
from io import StringIO
import csv
import pandas as pd
import numpy as np
import pickle
from config import FLASK_MODEL_PATH,PREDICT_ID_FLASK,FLASK_COLS

from flask import (
    Flask,
    g,
    redirect,
    make_response,
    render_template,
    request,
    session,
    url_for
)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='User', password='password1'))
          
app = Flask(__name__, static_url_path='', 
            static_folder='Flask_templates/static',
            template_folder='Flask_templates')

app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('form'))

        return redirect(url_for('login'))

    return render_template('login.html')

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route("/")
def form():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("base.html")

@app.route('/FLASK')
def form2():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("FLASK.html")

@app.route('/SAVE_RESULTS_PAGE')
def form3():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("SAVE_RESULTS_PAGE.html")

@app.route('/FLASK', methods=["POST"])
def transform_view():
    f = request.files['data_file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    print(csv_input)
    stream.seek(0)
    result = transform(stream.read())

    df = pd.read_csv(StringIO(result))
    df = df[list(FLASK_COLS)]

    # load the model from disk
    loaded_model = pickle.load(open(FLASK_MODEL_PATH, 'rb'))
    
    #Make predictions
    PredcitionsPCT = loaded_model.predict_proba(df.drop(list(PREDICT_ID_FLASK),axis=1))
    df = pd.concat([df[list(PREDICT_ID_FLASK)],round(pd.DataFrame(PredcitionsPCT)[1],2)],axis=1)

    COLS = PREDICT_ID_FLASK + ('Predictions',)
    df.columns = [list(COLS)]
    
    #Process results as a HTML table.
    table_df = df.to_html(index=False)
    Testeting = True

    return render_template("FLASK.html", table=table_df) #,response

@app.route('/SAVE_RESULTS_PAGE', methods=["POST"])
def SAVE_RESULTS():
    f = request.files['data_file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    print(csv_input)
    stream.seek(0)
    result = transform(stream.read())

    df = pd.read_csv(StringIO(result))
    df = df[list(FLASK_COLS)]

    # load the model from disk
    loaded_model = pickle.load(open(FLASK_MODEL_PATH, 'rb'))
    
    #make predictions.
    PredcitionsPCT = loaded_model.predict_proba(df.drop(list(PREDICT_ID_FLASK),axis=1))
    
    #Results dataframe.
    df = pd.concat([df[list(PREDICT_ID_FLASK)],round(pd.DataFrame(PredcitionsPCT)[1],2)],axis=1)

    COLS = PREDICT_ID_FLASK + ('Predictions',)
    df.columns = [list(COLS)]

    response = make_response(df.to_csv(index=False))
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"

    return response

@app.route('/sign_out')
def sign_out():
    session.pop('user_id')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=False,port=8080)