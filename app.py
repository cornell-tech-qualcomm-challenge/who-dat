from flask import Flask
from flask import request
from datetime import datetime
from flask_pymongo import PyMongo
from flask import request
from flask import jsonify

import json
import requests as requester


import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

_BASE_URL_ = 'http://api.kairos.com/'
_APP_KEY_ = '582019432e7dee645075ab35276367bc'
_APP_ID_ = 'fcca8995'
_CONTENT_TYPE_ = 'application/json'
_GALLERY_NAME_ = 'WHODATTEST'

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
    <p>It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400" />
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


#@app.route('/enroll',methods=['POST'])
def enroll(imageUrl, subjectId):
	data = request.get_json();
	if(imageUrl and subjectId):
		body = {}
		body['image'] = imageUrl	
		body['subject_id'] = subjectId
		body['gallery_name'] = _GALLERY_NAME_

		print(body)

		headers = {}
		headers['app_id'] = _APP_ID_
		headers['app_key'] = _APP_KEY_
		headers['Content-Type'] = _CONTENT_TYPE_

		print(headers)

		r = requester.post(_BASE_URL_+'enroll', json = body, headers = headers)
		print(r.content)
		if(r.content['face_id']):
			return True
		else:
			return False
	else:
		return False
		


	

@app.route('/send-to-kairos')
def recognize():
	print('recognize')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

