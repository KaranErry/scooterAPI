from flask import Flask, render_template, request
from geopy.distance import distance


app=Flask(__name__)

# root
@app.route('/')
def home():
	return render_template('home.html')


# Search for scooters
@app.route('/', methods=['GET'])
def search():
	# Search for scooters in the database
	search_lat, search_lng, search_radius = request.args['lat'], request.args['lng'], request.args['radius']	# parse request for search criteria
	# TODO: put in documentation that this will raise a werkzeug.exceptions.BadRequestKeyError exception if the args are not there
	db = init_db()	# initialize db
	search_results = []
	for scooter_dict in db:
		scooter_lat, scooter_lng, scooter_radius = scooter_dict['lat'], scooter_dict['lng'], scooter_dict['radius'] # populate scooter attributes
		# Calculate distance between the scooter location point and the search location point, in metres
		distance = distance((scooter_lat, scooter_lng), (search_lat, search_lng)).m
		if distance <= search_radius:
			# this scooter is within the search area
			search_results.append(scooter_dict['id'])
	return search_results

	
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
	db_json = open('scooter_db.json', 'r').read()
	return json.loads(db_json)
	
## class scooter for internal use
#class Scooter:
#	def __init__(self, scooter_id, lat, lng, reserved):
#		self.scooter_id = scooter_id
#		self.lat = lat
#		self.lng = lng
#		self.reserved = reserved
		
def write_db(db):
	db_json = json.dumps(db)
	open('scooter_db.json', 'w').write(db_json)