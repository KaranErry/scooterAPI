from flask import Flask, render_template, request
from geopy.distance import distance


app=Flask(__name__)

# root
@app.route('/')
def home():
	return render_template('home.html')
	
@app.route('/view_all_availble')
def view_all():
	db = init_db()
	all_scooters = convert_db_to_dictlist(db)
	return json.dumps(all_scooters)	# return a json-ified list of all the scooters


# Search for scooters
@app.route('/search', methods=['GET'])
def search():
	# Search for scooters in the database
	search_lat, search_lng, search_radius = request.args['lat'], request.args['lng'], request.args['radius']	# parse request for search criteria
	# TODO: put in documentation that this will raise a werkzeug.exceptions.BadRequestKeyError exception if the args are not there
	
	db = init_db()	# initialize db
	search_results = []
	for scooter in db:
		# Calculate distance between the scooter location point and the search location point, in metres
		distance = distance((scooter.lat, scooter.lng), (search_lat, search_lng)).m
		if distance <= search_radius and not scooter.is_reserved:
			# this scooter is available and within the search area
			search_results.append({	'id':scooter.id, 
									'lat':scooter.lat, 
									'lng':scooter.lng
								  })
			
	return json.dumps(search_results)	# return json-ified search results list

	
# Start a reservation 
@app.route('/reservation/start', methods=['GET'])
def start_reservation():
	reserve_id = request.args['id']	# parse request for id of scooter to be reserved
	# TODO: put in documentation that this will raise a werkzeug.exceptions.BadRequestKeyError exception if the args are not there
	db = init_db()
	
	# find the scooter with specified id to reserve
	try:
		scooter_to_reserve = next(scooter for scooter in db if scooter.id = reserve_id)	# get the scooter whose id matches the desired reserve_id
	except StopIteration:
		# no scooter with the reserve id was found
		response_dict = {	'result':False,
						 	'msg':f'No scooter with id {reserve_id} was found.'
						}
	
	# reserve if possible
	if not scooter_to_reserve.is_reserved:
		# scooter can be reserved
		scooter_to_reserve.is_reserved = True
		response_dict = {	'result':True,
						 	'msg':f'Scooter {reserve_id} was reserved successfully.'
						}
	else:
		# the scooter is already reserved
		response_dict = {	'result':False,
						 	'msg':f'Scooter with id {reserve_id} is already reserved.'
						}
			
	return json.dumps(response_dict)	# return response dict


# End a reservation
@app.route('/reservations/end', methods=['GET'])
def end_reservation():
	scooter_id_to_end = request.args['id']	# parse request for id of scooter whose reservation to be ended
	# TODO: put in documentation that this will raise a werkzeug.exceptions.BadRequestKeyError exception if the args are not there
	db = init_db()
		
	# find the scooter with specified id
	try:
		scooter_to_end_reserve = next(scooter for scooter in db if scooter.id = scooter_id_to_end)	# get the scooter whose id matches the desired scooter_id_to_end
	except StopIteration:
		# no scooter with the id was found
		response_dict = {	'result':False,
						 	'msg':f'No scooter with id {scooter_id_to_end} was found.'
						}
		
	# reserve if possible
	if scooter_to_reserve.is_reserved:
		# scooter is reserved and can be ended
		scooter_to_reserve.is_reserved = False
		# redirect to payment page
		return redirect(url_for('pay', id=))
	else:
		# the scooter is not currently reserved
		response_dict = {	'result':False,
						 	'msg':f'No reservation for scooter {scooter_id_to_end} presently exists.'
						}
	
	return json.dumps(response_dict)	# return response dict
	
			
# Pay for a completed reservation
@app.route('/reservation/pay', methods=['GET'])
def pay():
	# TODO: implement mock payments process
	response_dict = {	'result':True,
					 	'msg':f'Reservation for scooter {scooter_id_to_end} was ended successfully.',
						'txn_id':txn_id
					}
	
	return json.dumps(response_dict)	# return response dict	
		
		
def init_db():
	db_json = open('scooter_db.json', 'r').read()
	db_list = json.loads(db_json)
	# populate Scooter objects for easier access later
	db = []
	for scooter in db_list:
		scooter_obj = Scooter(	scooter['id'], 
								scooter['lat'], 
								scooter['lng'], 
								scooter['is_reserved']
							 )
		db.append(scooter_obj)
	return db
	
		
def write_db(db):
	# serialize Scooter objects 
	db_list = convert_db_to_dictlist(db)
	db_json = json.dumps(db_list)
	open('scooter_db.json', 'w').write(db_json)
	return True
		
# class scooter for internal use
class Scooter:
	def __init__(self, scooter_id, lat, lng, is_reserved):
		self.id = scooter_id
		self.lat = lat
		self.lng = lng
		self.is_reserved = is_reserved
	
	def to_dict(self):
		return {	'id':self.id, 
					'lat':self.lat, 
					'lng':self.lng, 
					'is_reserved':self.is_reserved
			   }
		
def convert_db_to_dictlist(db):
	db_list = []
	for scooter in db:
		db_list.append(scooter.to_dict)
	return db_list