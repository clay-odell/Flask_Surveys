from flask import Flask, render_template, request, redirect, session, flash 
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        session['responses'] = []
        session['survey_started'] = True
        return redirect ('/questions/0')
    elif 'survey_started' in session and session['survey_started']:
        flash("You have already started the survey.")
        return redirect(f"/questions/{len(session['responses'])}")
    return render_template("root.html")

@app.route("/questions/<int:question_id>", methods=['GET', 'POST'])
def question(question_id):
    survey = surveys['satisfaction']
    responses = session.get('responses')
    if not session.get('survey_started', False):
        flash("You need to start the survey first.")
        return redirect("/")
    if responses is None:
        # trying to access question page too soon
        flash("You are trying to access an invalid question. Please start from the beginning")
        return redirect("/")
    if question_id != len(responses):
        # trying to access questions out of order
        flash("You are trying to access an invalid question. Please answer the questions in order.")
        return redirect(f"/questions/{len(responses)}")
    if question_id == len(surveys['satisfaction'].questions):
        # all questions are answered
        return redirect("/thank_you")    
    if request.method == 'POST':
        answer = request.form.get('answer')
        responses.append(answer)
        session['responses'] = responses
        return redirect(f"/questions/{question_id + 1}")
    else:
        question = surveys['satisfaction'].questions[question_id]
        return render_template('questions.html', question=question)
    
@app.route("/thank_you")
def thank_you():
    return "Thank you for your answers!"