from flask import Flask, render_template, request
import geopy
from werkzeug.exceptions import BadRequestKeyError


app=Flask(__name__)

# root/home
@app.route('/')
def home():
	return render_template('home.html')

# Search for scooters
@app.route('/', methods=['GET'])
def search():
	# TODO: Search for scooters and return
	try:
		lat, lng, radius = request.args['lat'], request.args['lng'], request.args['radius']
	except BadRequestKeyError:
		# just redirect home
	# TODO: search for scooters based on lat, lng, radius
	# pseudocode:
	# for each scooter
	# 	if scooter location - specified location <= radius:
	#	  add to list
	# return the list
#	return render_template('home.html')
	return searchResults
	
# Start a reservation 
@app.route('/reservation/start', methods=['POST'])
def start_reservation():
	# TODO: try to reserve a scooter
	return success
#	if success:
#		return render_template('res_start_success.html')
#	else:
#		return render_template('res_start_failure.html')

# End a reservation
@app.route('/reservations/end', methods=['GET'])
def end_reservation():
	if 'id' in request.args:
		id = request.args['id']
		# TODO: try to end a reservation
	else:
		success = False
	
	if success:
		# TODO: calculate distance
		# redirect to payment page
		return redirect(url_for('pay', id=))
	else:
		return render_template('res_end_failure.html')
			
# Pay for a completed reservation
@app.route('/reservation/pay', methods=['GET'])
def start_reservation():
	# try to reserve a scooter
	if success:
		return render_template('res_start_success.html')
	else:
		return render_template('res_start_failure.html')
		
def init_db():
	db = json.loads(open('scooter_db.json', 'r').read())
	return db