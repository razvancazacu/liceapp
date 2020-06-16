from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rootalchemy@localhost/alchemydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'  # TODO: add security / login
api = Api(app)
admin = Admin(app, template_mode='bootstrap3')
db = SQLAlchemy(app)


class OrareModel(db.Model):
    __tablename__ = 'orare'
    id_orar = db.Column(db.Integer, primary_key=True)
    nume_orar = db.Column(db.String(100))

    def __repr__(self):
        return self.nume_orar


class OrareView(ModelView):
    page_size = 50
    column_searchable_list = ['nume_orar']
    column_filters = ['nume_orar']


class OreModel(db.Model):
    __tablename__ = 'ore'
    id = db.Column(db.Integer, primary_key=True)
    id_orar = db.Column(db.Integer, db.ForeignKey('orare.id_orar'))
    zi = db.Column(db.String(45))
    ora_inceput = db.Column(db.String(45))
    ora_final = db.Column(db.String(45))
    profesor = db.Column(db.String(45))
    materie = db.Column(db.String(45))
    sala = db.Column(db.String(45))
    saptamana = db.Column(db.String(45))
    grupa = db.Column(db.String(45))
    orar = db.relationship('OrareModel', backref='ora_to_orar')


class OreView(ModelView):
    page_size = 50
    column_searchable_list = ('sala', 'materie', 'orar.nume_orar', 'profesor')
    column_filters = ('sala', 'materie', 'orar.nume_orar', 'profesor')


class WarningsModel(db.Model):
    __tablename__ = 'warnings'
    id_warning = db.Column(db.Integer, primary_key=True)
    id_orar = db.Column(db.Integer, db.ForeignKey('orare.id_orar'))
    warning_details = db.Column(db.String(100))
    orar = db.relationship('OrareModel', backref='warning_to_orare')


class WarningsView(ModelView):
    page_size = 50
    column_searchable_list = ('orar.nume_orar', 'warning_details')
    column_filters = ('orar.nume_orar', 'warning_details')


admin.add_view(OrareView(OrareModel, db.session))
admin.add_view(OreView(OreModel, db.session))
admin.add_view(WarningsView(WarningsModel, db.session))

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)

    # app.run(host='127.0.0.1', debug=True, ssl_context=('cert.pem', 'key.pem'))
    # app.run()
