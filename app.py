from flask import Flask, render_template, request, redirect 
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = '110-104-541'
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
toolbar = DebugToolbarExtension(app)


@app.route("/")
def root():
    return render_template("root.html")
if __name__ == '__main__':
    app.run()