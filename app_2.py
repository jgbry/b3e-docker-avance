from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>🐱 Yo depuis mon app !</h1>
        <img src="https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif" alt="cat gif">
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)