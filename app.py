from flask import Flask


app=Flask(__name__)

# Home page
@app.route('/')
def home():
	return render_template('home.html')