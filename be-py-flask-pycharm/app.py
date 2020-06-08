from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:rootalchemy@localhost/alchemydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)


if __name__ == '__main__':
    from db import db  # Avoiding circular import
    db.init_app(app)

    app.run(host='127.0.0.1', debug=True)
    # app.run(host='127.0.0.1', debug=True, ssl_context=('cert.pem', 'key.pem'))
    # app.run()
