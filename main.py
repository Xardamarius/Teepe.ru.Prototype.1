from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teepy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Websites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_site = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    about = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    q = request.args.get('q')

    if q:
        websites = Websites.query.filter(Websites.title.contains(q) | Websites.about.contains(q))
        return render_template('search.html', data=websites)
    else:
        websites = Websites.query.order_by(Websites.title).all()
    return render_template('index.html')

@app.route('/search')
def search():
    q = request.args.get('q')

    if q:
        websites = Websites.query.filter(Websites.title.contains(q) | Websites.about.contains(q))
        return render_template('search.html', data=websites)
    else:
        websites = Websites.query.order_by(Websites.title).all()

    return render_template('search.html', data=websites)

@app.route('/add-site', methods=['POST', 'GET'])
def add_site():

    if request.method == 'POST':
        title = request.form['title']
        about = request.form['about']
        url_site = request.form['url_site']

        websites = Websites(title=title, about=about, url_site=url_site)

        try:
            db.session.add(websites)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка!"

    return render_template('add-site.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
