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
	# reserve_id = request.form['id'] # for POST request
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
		
	# try and find the scooter with specified id
	scooter = get_scooter_with_id(scooter_id_to_end, db)
	if scooter:
		# end reservation if possible
		if scooter.is_reserved:
			# scooter is reserved and can be ended
			scooter.is_reserved = False
			write_db(db)	# update db
			# redirect to payment page
			return redirect(url_for('pay', id=scooter_id_to_end, lat=end_lat, lng=end_lng))
		else:
			# the scooter is not currently reserved
			error = { 'msg': f'Error 422 - No reservation for scooter {scooter_id_to_end} presently exists.' }
			return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	else:
		# no scooter with the id was found
		error = { 'msg': f'Error 422 - No scooter with id {scooter_id_to_end} was found.' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	
			
# Pay for a completed reservation
@app.route('/reservation/pay', methods=['GET'])
def pay():
	try:
		scooter_id, end_lat, end_lng = \
			request.args['id'], \
			float(request.args['lat']), \
			float(request.args['lng'])	# parse request for end-reservation details
	except werkzeug.exceptions.BadRequestKeyError:
		# the required parameters are not present in the search query
		error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	except ValueError:
		error = { 'msg': 'Error 422 - Lat/Lng values must be numbers' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	
	# try and find the scooter with specified id
	db = init_db()
	scooter = get_scooter_with_id(scooter_id, db)
	if scooter:
		# construct location point tuples
		old_location = (scooter.lat, scooter.lng)
		new_location = (end_lat, end_lng)
		# calculate distance between points, in metres
		distance_ridden = geodesic(old_location, new_location).m
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
							 	'msg':f'Payment for scooter {scooter_id} was made successfully.',
								'txn_id':txn_id
							}
		else:
			# there was a problem with the transaction
			error = { 'msg': f"Error 422 - {payment_response['msg']}" }
			return json.dumps(error), 404, {'ContentType':'application/json'} 
	else:
		# no scooter with the id was found
		error = { 'msg': f'Error 422 - No scooter with id {scooter_id} was found.' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	
	return json.dumps(response_dict), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# return response dict


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
	# TODO: Turn debug flag off for production system
	app.run('localhost', 8080)