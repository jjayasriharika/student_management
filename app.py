from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import StudentForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False  # CSRF disabled
app.config['SECRET_KEY'] = 'harika'

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    query = request.args.get('q')
    if query:
        students = Student.query.filter(
            (Student.name.ilike(f'%{query}%')) |
            (Student.roll.ilike(f'%{query}%')) |
            (Student.class_name.ilike(f'%{query}%'))
        ).all()
    else:
        students = Student.query.all()
    return render_template('index.html', students=students, query=query)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Student(
            name=form.name.data,
            roll=form.roll.data,
            class_name=form.class_name.data,
            email=form.email.data
        )
        db.session.add(new_student)
        db.session.commit()
        flash("Student added successfully!", "success")
        return redirect(url_for('home'))
    return render_template('add.html', form=form)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        flash("Student updated successfully!", "info")
        return redirect(url_for('home'))
    return render_template('update.html', form=form)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "danger")
    return redirect(url_for('home'))

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)