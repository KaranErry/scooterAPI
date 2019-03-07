from flask import Flask, render_template, request
import geopy

app=Flask(__name__)

# root/home
@app.route('/')
def home():
	return render_template('home.html')

# Search for scooters
@app.route('/', methods=['GET'])
def search():
	# TODO: Search for scooters and return
	
	return render_template('home.html')
	
# Start a reservation 
@app.route('/reservation/start', methods=['GET'])
def start_reservation():
	# TODO: try to reserve a scooter
	if success:
		return render_template('res_start_success.html')
	else:
		return render_template('res_start_failure.html')

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