from flask import Flask, render_template, request, redirect 
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

responses = []

@app.route("/")
def root():
    return render_template("root.html")

@app.route("/questions/<int:question_id>", methods=['GET', 'POST'])
def question(question_id):
    survey = surveys['satisfaction']
    if question_id >= len(survey.questions):
        return redirect ("/thank_you")
    if request.method == 'POST':
        answer = request.form.get('answer')
        responses.append(answer)
        return redirect(f"/questions/{question_id + 1}")
    else:
        question = survey.questions[question_id]
        return render_template('questions.html', question=question)
    
@app.route("/thank_you")
def thank_you():
    return "Thank you for your answers!"