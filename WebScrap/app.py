"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import *
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
@app.route('/')
def index():
    return render_template('login.html')
    
@app.route('/log',methods=['POST','GET'])
def log():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '123':
            return render_template('web.html')
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)
 
@app.route('/web',methods=['POST','GET'])
def web():
    url=None
    error=None
    article=''
    if request.method == 'POST':
       url=request.form['url']
       print(url)
       page = requests.get(url)
       soup = BeautifulSoup(page.content, 'html.parser')
       contents= soup.find_all('p')
       for i in contents:
          article = article + ' ' +  i.text
       return render_template('web.html',article=article)
    else :
        error='Invalid URL'
    return render_template('web.html',error=error)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
