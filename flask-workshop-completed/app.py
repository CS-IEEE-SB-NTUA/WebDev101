from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from forms import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# secret key for sessions (signed cookies). Flask uses it to protect the contents of the user session against tampering.
app.config["SECRET_KEY"] = '\xfc\x1a\x1b\x91G\x97E\xceb\xaa\x15\xa8u\x86\xaf\x13\x9fm\x1e\xbb\x85\t'
# token for csrf protection of forms.
app.config["WTF_CSRF_SECRET_KEY"] = '\xfc\x1a\x1b\x91G\x97E\xceb\xaa\x15\xa8u\x86\xaf\x13\x9fm\x1e\xbb\x85\t'
db = SQLAlchemy(app)


# To-do model
class ListModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    due_by = db.Column(db.Date, default=date.today())

    def __repr__(self):
        return f"<List {self.id}: {self.title}>"


class TasksModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey(
        ListModel.id), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.id}: {self.title}>"


with app.app_context():
    db.create_all()


# Home route
@app.route("/")
def lists():
    lists = ListModel.query.order_by(ListModel.id.desc())
    return render_template('lists.html', lists=lists)


# Route to display the new list form and to handle the inputs
@app.route("/lists/new", methods=["GET", "POST"])
def new_list():
    listform = ListForm()
    try:
        if (request.method == "POST" and listform.validate_on_submit()):
            newlistdict = listform.__dict__
            list = ListModel(
                title=newlistdict["title"].data, description=newlistdict["description"].data, due_by=newlistdict["due_by_date"].data)
            db.session.add(list)
            db.session.commit()
            return redirect(url_for("lists"))

        return render_template("new_list.html", form=listform)
    except Exception as e:
        flash(str(e), "danger")
        return render_template("new_list.html", form=listform)


# Route to the List
@app.route("/<list_title>")
def print_list(list_title):
    list = db.one_or_404(db.select(ListModel).filter_by(title=list_title))
    tasks = db.session.scalars(TasksModel.query.filter_by(list_id=list.id))
    return render_template("list.html", list=list, tasks=tasks.all())


# Route to update the completed field
"""
    Το μόνο που κάνουμε σε αυτή τη συνάρτηση, είναι να κάνουμε update την τιμή του completed αν πατήσει ο χρήστης το checkbox στη σελίδα lists.html
"""


@app.route('/lists/<int:list_id>', methods=['PUT', 'POST'])
def update_list(list_id):
    try:
        list = ListModel.query.get(list_id)
        if list:
            completed = request.form.get('completed', '')
            if completed == 'on':
                list.completed = True
            else:
                list.completed = False
            db.session.commit()
            """
                Επιστρέφουμε αυτό, γιατί δεν θέλουμε να αλλάξει η σελίδα μας και το 204 είναι ο κωδικός που στέλνουμε στον client για να ξέρει πως 
                η ενημέρωση έγινε σωστά
            """
            return '', 204
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("lists"))


# Route to delete a specific list

"""
    Για να κάνουμε delete μία λίστα, δεν μας επιτρέπεται by default να την διαγράψουμε αμέσως (άλλος ένας λόγος που χρησιμοποιούμε το ForeignKey). 
    Αυτό συμβαίνει γιατί δεν θέλουμε να παραμείνουν tasks στη βάση μας τα οποία δεν αντιστοιχούν σε λίστα.
    Μπούμε να ορίσουμε τη βάση μας ώστε διαγράφοντας τη λίστα να τα διαγράφει όλα αλλά ο πιο σωστός τρόπος είναι να βρούμε όλα τα tasks
    που ανήκουν στη λίστα μας, να διαγράψουμε αυτά και στο τέλος να διαγράψουμε την ίδια τη λίστα. Προφανώς, αν μία λίστα δεν έχει tasks,
    μπορούμε να τη διαγράψουμε κατευθείαν. 
"""


@app.route("/lists/delete/<int:list_id>", methods=['DELETE', 'POST'])
def delete_list(list_id):
    tasks = TasksModel.query.filter_by(list_id=list_id)
    list = ListModel.query.get(list_id)
    try:
        for task in tasks:
            db.session.delete(task)
        db.session.delete(list)
        db.session.commit()
        return redirect(url_for("lists"))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("lists"))


# Route to display the edit and handle the list form

@app.route('/lists/<int:list_id>/edit', methods=['GET', 'POST'])
def edit_list_form(list_id):
    listform = ListForm()
    try:
        if (request.method == 'POST' and listform.validate_on_submit()):
            newlist = listform.__dict__
            list = ListModel.query.get(list_id)
            """
                Πρώτα, πρέπει να βρούμε την καταχώρηση που θέλουμε να τροποποιήσουμε.
                Μετά, δίνουμε τις καινούργιες τιμές που παίρνουμε από την φόρμα στα πεδία της καταχώρησης και κάνουμε commit ώστε να γίνει
                save η τιμή στη βάση μας. 
            """
            list.title = newlist['title'].data
            list.description = newlist['description'].data
            list.due_by = newlist['due_by_date'].data
            list.completed = newlist['completed'].data
            db.session.commit()
            return redirect(url_for('lists'))
        """
            Θέλουμε να έχουμε προσυμπληρωμένα τα πεδία ώστε να ξέρει ο χρήστης τι τιμές είχαμε από πριν.
            Γι'αυτό, κάνουμε ένα query ώστε να βρόυμε την καταχώρηση και προσθέτουμε τις τιμές τους στα αντίστοιχα πεδία.
        """
        list = ListModel.query.get(list_id)
        listform.title.data = list.title
        listform.description.data = list.description
        listform.due_by_date.data = list.due_by
        listform.completed.data = list.completed
        return render_template('edit_list.html', form=listform)

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for('lists'))


@app.route('/<list_id>/add', methods=['POST'])
def add_task(list_id):
    task = TasksModel(title=request.form['title'], list_id=list_id)
    db.session.add(task)
    db.session.commit()
    list = db.one_or_404(db.select(ListModel).filter_by(id=list_id))
    return redirect(url_for('print_list', list_title=list.title))


@app.route('/<task_id>', methods=['POST'])
def check_task(task_id):
    try:
        task = TasksModel.query.get(task_id)
        if request.form.get('completed', '') == "on":
            task.completed = True
        else:
            task.completed = False
        db.session.commit()
        return '', 204
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for('lists'))


if __name__ == "__main__":
    app.run(debug=True)
