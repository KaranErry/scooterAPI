from flask import Flask, render_template, request, redirect, url_for, make_response
from geopy.distance import distance as geodesic
import json, werkzeug
from http import HTTPStatus

app=Flask(__name__)

# root
@app.route('/')
def home():
	return redirect(url_for('view_all_available'))
	
@app.route('/view_all_available')
def view_all_available():
	db = init_db()
	available_scooters = [scooter for scooter in db if not scooter.is_reserved]
	available_scooters_dictlist = convert_db_to_dictlist(available_scooters)
	return json.dumps(available_scooters_dictlist), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# return a json-ified list of all the scooters with status 200


# Search for scooters
@app.route('/search', methods=['GET'])
def search():
	# Search for scooters in the database
	# parse request params
	try:
		search_lat, search_lng, search_radius = \
			float(request.args['lat']), \
			float(request.args['lng']), \
			float(request.args['radius'])	# parse request for search criteria
	except werkzeug.exceptions.BadRequestKeyError:
		# the required parameters are not present in the search query
		error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	except ValueError:
		error = { 'msg': 'Error 422 - Lat/Lng values must be numbers' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422

	# validate lat and long values
	if not -90 <= search_lat <= 90:
		error = { 'msg': 'Error 422 - Latitude must be in the [-90, 90] range.'}
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	if not -180 <= search_lng <= 180:
		error = { 'msg': 'Error 422 - Longitude must be in the [-180, 180] range.'}
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	
	db = init_db()	# initialize db

	search_results = []
	for scooter in db:
		# Calculate distance between the scooter location point and the search location point, in metres
		distance = geodesic((scooter.lat, scooter.lng), (search_lat, search_lng)).m
		if distance <= search_radius and not scooter.is_reserved:
			# this scooter is available and within the search area
			search_results.append({	'id':scooter.id, 
									'lat':scooter.lat, 
									'lng':scooter.lng
								  })
			
	return json.dumps(search_results), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# return json-ified search results list with status 200

	
# Start a reservation 
@app.route('/reservation/start', methods=['GET'])
def start_reservation():
	# parse request params
	try:
		reserve_id = request.args['id']	# parse request for id of scooter to be reserved
	except werkzeug.exceptions.BadRequestKeyError:
		# the required parameters are not present in the search query
		error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422

	db = init_db()
	
	# try and find the scooter with specified id
	scooter = get_scooter_with_id(reserve_id, db)
	if scooter:
		# reserve if possible
		if not scooter.is_reserved:
			# scooter can be reserved
			scooter.is_reserved = True
			write_db(db)	# update db
			success = { 'msg': f'Scooter {reserve_id} was reserved successfully.' }
			return json.dumps(success), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# respond with status 200

		else:
			# the scooter is already reserved
			error = { 'msg': f'Error 422 - Scooter with id {reserve_id} is already reserved.' }
			return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	else:
		# no scooter with the reserve id was found
		error = { 'msg': f'Error 422 - No scooter with id {reserve_id} was found.' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422


# End a reservation
@app.route('/reservation/end', methods=['GET'])
def end_reservation():
	# parse request params
	try:
		scooter_id_to_end = request.args['id']	# parse request for id of scooter whose reservation to be ended
		end_lat, end_lng = \
			float(request.args['lat']), \
			float(request.args['lng'])
		db = init_db()
	except werkzeug.exceptions.BadRequestKeyError:
		# the required parameters are not present in the search query
		error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	except ValueError:
		error = { 'msg': 'Error 422 - Lat/Lng values must be numbers' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422

	# validate lat and long values
	if not -90 <= end_lat <= 90:
		error = { 'msg': 'Error 422 - Latitude must be in the [-90, 90] range.'}
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	if not -180 <= end_lng <= 180:
		error = { 'msg': 'Error 422 - Longitude must be in the [-180, 180] range.'}
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
		
	# try and find the scooter with specified id
	scooter = get_scooter_with_id(scooter_id_to_end, db)
	if scooter:
		# end reservation if possible
		if scooter.is_reserved:
			# scooter is reserved and can be ended
			
			# initiate payment
			payment_response = pay(scooter, end_lat, end_lng)
			if payment_response['status']:
				# the payment was completed successfully
				
				# update scooter's reserved status and location
				scooter.is_reserved = False
				scooter.lat, scooter.lng = end_lat, end_lng
				write_db(db)
				# construct successful response
				success =	{	'msg': f'Payment for scooter {scooter_id_to_end} was made successfully and the reservation was ended.',
								'txn_id': payment_response['txn_id']
							}
				return json.dumps(success), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# respond with status 200
			else:
				# the payment failed for some reason
				error = { 'msg': payment_response['msg'] }
				response_code = payment_response['code']
				return json.dumps(error), response_code, {'Content-Type':'application/json'}
		else:
			# the scooter is not currently reserved
			error = { 'msg': f'Error 422 - No reservation for scooter {scooter_id_to_end} presently exists.' }
			return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	else:
		# no scooter with the id was found
		error = { 'msg': f'Error 422 - No scooter with id {scooter_id_to_end} was found.' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422


# ==================
#  HELPER FUNCTIONS	
# ==================


def pay(scooter, end_lat, end_lng):
	# Initialise the payment process
	# construct location point tuples
	old_location = (scooter.lat, scooter.lng)
	new_location = (end_lat, end_lng)
	# calculate distance between points, in metres
	distance_ridden = geodesic(old_location, new_location).m
	distance_ridden = round(distance_ridden)
	# calculate cost (currently a dummy function that returns the distance as the cost)
	cost = calculate_cost(distance_ridden)	# returns cost = distance for now
	# redirect to payment gateway and return response (currently a dummy function that returns a hypothetical transaction id)
	return payment_gateway(cost)	# returns hypothetical success and txn id for now
	
def payment_gateway(cost):
	# TODO: Implement real payment processing in future
	txn_id = 379892831
	return 	{	'status': True,
				'txn_id': txn_id
			}

def calculate_cost(distance):
	# TODO: Implement meaningful cost calculation in future
	return distance

		
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
	
	
def get_scooter_with_id(search_id, db):
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
		db_list.append(scooter.to_dict())
	return db_list
		


if __name__== "__main__":
	# TODO: Turn debug flag off for production system
	app.run('localhost', 8080)