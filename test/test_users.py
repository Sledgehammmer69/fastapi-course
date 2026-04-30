import pytest
from jose import jwt
from app import schemas
from app.config import settings







def test_root(client_fixture):                      # Define a test function to test the root endpoint of the FastAPI app
    res = client_fixture.get("/")                   # Send a GET request to the root endpoint ("/") of the FastAPI app
    print(res)                                      # Print the response object to the console for debugging purposes
    print(res.json())                               # Print the JSON content of the response to the console for debugging purposes
    print(res.json().get("Message"))                # Print the value associated with the "Message" key in the JSON response to the console for debugging purposes
    assert res.json().get("Message") == "Hello World. Welcome to my FastApi creation. Testingbeing done on docker as well....if this can be seen then it is working. Thanks for watching." # Assert that the value of the "Message" key in the JSON response matches the expected string
    #assert res.status_code == 201                  # Assert that the status code of the response is 201 (Created)


def test_create_user(client_fixture):               # Define a test function to test the user creation endpoint
    res = client_fixture.post("/users/", json={"email": "hkello123@gamil.com", "password": "password123"}) # Send a POST request to the "/users/" endpoint with a JSON payload containing an email and password
    print(res.json())                               # Print the JSON content of the response to the console for debugging purposes

    new_user = schemas.UserOut(**res.json())        # Create a new instance of the UserOut schema using the JSON response from the API
    assert new_user.email == "hkello123@gamil.com"
    assert res.status_code == 201                   # Assert that the status code of the response is



################################# test login ###############################################################################################

def test_login_user(client_fixture, test_user):                                     # Define a test function to test the user login endpoint
    res = client_fixture.post("/login", 
        data={"username": test_user["email"], "password": test_user["password"]})   #siwtch it from json to data since we are sending form data instead of json payload. 
    login_res = schemas.Token(**res.json())                                         # Create a new instance of the Token schema using the JSON response from the API
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]) # Decode the access token from the login response using the secret key and algorithm specified in the settings
    id = payload.get("user_id")                                                     # Extract the user ID from the decoded token payload
    assert id == test_user["id"]                                                    # Assert that the user ID from the token payload matches the ID of the test user
    assert login_res.token_type == "bearer"                                         # Assert that the token type in the login response is "bearer"
    assert res.status_code == 200                                                   # Assert that the status code of the response is 200 (OK)


@pytest.mark.parametrize("email, password, status_code",[
    ("wrongemail@gmail.com", "password123", 403),
    ("hkello123@gamil.com", "wrongpassword", 403),
    ("wongemail@gmail.com", "wrongpassword", 403),
    (None, "password123", 422),
    ("hkello123@gamil.com", None, 422)
])
def test_incorrect_login(test_user, client_fixture, email, password, status_code):  # Define a test function to test incorrect login scenarios
    res = client_fixture.post("/login", 
        data={"username": email, "password": password})                             # Send a POST request to the "/login" endpoint with incorrect password
    assert res.status_code == status_code                                           # Assert that the status code of the response is 403 (Forbidden) for incorrect login
    #assert res.json().get("detail") == "Invalid Credentials"                       # Assert that the error message in the response indicates invalid credentials




