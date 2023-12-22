from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, IntegerField
from wtforms.validators import DataRequired, URL, Length, Email, ValidationError
from flask_ckeditor import CKEditorField





# Custom Validators
def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)

    def _length(form, field):
        # if field.data is not Empty, return length of field.data
        # otherwise return 0.
        l = field.data and len(field.data) or 0
        # if l is less than min - or l is >= max, raise validation error
        if l < min or max != -1 and l > max:
            raise ValidationError(message)

    return _length

def validate_password(message):
    def _validate(form,field):
        if form.password.data != field.data:
            raise ValidationError(message)
    return _validate


# class MyForm(Form):
#     name = StringField('Name', [InputRequired(), length(max=50)])


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class RegistrationForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email = EmailField("Email",validators=[DataRequired(), Email(), Length(min=6,max=125)])
    password = PasswordField("Password",validators=[DataRequired(),length(6,100)])
    verify_password = PasswordField("Verify Password",validators=[DataRequired(), Length(min=6,max=30), validate_password(message="Password doesn't match")])
    submit = SubmitField("Register")

# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = EmailField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")

# TODO: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    body = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")

# TODO: Create a Contact Form for users to reach out
class ContactForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email_address = EmailField("Email Address",validators=[DataRequired(), Email(), Length(min=6,max=125)])
    phone_number = StringField("Phone Number",validators=[DataRequired(),Length(min=10, max=12)])
    message = CKEditorField("Message", validators=[DataRequired()])
