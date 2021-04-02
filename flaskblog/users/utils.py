import os
import secrets

from PIL import Image
from flask import url_for
from flask_mail import Message

from flaskblog import mail, app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    # html form will add the 'filename' attribute to the form_picture value automatically.
    # os.path.split will give two values viz. file_name and file_extension, but here we just want to use the extension, so in python if we donot want to use a variable, we name it as underscore('_') like we did here with filename
    picture_fn = random_hex + f_ext # picture_filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resizing the images to 125 px, else large images will take much space on the file system
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=os.environ.get('EMAIL_USER'),
                  recipients=[user.email])

    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then, simply ignore this message and no changes will be made.'''

    mail.send(msg)


def delete_picture(image_file):
    image_path = os.path.join(app.root_path, 'static/profile_pics', image_file)
    os.remove(image_path)

