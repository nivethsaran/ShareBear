import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from deta import Deta
from flask_qrcode import QRcode
import requests

app = Flask(__name__)
jdoodle_url = 'https://api.jdoodle.com/v1/execute'
load_dotenv()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


deta = Deta(os.environ['TOKEN'])
codes = deta.Base("codes")
app.config['SECRET_KEY'] = os.environ['SECRET']
app.register_error_handler(404, page_not_found)
qrcode = QRcode(app)
JDOODLEID = os.environ['JDOODLEID']
JDOODLESECRET = os.environ['JDOODLESECRET']


@app.route('/', methods=["GET", "POST"])
def renderMainPage():
    if request.method == 'GET':
        return render_template('index.html', baseurl=request.base_url)
    else:
        codename = request.form['codename']
        code = request.form['code']
        language = request.form['language']
        input = request.form['input']
        output = request.form['output']
        PIN = ''
        pin_enabled = False
        if 'customSwitch1' in request.form:
            pin_enabled = request.form['customSwitch1'] == 'on'
            PIN = request.form['PIN']
        else:
            pin_enabled = False
        executable = False
        if 'customSwitch2' in request.form:
            executable = request.form['customSwitch2'] == 'on'
        else:
            executable = False

        code_entry = codes.put({
            "name": codename,
            "code": code,
            "pin": PIN,
            "pin_enabled": pin_enabled,
            "executable": executable,
            "input": input,
            "output": output,
            "language": language,

        })

        return redirect(url_for('renderSharedCodes', code_id=code_entry['key']))


def updateCodeName(coderes):
    if coderes['language'] == 'C':
        coderes['name'] = coderes['name'] + '.c'
    elif coderes['language'] == 'Java':
        coderes['name'] = coderes['name'] + '.java'
    elif coderes['language'] == 'C++':
        coderes['name'] = coderes['name'] + '.cpp'
    elif coderes['language'] == 'Python':
        coderes['name'] = coderes['name'] + '.py'
    return coderes


@app.route('/<code_id>', methods=['GET', 'POST'])
def renderSharedCodes(code_id):
    if request.method == "GET":
        print(code_id)
        coderes = codes.get(code_id)
        print('key' in session)
        if coderes is None:
            abort(404, description="Resource not found")
        elif coderes['pin_enabled']:
            if 'key' not in session:
                return render_template('auth.html', code_id=code_id, create=True)
            else:
                session.pop('key', None)
                coderes = updateCodeName(coderes)
                return render_template('code.html', coderes=coderes, baseurl=request.base_url, create=True)
        else:
            print(coderes)
            coderes = updateCodeName(coderes)
            return render_template('code.html', coderes=coderes, baseurl=request.base_url, create=True)
    else:
        print(code_id)
        coderes = codes.get(code_id)
        if coderes is None:
            abort(404, description="Resource not found")
        elif request.form['PIN'] == coderes['pin']:
            coderes = updateCodeName(coderes)
            session['key'] = code_id
            # return render_template('code.html', coderes=coderes, baseurl=request.base_url)
            return redirect(url_for('renderSharedCodes', code_id=code_id))
        else:
            flash('Invalid PIN')
            return render_template('auth.html', code_id=code_id, create=True)


# @app.route('/showAll', methods=['GET'])
# def showAllCodeFromDatabase():
#     return {"codes": next(codes.fetch({}))}
#
#
# @app.route('/deleteAll', methods=['GET'])
# def deleteAllCodeFromDatabase():
#     toDeleteCodes = next(codes.fetch({}))
#     for i in toDeleteCodes:
#         codes.delete(i['key'])
#     return '{"STATUS":"DELETEDALL"}'
#
#
# @app.route('/deleteCode/<key>', methods=["DELETE"])
# def deleteCodeWithKey(key):
#     print(key)
#     print(codes.delete(key))
#     return '{"STATUS":"DELETED"}'


def getExecLanguage(language):
    if language == 'C':
        return 'c'
    elif language == 'Java':
        return 'java'
    elif language == 'Python':
        return 'python3'
    elif language == 'C++':
        return 'cpp14'


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/execute', methods=['POST'])
def execute():
    print(request.form)
    data = {}
    language = getExecLanguage(request.form['language'])
    debug = False
    if JDOODLEID is None or JDOODLEID is None or debug:
        return "Setup Proper API"
    else:
        try:
            data['clientId'] = JDOODLEID
            data['clientSecret'] = JDOODLESECRET
            data['script'] = request.form['code']
            data['stdin'] = request.form['input']
            data['language'] = language
            data['versionIndex'] = 0

            output = requests.post(jdoodle_url, json=data).text
            print(output)
            return json.loads(output)['output'].replace('\n', ' \r\n ')
        except:
            return "Unknown error occured. Please try again later"


if __name__ == '__main__':
    app.run()
