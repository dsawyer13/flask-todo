from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '3847290387sadfashjdf89a7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.String(10), nullable=False, default='Low')
    editing = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        todo_content = request.form['task']
        todo_priority = request.form['priority']
        new_todo = Todo(task=todo_content, priority=todo_priority)
        print(todo_content, todo_priority)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding your task'
    else:
        tasks = Todo.query.all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error deleting your task'


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    task_to_edit = Todo.query.get_or_404(id)
    task_to_edit.editing = True

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error editing your task'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    task_to_update.task = request.form['task']
    task_to_update.priority = request.form['priority']
    task_to_update.editing = False
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error updating your task'


@app.route('/cancel/<int:id>', methods=['POST', 'GET'])
def cancel(id):
    task_to_cancel = Todo.query.get_or_404(id)
    task_to_cancel.editing = False

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error canceling your change'


if __name__ == '__main__':
    app.run(debug=True)
