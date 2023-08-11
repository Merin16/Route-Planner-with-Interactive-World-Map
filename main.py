from flask import Flask, request, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Template
from flask import render_template_string
from urllib.parse import quote_plus
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os

app = Flask(__name__)
password = quote_plus('Merin@123')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{password}@localhost:3306/htmldata'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Merin@123@localhost:3306/htmldata'
db = SQLAlchemy(app)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    # add_destination = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_route():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        # add_destination = request.form['additional-destinations']
        ports = request.form.getlist('ports[]')

        new_route = Route(source=source, destination=destination)
        db.session.add(new_route)
        db.session.commit()

        return 'Data saved successfully!'

@app.route('/download', methods=['GET'])
def download_pdf():
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawString(100, 700, "Hello PDF")
    c.showPage()
    c.save()

    pdf_buffer.seek(0)
    print(pdf_buffer.read())  # Print PDF content to console

    response = make_response(pdf_buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=test.pdf'

    return response



if __name__ == '__main__':
    app.run(debug=True)
