from flask import Flask, render_template, request
from geopy.distance import distance
import json

app=Flask(__name__)

# root
@app.route('/')
def home():
	return render_template('home.html')
	
@app.route('/view_all_available')
def view_all_available():
	db = init_db()
	available_scooters = [scooter for scooter in db if not scooter.is_reserved]
	available_scooters_dictlist = convert_db_to_dictlist(available_scooters)
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
	
	# try and find the scooter with specified id
	scooter = get_scooter_with_id(reserve_id)
	if scooter:
		# reserve if possible
		if not scooter_to_reserve.is_reserved:
			# scooter can be reserved
			scooter_to_reserve.is_reserved = True
			write_db(db)	# update db
			response_dict = {	'result':True,
							 	'msg':f'Scooter {reserve_id} was reserved successfully.'
							}
		else:
			# the scooter is already reserved
			response_dict = {	'result':False,
							 	'msg':f'Scooter with id {reserve_id} is already reserved.'
							}
	else:
		# no scooter with the reserve id was found
		response_dict = {	'result':False,
						 	'msg':f'No scooter with id {reserve_id} was found.'
						}
	
	return json.dumps(response_dict)	# return response dict


# End a reservation
@app.route('/reservations/end', methods=['GET'])
def end_reservation():
	scooter_id_to_end = request.args['id']	# parse request for id of scooter whose reservation to be ended
	end_lat, end_lng = request.args['lat'], request.args['lng']
	# TODO: put in documentation that this will raise a werkzeug.exceptions.BadRequestKeyError exception if the args are not there
	db = init_db()
		
	# try and find the scooter with specified id
	scooter = get_scooter_with_id(scooter_id_to_end)
	if scooter:
		# reserve if possible
		if scooter_to_reserve.is_reserved:
			# scooter is reserved and can be ended
			scooter_to_reserve.is_reserved = False
			write_db(db)	# update db
			# redirect to payment page
			return redirect(url_for('pay', id=scooter_id_to_end, lat=end_lat, lng=end_lng))
		else:
			# the scooter is not currently reserved
			response_dict = {	'result':False,
							 	'msg':f'No reservation for scooter {scooter_id_to_end} presently exists.'
							}
	else:
		# no scooter with the id was found
		response_dict = {	'result':False,
						 	'msg':f'No scooter with id {scooter_id_to_end} was found.'
						}
	
	return json.dumps(response_dict)	# return response dict
	
			
# Pay for a completed reservation
@app.route('/reservation/pay', methods=['GET'])
def pay():
	scooter_id, end_lat, end_lng = request.args['id'], request.args['lat'], request.args['lng']	# parse request for end-reservation details
	# TODO: put in documentation that this will raise a werkzeug.exceptions.BadRequestKeyError exception if the args are not there
	# try and find the scooter with specified id
	scooter = get_scooter_with_id(scooter_id)
	if scooter:
		# construct location point tuples
		old_location = (scooter.lat, scooter.lng)
		new_location = (end_lat, end_lng)
		# calculate distance between points, in metres
		distance_ridden = distance(old_location, new_location).m
		distance_ridden = round(distance_ridden)
		# calculate cost (currently a dummy function that returns the distance as the cost)
		cost = calculate_cost(distance_ridden)	# returns cost = distance for now
		# call the payment function (currently a dummy function that returns a hypothetical transaction id)
		payment_response = make_payment(cost)	# returns hypothetical success and txn id for now
		if payment_response['result']:
			# the transaction was successful
			txn_id = payment_response['txn_id']
			# update scooter's location
			scooter.lat, scooter.lng = end_lat, end_lng
			write_db(db)
			# construct successful response
			response_dict = {	'result':True,
							 	'msg':f'Payment for scooter {scooter_id_to_end} was made successfully.',
								'txn_id':txn_id
							}
		else:
			# there was a problem with the transaction
			response_dict = {	'result':False,
							 	'msg':payment_response['msg']
							}
	else:
		# no scooter with the id was found
		response_dict = {	'result':False,
						 	'msg':f'No scooter with id {scooter_id_to_end} was found.'
						}
	
	return json.dumps(response_dict)	# return response dict	
		
	
# ==================
#  HELPER FUNCTIONS	
# ==================
		
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
	
	
def get_scooter_with_id(search_id):
	db = init_db()
	try:
		scooter = next(scooter for scooter in db if scooter.id == search_id)	# get the scooter with specified id
		return scooter
	except StopIteration:
		# no scooter with the id was found
		return None
	
		
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
	

def calculate_cost(distance):
	# TODO: Implement meaningful cost calculation in future
	return distance
	
def make_payment(cost):
	# TODO: Implement real payment processing in future
	return {	'result':True,
				'msg':'Your payment was made successfully.',
				'txn_id':'379892831'			
		   }
		


if __name__== "__main__":
	# TODO: Turn debug flag off
	app.run('localhost', 8080, debug=True)