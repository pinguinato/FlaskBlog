from blog import app, db
from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from blog.models import Post, User
from blog.forms import LoginForm, PostForm


@app.route('/')
@app.route('/posts')
def homepage():
    # i post sono ordinati per data di creazione decrescente  
    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("homepage.html", posts=posts)


@app.route('/posts/<int:post_id>')
def post_details(post_id):
    post_instance = Post.query.get_or_404(post_id) # questo metodo mi permette se chiamo un post che non esiste di andare in 404 e non in None Type
    return render_template("post_details.html", post=post_instance)


@app.route('/about')
def about_page():
    return render_template("about_page.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Username and password non combaciano!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('homepage'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/create-post', methods=["GET", "POST"])
@login_required
def post_create():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, body=form.body.data, description=form.description.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post_details', post_id=new_post.id))
    return render_template("post_editor.html", form=form)

