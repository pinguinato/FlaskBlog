from blog import app
from flask import render_template
from blog.models import Post


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

