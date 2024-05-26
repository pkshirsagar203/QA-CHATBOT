from flask import Flask, request, render_template, flash, redirect, url_for, session
from objective import ObjectiveTest
from subjective import SubjectiveTest
import nltk


nltk.download('punkt')  

app = Flask(__name__)
app.secret_key = 'aica2'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_generate', methods=["POST"])
def test_generate():
    if request.method == "POST":
        inputText = request.form["itext"]
        testType = request.form["test_type"]
        try:
            noOfQues = int(request.form["noq"])  
        except ValueError:
            flash('Number of questions must be an integer.')
            return redirect(url_for('index'))

        if testType == "objective":
            objective_generator = ObjectiveTest(inputText, noOfQues)
            try:
                question_list, answer_list = objective_generator.generate_test()
                testgenerate = zip(question_list, answer_list)
                return render_template('generatedtestdata.html', cresults=testgenerate)
            except Exception as e:
                flash(f'Error generating objective test: {e}')
                return redirect(url_for('index'))

        elif testType == "subjective":
            subjective_generator = SubjectiveTest(inputText, noOfQues)
            try:
                question_list, answer_list = subjective_generator.generate_test()
                testgenerate = zip(question_list, answer_list)
                return render_template('generatedtestdata.html', cresults=testgenerate)
            except Exception as e:
                flash(f'Error generating subjective test: {e}')
                return redirect(url_for('index'))

        else:
            flash('Error Occurred! Invalid test type selected.')
            return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
