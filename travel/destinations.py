from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Destination, Comment
from .forms import DestinationForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

destbp = Blueprint('destination', __name__, url_prefix='/destinations')

@destbp.route('/<id>')
def show(id):
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))

    commentForm = CommentForm()
    return render_template('destinations/show.html', destination=destination, form=commentForm)

@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type:', request.method)
    form = DestinationForm()
    if form.validate_on_submit():

        db_file_path = check_upload_file(form)

        destination = Destination(name = form.name.data,
                                  description = form.description.data,
                                  image = db_file_path)
        db.session.add(destination)
        db.session.commit()
        print('Successfully created new travel destination', 'success')

        return redirect(url_for('destination.create'))
    return render_template('destinations/create.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/img',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@destbp.route('/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()

    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    if form.validate_on_submit():

        comment = Comment(text=form.text.data, destination=destination, user=current_user)

        db.session.add(comment)
        db.session.commit()

        print(f"The following comment has been posted: {form.text.data}")
    return redirect(url_for('destination.show', id=id))



# def get_destination():
#     #description of Italy
#     italy_desc = "Italy, a mesmerizing country nestled in southern Europe, captivates with its rich tapestry of culture, history, and natural beauty. From the romantic allure of Venice's winding canals and the architectural splendor of Rome's ancient ruins to the culinary delights of pizza, pasta, and gelato, Italy is a sensory journey through the ages. Its artistic heritage, exemplified by Renaissance masterpieces like Michelangelo's David and the timeless elegance of Florence, is a testament to its enduring influence on the world. Surrounded by the Mediterranean Sea, Italy boasts stunning coastlines along the Amalfi and Cinque Terre, while the majestic Alps cradle its northern borders offering breathtaking landscapes for exploration"

#     #image location
#     image_loc = "../static/img/italy.jpg"

#     destination = Destination('Italy', italy_desc, image_loc)

#     #comments
#     comment = Comment("Georno", "oui oui baguette", '2023-08-12 11:00:00')
#     destination.set_comments(comment)
#     comment = Comment("Sally", "Good food", '2023-012-25 1:45:30')
#     destination.set_comments(comment)
#     comment = Comment("Danny", "Very pretty", '2023-02-13 18:02:40')
#     destination.set_comments(comment)
#     return destination