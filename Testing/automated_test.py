# Import module
import random
from __test__ import unitTester
from termcolor import cprint

# Function for the automated testing function
def automated_test(testCaseCounter):
    location_arr = ["adyar", "anna nagar", "chrompet", "kk nagar", "karapakkam", "t nagar", "velachery"]
    parking_arr = ["no", "yes"]
    houseType_arr = ["commercial", "house", "others"]
    streetType_arr = ["gravel", "no access", "paved"]
    N_BEDROOM_arr = [1,2,3,4,5]
    N_BATHROOM_arr = [1,2,3,4,5]
    N_ROOM_arr = [1,2,3,4,5]
    QS_ROOMS_arr = [1,2,3,4,5]
    QS_BATHROOM_arr = [1,2,3,4,5]
    QS_BEDROOM_arr = [1,2,3,4,5]
    QS_OVERALL_arr = [1,2,3,4,5]

    # Generating a random test case
    testCase = [random.choice(location_arr),random.choice(parking_arr),random.choice(houseType_arr),random.choice(streetType_arr),random.choice(range(500, 2501)),random.choice(N_BEDROOM_arr),random.choice(N_BATHROOM_arr),random.choice(N_ROOM_arr),random.choice(QS_ROOMS_arr),random.choice(QS_BATHROOM_arr),random.choice(QS_BEDROOM_arr),random.choice(QS_OVERALL_arr)]

    location = testCase[0]
    parking = testCase[1]
    houseType = testCase[2]
    streetType = testCase[3]
    INT_SQFT = testCase[4]
    N_BEDROOM = testCase[5]
    N_BATHROOM = testCase[6]
    N_ROOM = testCase[7]
    QS_ROOMS = testCase[8]
    QS_BATHROOM = testCase[9]
    QS_BEDROOM = testCase[10]
    QS_OVERALL = testCase[11]

    # Testing using the unitTester function from the __test__.py program
    if(unitTester(location, parking, houseType, streetType, INT_SQFT, N_BEDROOM, N_BATHROOM, N_ROOM, QS_ROOMS, QS_BATHROOM, QS_BEDROOM, QS_OVERALL)):
        cprint(f'Test Case {testCaseCounter} Passed', 'green', attrs=['bold'])
    else:
        cprint(f'Test case {testCaseCounter} Failed', 'red', attrs=['bold'])



# ---------------------------------------------------------- DRIVER CODE ------------------------------------------------------
if __name__ == '__main__':

    n = int(input("Enter the number of test cases to run: "))   
    for i in range(1,n+1):
        automated_test(i)
