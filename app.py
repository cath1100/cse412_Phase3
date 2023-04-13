from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route('/')
def hello():
    # return '<h1>testing</h1>'
    return render_template('Home.html')

@app.route('/AccountInfo')
def displayInfo():
    return render_template('account.html')

@app.route('/ChangeInfo')
def ChangeInfo():
    return render_template('changeInfo.html')

if __name__ == '__main__':
    app.debug = True
    app.run()