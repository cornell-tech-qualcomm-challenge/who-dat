from flask import Flask
from datetime import datetime
from flask_pymongo import PyMongo
from flask import request
from flask import jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://heroku_hss4cbmf:l9om2njf67q23vsloq9t394jk8@ds135444.mlab.com:35444/heroku_hss4cbmf'

mongo = PyMongo(app)

cloudinary.config( 
  cloud_name = "djv82dqoq", 
  api_key = "964894861133628", 
  api_secret = "lkG3LIbSpZbCxU5KPyD8DqFi3LI" 
)

@app.route('/')
def homepage():
    #the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>

    """

@app.route('/signup', methods=['POST'])
def signuppage():
    return render_template('index.html')

@app.route('/submit-signup', methods=['POST'])
def submitsignup():
    users = mongo.db.users
    #print(request.form['name'],request.form['linkedin'])
    #name = request.form['name']
    linkedin = request.form['linkedin']
    imagefile = request.files['imagefile']
    img_resp = cloudinary.uploader.upload(imagefile)
    img_url = img_resp['url']
    user_id = users.insert({'linkedin': linkedin,'img_url':img_url})
    return jsonify({'result' : '200'})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)