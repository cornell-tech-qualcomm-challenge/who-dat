from flask import Flask
from flask import request
from datetime import datetime
import json
import requests as requester

app = Flask(__name__)

_BASE_URL_ = 'http://api.kairos.com/'
_APP_KEY_ = '582019432e7dee645075ab35276367bc'
_APP_ID_ = 'fcca8995'
_CONTENT_TYPE_ = 'application/json'
_GALLERY_NAME_ = 'WHODATTEST'


@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)


#@app.route('/enroll',methods=['POST'])
def enroll(imageUrl, subjectId):
	data = request.get_json();
	if(imageUrl && subjectId):
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
		return r.content
	else:
		return 'error'
		


	

@app.route('/send-to-kairos')
def recognize():
	print('recognize')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

