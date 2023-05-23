from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from forms import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to_do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# secret key for sessions (signed cookies). Flask uses it to protect the contents of the user session against tampering.
app.config["SECRET_KEY"] = '\xfc\x1a\x1b\x91G\x97E\xceb\xaa\x15\xa8u\x86\xaf\x13\x9fm\x1e\xbb\x85\t'
# token for csrf protection of forms.
app.config["WTF_CSRF_SECRET_KEY"] = '\xfc\x1a\x1b\x91G\x97E\xceb\xaa\x15\xa8u\x86\xaf\x13\x9fm\x1e\xbb\x85\t'
db = SQLAlchemy(app)


# To-do Model
class ListModel(db.Model):
    pass

# End of To-do Model


class TasksModel(db.Model):
    pass

# Tasks Model


# End of Tasks Model

with app.app_context():
    db.create_all()


# Home route
def lists():
    pass


# Route to the List
def print_list(list_title):
    pass


# Route to display the new to-do form and to handle the inputs
def new_list():
    pass


# Route to update an existing todo
def update_list(list_id):
    pass


# Route to delete a specific todo
def delete_list(list_id):
    pass


"""
#FUnction to edit the main atributes of a list
@app.route('/lists/<int:list_id>/edit', methods=['GET', 'POST'])
def edit_list_form(list_id):
    listform = ListForm()
    try:
        if (request.method == 'POST' and listform.validate_on_submit()):
            newlist = listform.__dict__
            list = ListModel.query.get(list_id)
            list.title = newlist['title'].data
            list.description = newlist['description'].data
            list.due_by=newlist['due_by_date'].data
            list.completed = newlist['completed'].data
            db.session.add(list)
            db.session.commit()
            return redirect(url_for('lists'))
        
        list = ListModel.query.get(list_id)
        listform.title.data = list.title
        listform.description.data = list.description
        listform.due_by_date.data = list.due_by
        listform.completed.data = list.completed
        return render_template('edit_list.html', form=listform)
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for('lists'))


#Add a task to a list
@app.route('/<list_id>/add', methods=['POST'])
def add_task(list_id):
    task = TasksModel(title=request.form['title'], list_id=list_id)
    print(list_id)
    print(task)
    db.session.add(task)
    db.session.commit()
    list = db.one_or_404(db.select(ListModel).filter_by(id=list_id))
    return redirect(url_for('print_list', list_title=list.title))


#Function to handle the completed checkbox of task
@app.route('/<task_id>',methods=['POST'])
def check_task(task_id):
    try:
        task = TasksModel.query.get(task_id)
        if request.form.get('completed', '') == "on":
            print(request.form.get('completed', ''))
            task.completed = True
        else:
            task.completed = False
        db.session.add(task)
        db.session.commit()
        return '',204
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for('lists'))
"""
