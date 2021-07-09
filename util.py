import json
import pickle
import numpy as np
import sklearn

# GLOBAL VARIABLES
__locations = None
__parking = None
__houseType = None
__streetType = None
__data_columns = None
__model = None

# ================================================== Function to get 'estimated house price' =============================================


def get_estimated_price(location, parking, houseType, streetType, INT_SQFT,
                        N_BEDROOM, N_BATHROOM, N_ROOM, QS_ROOMS, QS_BATHROOM,
                        QS_BEDROOM, QS_OVERALL):
    try:
        loc_index = __data_columns.index(location.lower())
        park_index = __data_columns.index(parking.lower())
        house_index = __data_columns.index(houseType.lower())
        street_index = __data_columns.index(streetType.lower())
    except:
        loc_index = -1
        park_index = -1
        house_index = -1
        street_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = INT_SQFT
    x[1] = N_BEDROOM
    x[2] = N_BATHROOM
    x[3] = N_ROOM
    x[4] = QS_ROOMS
    x[5] = QS_BATHROOM
    x[6] = QS_BEDROOM
    x[7] = QS_OVERALL

    # setting the location index
    if loc_index >= 0:
        x[loc_index] = 1

    #setting the parking index
    if park_index >= 0:
        x[park_index] = 1

    # setting the house typr index
    if house_index >= 0:
        x[house_index] = 1

    # setting the street type index
    if street_index >= 0:
        x[street_index] = 1

    return int(__model.predict([x])[0])


# ======================================================================================================================================

# ================================================== Function to get values for attributes =============================================


def get_location_names():
    return __locations


# get the location names
def get_parking():
    return __parking


# get the location names
def get_houseType():
    return __houseType


# get the location names
def get_streetType():
    return __streetType


# ======================================================================================================================================

# ================================================== Function to load the saved artifacts ==============================================


def load_saved_artifacts():
    print(" Initializing Saved Artifacts ....")
    global __data_columns
    global __locations
    global __parking
    global __houseType
    global __streetType
    global __model

    # opening the columns.json file in the read mode
    with open('./artifacts/columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[8:15]
        __parking = __data_columns[15:17]
        __houseType = __data_columns[17:20]
        __streetType = __data_columns[20:]

    # opening the Machine_Learning_Model.pickle binary file in read binary mode
    with open("./artifacts/Machine_Learning_Model.pickle", "rb") as f:
        __model = pickle.load(f)

    print("Loading the saved artifacts ....... Done")


# ==================================================================================================================================
