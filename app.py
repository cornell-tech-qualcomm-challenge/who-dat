from flask import Flask
from flask import request
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
    print(str(user_id))

    successfullyEnrolled = enroll(img_url, str(user_id))

    return jsonify({'result':successfullyEnrolled})


@app.route('/submit-picture', methods=['POST'])
def submitpicture():
   
	imagefile = request.files['imagefile']
	img_resp = cloudinary.uploader.upload(imagefile)
	img_url = img_resp['url']


	matches = recognize(img_url)

	if(len(matches) != 0):
		users = mongo.db.users
		userId = matches[0]['subject_id']
		userInfo = users.find_one({'_id':ObjectId(userId)})
		return jsonify({'userImage':userInfo.get('img_url'),'linkedin':userInfo.get('linkedin')})
	return 'No Matches'



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
		print(r.status_code)
		if(r.status_code == 200):
			return '200'
		else:
			return '500'
	else:
		return '500'
		


	

def recognize(imageUrl):
	print('recognize')
	if(imageUrl):
		body = {}
		body['image'] = imageUrl	
		body['gallery_name'] = _GALLERY_NAME_

		print(body)

		headers = {}
		headers['app_id'] = _APP_ID_
		headers['app_key'] = _APP_KEY_
		headers['Content-Type'] = _CONTENT_TYPE_

		print(headers)

		r = requester.post(_BASE_URL_+'recognize', json = body, headers = headers)
		if(r.status_code == 200):
			responseJson = r.json()
			print(responseJson)
			return responseJson['images'][0]['candidates']
		return '[]'



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

