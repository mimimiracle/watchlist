from flaskr.db import query_db
import os
import re

from flask import Flask, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    from . import db
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/userProfile', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def get_profile():
        if request.method == 'GET':
            uid = request.args.get('uid', '')
            print(uid)
            query = 'select * from user where id={}'.format(uid)
            # 获取数据库连接
            result = query_db(query, one=True)
            id = result['id']
            username = result['username']
            password = result['password']

            return {'id': id, 'username': username, 'password': password}

        elif request.method == 'POST':
            name = request.form.get('username')
            password = request.form.get('password')
            query = 'select * from user where username=\'{}\''.format(name)
            print(query)
            result = query_db(query, one=True)
            if password == result['password']:
                return 'login success'
            else:
                return 'wrong username or password'
            


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app