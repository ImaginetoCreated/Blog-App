from datetime import date
from flask import render_template, url_for, request, flash
from flask_login import current_user, login_required, login_user, logout_user
from website.forms import CreatePostForm, RegistrationForm, LoginForm, CommentForm, ContactForm
from website import create_app, DB_NAME, DB_Blogs
from website.models import BlogPost, User, Comments
from website.security import hash, check_hashed_password
from website.clean_ckeditor import strip_invalid_html
from functools import wraps
from flask import redirect, abort
from website.contact import Contact


base_app = create_app()
app = base_app[0]
user = base_app[2]
db = base_app[1]
BlogPost = BlogPost
blogs = BlogPost()
comments = Comments()

# TODO: Configure Flask-Login



# TODO: Use Werkzeug to hash the user's password when creating a new user.
# hashing a password provided by user

# Todo - create an admin decorator called '@admin_only'
# Admin decorator function
def admin_only(f):
    @wraps(f)
    def check_access(*args,**kwargs):
        if current_user.id != 1:
            abort(404)
        return f(*args,**kwargs)
    return check_access

# HTML Routes
@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        form = RegistrationForm()
        email = form.email.data
        # determine if user exists already with email
        site_user = user.query.filter_by(email=email).first()
        if site_user:
            # print(site_user.id)
            flash("You already have an account with that email. Please login")
            print("first condition reached - failed sign in")
            return redirect(url_for("login"))
        if form.validate_on_submit():
            with app.app_context():
                new_user = User(
                    email=email,
                    password=hash(form.password.data),
                    name=form.name.data
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=RegistrationForm())


# TODO: Retrieve a user from the database based on their email.
@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        form = LoginForm()
        email = form.email.data
        password = form.password.data
        # find the user
        user = User.query.filter_by(email=email).first()
        # check if the user exists
        # take password, hash it , and compare to hashed password
        if not user:
            error = True
            flash("Email not found. Please re-enter your email or register to sign up.")
            return render_template('login.html',form=LoginForm(), error=error)
        elif not check_hashed_password(user.password,password):
            error = True
            flash('You entered the wrong password, please try again')
            # login user and create session
            return render_template('login.html', form=LoginForm(), error=error)
    # if above user is valid and password matches, login user, continue to main page
        login_user(user, remember=True)
        return redirect(url_for('get_all_posts',logged_in=current_user.is_authenticated))
    return render_template("login.html", form=LoginForm(), error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def get_all_posts():
    # # below should work but doesn't
    # result = db.session.execute(db.select(BlogPost))
    # posts = result.scalars().all()

    # alternative code
    posts = blogs.get_all_blogs()
    for post in posts:
        print(post)
    user_id = current_user.id
    return render_template("index.html", all_posts=posts, user_id =user_id)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=['GET','POST'])
@login_required
def show_post(post_id):
    print(DB_NAME)
    requested_post = db.get_or_404(BlogPost, post_id)
    commentary = comments.get_all_comments(post_id)
    if request.method == 'POST':
        form = CommentForm()
        text = form.body.data
        if form.validate_on_submit():
            new_comment = Comments(
                user_id=current_user.id,
                post_id=post_id,
                text=strip_invalid_html(text),
                commenter=current_user,
                post=requested_post
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("show_post", post_id=post_id))
    return render_template("post.html", post=requested_post, form=CommentForm(), comments=commentary)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=strip_invalid_html(form.body.data),
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = strip_invalid_html(edit_form.body.data)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['POST','GET'])
def contact():
    if request.method == 'POST':
        form = ContactForm(
            name=request.form["name"],
            email_address=request.form["email"],
            phone_number=request.form["phone"],
            message=strip_invalid_html(request.form["message"])
        )
        # if form.validate_on_submit():
        email = Contact(
            form_name=form.name.data,
            form_email=form.email_address.data,
            form_phone=form.phone_number.data,
            form_message=form.message.data
        )
        email.send_message()
        flash('You sent a message!!')
        redirect(url_for('about'))
    return render_template("contact.html", form=Contact)


if __name__ == "__main__":
    app.run(debug=False, port=5002)
