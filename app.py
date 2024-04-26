from flask import Flask, render_template, request, redirect, session 
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "110-104-541"


@app.route("/")
def root():
    session['responses'] = []
    return render_template("root.html")

@app.route("/questions/<int:question_id>", methods=['GET', 'POST'])
def question(question_id):
    survey = surveys['satisfaction']
    responses = session.get('responses')
    if responses is None:
        # trying to access question page too soon
        return redirect("/")
    if question_id != len(responses):
        # trying to access questions out of order
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