import app
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from datetime import date


class ListForm(FlaskForm):
    title = StringField(label="Title:", validators=[DataRequired(message="Title is a required field.")])
    description = TextAreaField(label = "Description: ")
    due_by_date = DateField(label = "Due By:", default=date.today())
    completed = BooleanField(label = "Completed")
    submit = SubmitField("Submit")

    """
        Αυτή η συνάρτηση, την έχουμε κάνει για να ελέγξουμε την τιμή της ημερομηνίας που καταχωρεί ο χρήστης.
        Για να φτιάξουμε μια συνάρτηση για μόνο ένα πεδίο, αρκεί να την ονομάσουμε validate_{το όνομα του πεδίου όπως ακριβώς έχει οριστεί από πάνω}
    """
    
    def validate_due_by_date(form,field):
        if field.data < date.today():
            raise ValidationError("Due by date must be after today")
        
