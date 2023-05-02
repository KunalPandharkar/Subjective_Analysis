from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import os
import os,io
from google.cloud import vision_v1
import string
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import re
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/subjective_analysis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database object
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll = db.Column(db.String(30))
    marks = db.Column(db.Integer)
    total_marks = db.Column(db.Integer)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded image file
        uploaded_file = request.files['file']
        image_path = 'static/images/' + uploaded_file.filename
        uploaded_file.save(image_path)

        # Get the standard answer and marks
        standard_answer = request.form['standard_answer']
        marks = int(request.form['marks'])

        #Process Image
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Google_Key.json'
        client = vision_v1.ImageAnnotatorClient()

        with io.open(os.path.join(image_path),'rb') as image_file:
            content = image_file.read()

        image = vision_v1.types.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        # Concatenate only the first item in the texts list
        all_text = texts[0].description if len(texts) > 0 else ''

        all_text = all_text.replace('\n', ' ')

        print(all_text)

        # Using replace() method to remove spaces
        output_str = all_text.replace(" ", "")

        output_str = output_str.lower()
        print(output_str)

        # Using regular expression to extract roll number
        # Using regular expressions to extract roll number, name, and subject
        roll_pattern = r'roll:(\d+)'
        roll_match = re.search(roll_pattern, output_str)
        
        roll_number = 0

        if roll_match:
            roll_number = roll_match.group(1)
        else:
            print("No roll number found in the input string.")

        # Define two sample answers
        answer_1 = str(all_text)
        answer_2 = standard_answer

        # Preprocess the text by removing punctuation and converting to lowercase
        translator = str.maketrans('', '', string.punctuation)
        answer_1 = answer_1.translate(translator).lower()
        answer_2 = answer_2.translate(translator).lower()

        # Tokenize the text by splitting on whitespace
        tokens_1 = nltk.word_tokenize(answer_1)
        tokens_2 = nltk.word_tokenize(answer_2)

        # Create a set of unique tokens
        unique_tokens = set(tokens_1 + tokens_2)

        # Vectorize the text using TF-IDF
        vectorizer = TfidfVectorizer(vocabulary=unique_tokens)
        vectors = vectorizer.fit_transform([answer_1, answer_2]).toarray()

        # Calculate the cosine similarity between the two vectors
        similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]

        # Generate the percentage of correctness
        percentage_correct = similarity * 100
        percentage_correct = round(percentage_correct)

        student_marks = (int(percentage_correct) / 100) * marks

        student_marks = round(student_marks)


        # Insert data into the database
        student = Student(roll=roll_number, marks=student_marks,total_marks=marks)
        db.session.add(student)
        db.session.commit()

        # Generate a pie chart
        labels = ['Correct', 'Incorrect']
        sizes = [int(percentage_correct), 100 - int(percentage_correct)]
        explode = (0.1, 0)
        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal')
        chart_path = 'static/images/chart.png'
        plt.savefig(chart_path)

        # Clear the plot to avoid issues with overlapping images
        plt.clf()

        students = Student.query.all()
        # Render the HTML template with the uploaded image file, textarea, and pie chart
        return render_template('result.html', image_path=image_path, student_marks=student_marks, chart_path=chart_path,total_marks=marks,student_percentage=percentage_correct,roll_number=roll_number)

    return render_template('upload.html')

if __name__ == '__main__':
    # Create the images directory if it doesn't exist
    image_dir = 'static/images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
