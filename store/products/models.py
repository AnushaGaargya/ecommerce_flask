from store import db
from datetime import datetime


class AddProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable = False)
    desc = db.Column(db.Text, nullable=False)
    mftr_date = db.Column(db.Date, nullable=False)
    exp_date = db.Column(db.Date, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('posts', cascade="all, delete-orphan",lazy=True))

    image = db.Column(db.String(150), nullable=True)
    # image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    # image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')


    def __repr__(self):
        return '<AddProduct %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30),nullable=False,unique=True)

db.create_all()