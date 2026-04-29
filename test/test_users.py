from app import schemas
from .database_testing import client_fixture, session_fixture


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