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
	for scooter in db:
		# Calculate distance between the scooter location point and the search location point, in metres
		distance = distance((scooter.lat, scooter.lng), (search_lat, search_lng)).m
		if distance <= search_radius and not scooter.reserved:
			# this scooter is available and within the search area
			search_results.append({'id':scooter.id, 'lat':scooter.lat, 'lng':scooter.lng})
	return json.dumps(search_results)	# return json-ified search results list

	
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
	id = request.args['id']
	# TODO: try to end a reservation
	
	# TODO: put in documentation that this will raise a werkzeug.exceptions.BadRequestKeyError exception if the 'id' arg is not there
	
	if success:
		# TODO: calculate distance
		# redirect to payment page
		return redirect(url_for('pay', id=))
	else:
		return render_template('res_end_failure.html')
	
			
# Pay for a completed reservation
@app.route('/reservation/pay', methods=['GET'])
def pay():
	# TODO: implement mock payments process
	return txn_id
		
		
		
def init_db():
	db_json = open('scooter_db.json', 'r').read()
	db_list = json.loads(db_json)
	# populate Scooter objects for easier access later
	db = []
	for scooter in db_list:
		scooter_obj = Scooter(scooter['id'], scooter['lat'], scooter['lng'], scooter['reserved'])
		db.append(scooter_obj)
	return db
	
		
def write_db(db):
	db_list = {}
	for scooter in db:
		scooter_dict = {'id':scooter.id, 'lat':scooter.lat, 'lng':scooter.lng, 'reserved':scooter.reserved}
		db_list.append(scooter_dict)
	db_json = json.dumps(db_list)
	open('scooter_db.json', 'w').write(db_json)
		
# class scooter for internal use
class Scooter:
	def __init__(self, scooter_id, lat, lng, reserved):
		self.id = scooter_id
		self.lat = lat
		self.lng = lng
		self.reserved = reserved