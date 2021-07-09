import os
import pickle
import numpy as np
import json

global __data_columns
global __model


def unitTester(location, parking, houseType, streetType, INT_SQFT, N_BEDROOM, N_BATHROOM, N_ROOM, QS_ROOMS, QS_BATHROOM, QS_BEDROOM, QS_OVERALL):

    # Load the machine learning model
    with open("Testing\Model\Machine_Learning_Model.pickle", "rb") as f:
        __model = pickle.load(f)

    # Load the json file
    with open("Testing\Model\columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']

    # created a 2D Array
    x = np.zeros(len(__data_columns))

    # check for the valid inputs
    try:
        x[0] = __data_columns.index(location.lower())
        x[1] = __data_columns.index(parking.lower())
        x[2] = __data_columns.index(houseType.lower())
        x[3] = __data_columns.index(streetType.lower())
    except ValueError:
        # print("TEST CASE FAILED: Invalid String Inputs")
        return False

    try:
        ValidInputForNRooms = [1,2,3,4,5,6]
        ValidInput = [1, 2, 3, 4, 5]
        x[4] = int(INT_SQFT)
        x[5] = int(N_BEDROOM)
        x[6] = int(N_BATHROOM)
        x[7] = int(N_ROOM)
        x[8] = int(QS_ROOMS)
        x[9] = int(QS_BATHROOM)
        x[10] = int(QS_BEDROOM)
        x[11] = int(QS_OVERALL)

        # check for the valid input range
        if(x[4] < 500 or x[4] > 2500):
            # print("INTERIOR SQFT: Index out of bound")
            return False
        if(x[5] not in ValidInput):
            # print("N_BEDROOM: Index out of bound")
            return False
        if(x[6] not in ValidInput):
            # print("N_BATHROOM: Index out of bound")
            return False
        if(x[7] not in ValidInputForNRooms):
            # print("N_ROOM: Index out of bound")
            return False
        if(x[8] not in ValidInput):
            # print("QS_ROOMS: Index out of bound")
            return False
        if(x[9] not in ValidInput):
            # print("QS_BATHROOM: Index out of bound")
            return False
        if(x[10] not in ValidInput):
            # print("QS_BEDROOM: Index out of bound")
            return False
        if(x[11] not in ValidInput):
            # print("QS_OVERALL: Index out of bound")
            return False

    except ValueError:
        # print("TEST CASE FAILED: Invalid Numeral Inputs")
        return False

    estimatedPrice = int(__model.predict([x])[0])

    if(2156875 <= estimatedPrice or estimatedPrice <= 23667340):
        # print("TEST CASES PASSED!!!!")
        return True
    else:
        # print("TEST CASES FAILED!!!!")
        return False

