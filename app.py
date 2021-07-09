# Package importing
from flask import Flask, render_template, url_for, redirect, jsonify, request
from authlib.integrations.flask_client import OAuth
import util

# Declaring the flasks app name
app = Flask(__name__)

# ============================================= Authentication configration for Google and Github ========================================
oauth = OAuth(app)

# Secret key is the one asset that defines your are the authorized owner of the software
app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"

# CLIENT_ID and CLIENT_SECRET are the credentials from the developer account of Google
app.config['GOOGLE_CLIENT_ID'] = "790276491366-hf1untelphhtvafl00o5beagffj918d1.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "f-Lymg1iLNvvhQl_RZXZfQOp"

# CLIENT_ID and CLIENT_SECRET are the credentials from the developer account of Github
app.config['GITHUB_CLIENT_ID'] = "67beeb3d9297f11e3102"
app.config['GITHUB_CLIENT_SECRET'] = "8f8a06364b62b470c02da78e5adf2c25bbe22de2"

# Autlib Oauth2.0 configration for Google
google = oauth.register(
    name='google',
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # This is only needed if using openId to fetch user info
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

# Autlib Oauth2.0 configration for Github
github = oauth.register(
    name='github',
    client_id=app.config["GITHUB_CLIENT_ID"],
    client_secret=app.config["GITHUB_CLIENT_SECRET"],
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)
# ========================================================================================================================================

# ================================================== Authentication routing for Google and Github ========================================


# Default route to the home page
@app.route('/')
def index():
    return render_template('index.html')


# Route to the login page
@app.route('/login')
def login():
    return render_template('login.html')


# Google login route
@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorized route
@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    print(f"\n{resp}\n")
    redirect_uri = url_for('estimate_Price', _external=False)
    # return "You are successfully signed in using google"
    return redirect(redirect_uri)


# Github login route
@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


# Github authorized route
@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    print(f"\n{resp}\n")
    redirect_uri = url_for('estimate_Price', _external=False)
    # return "You are successfully signed in using google"
    return redirect(redirect_uri)


# Contact the developer's route
@app.route('/contact')
def contact_page():
    return render_template('contact.html')


# Contact the developer's route
@app.route('/estimatePrice')
def estimate_Price():
    return render_template('PriceEstimator.html')


# ========================================================================================================================================

# =================================================== Machine Learning Backend Routing ===================================================


#  Get the location info.
@app.route('/get_location_names')
def get_location_names():
    response = jsonify({'location': util.get_location_names()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


#  Get the parking info.
@app.route('/get_parking')
def get_parking():
    response = jsonify({'parking': util.get_parking()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


#  Get the type of house info.
@app.route('/get_houseType')
def get_houseType():
    response = jsonify({'houseType': util.get_houseType()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


#  Get the type of street info
@app.route('/get_streetType')
def get_streetType():
    response = jsonify({'streetType': util.get_streetType()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# Route to predict the house prices
@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    '''
    @ The predict_home_price docs:

        House Features:
            INT_SQFT – The interior Sq. Ft of the property
            N_BEDROOM – The number of Bed rooms
            N_BATHROOM - The number of bathrooms
            N_ROOM – Total Number of Rooms
            QS_ROOMS – The quality score assigned for rooms based on buyer reviews
            QS_BATHROOM – The quality score assigned for bathroom based on buyer reviews
            QS_BEDROOM – The quality score assigned for bedroom based on buyer reviews
            QS_OVERALL – The Overall quality score assigned for the property

        BUILD TYPE – 
            House (ready to move-in)
            Commercial (it's a property for rental / business)
            Others (can be villa, penthouse etc.)

        Surrounding and Locality
            Parking Facility – Whether parking facility is available.

        STREET TYPE - 
            Gravel 
            Paved
            No Access
    '''
    if request.method == "POST":
        # String datatype attributes
        location = request.form.get('ui-location')
        parking = request.form.get('ui-parking-facility')
        houseType = request.form.get('ui-house-type')
        streetType = request.form.get('ui-street-type')

        # int datatype attributes
        INT_SQFT = int(request.form.get('ui-int-sqft'))
        N_BEDROOM = int(request.form.get('ui-n-bedroom'))
        N_BATHROOM = int(request.form.get('ui-n-bathroom'))
        N_ROOM = int(request.form.get('ui-n-room'))
        QS_ROOMS = int(request.form.get('ui-qs-room'))
        QS_BATHROOM = int(request.form.get('ui-qs-bathroom'))
        QS_BEDROOM = int(request.form.get('ui-qs-bedroom'))
        QS_OVERALL = int(request.form.get('ui-qs-overall'))

        print('got the values in here!!!')
        response = jsonify({
            'estimated_price':
            util.get_estimated_price(location, parking, houseType, streetType,
                                     INT_SQFT, N_BEDROOM, N_BATHROOM, N_ROOM,
                                     QS_ROOMS, QS_BATHROOM, QS_BEDROOM,
                                     QS_OVERALL)
        })
        print(response)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return render_template('PriceEstimator.html',response=response.json)


# ======================================================================================================================================

# =============================================================== Driver Code ==========================================================
if __name__ == '__main__':
    # Loading the artifacts....
    util.load_saved_artifacts()
    app.run(debug=True)
