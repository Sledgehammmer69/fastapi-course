from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base

from fastapi.testclient import TestClient # Import TestClient from fastapi.testclient
from app.main import app
import pytest
from app import schemas

#since this is a testing environment we can hardcode the database url here for testing purposes but we can also use the settings from config.py as well since we have already set up the testing database there as well. So we can use that as well for testing purposes.
#SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:Slenderman69@localhost:5432/fastapi_test' 

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test' #or we can use _test since we have already set up the testing database in config.py as well. So we can use that for testing purposes instead of hardcoding the database url here.

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine) #use this line to create the tables in the testing database based on the models defined in the app. This will ensure that the testing database has the necessary tables for the tests to run properly.


#dependency
def override_get_db():                  # Define a function to override the get_db dependency for testing purposes
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



#app.dependency_overrides[get_db] = override_get_db # Override the get_db dependency in the FastAPI app with the override_get_db function for testing purposes




client = TestClient(app)                               # Create an instance of TestClient using the FastAPI app
@pytest.fixture()                    #this will ensure that the fixture is run for each test function, so we get a clean slate for each test run. This is important to ensure that our tests are independent and do not interfere with each other.
def session_fixture():
    Base.metadata.drop_all(bind=engine)               #drop the tables in the testing database before running the tests to clean up the testing environment and ensure that it is reset for the next test run 
    Base.metadata.create_all(bind=engine)             #create the tables in the testing database before running the tests to ensure that the testing environment is set up correctly
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#this function is to create our tables in testing database
#the it's gonna run our test where yield just returns our test client and performs the test
#after that's done the tables will be dropped and we can start fresh for the next test run.
#it follows this pattern: run our code before we run our test (setup), then run our test, then run our code after we run our test (teardown) to clean up the testing environment.

#or we can switch the drop_all to the beginning of the fixture to ensure that we start with a clean slate 
#before running our tests, and then create the tables after dropping them. This way, we can ensure that any leftover data from previous test runs is removed before we create the tables for the current test run.


@pytest.fixture()                    #this will ensure that the fixture is run for each test function, so we get a clean slate for each test run. This is important to ensure that our tests are independent and do not interfere with each other. 
def client_fixture(session_fixture):                # Define a fixture function to provide a TestClient instance for testing
    #Base.metadata.drop_all(bind=engine)            #drop the tables in the testing database before running the tests to clean up the testing environment and ensure that it is reset for the next test run 
    #Base.metadata.create_all(bind=engine)          #create the tables in the testing database before running the tests to ensure that the testing environment is set up correctly
    def override_get_db():                          # Define a function to override the get_db dependency for testing purposes
        try:
            yield session_fixture
        finally:
            session_fixture.close()
    app.dependency_overrides[get_db] = override_get_db # Override the get_db dependency in the FastAPI app with the override_get_db function for testing purposes
    yield TestClient(app)                           #change from return to yield since we want to run some code before and after the test (setup and teardown)
    #Base.metadata.drop_all(bind=engine)            #drop the tables in the testing database after running the tests to clean up the testing environment and ensure that it is reset for the next test run 


@pytest.fixture()
def test_user(client_fixture):
    user_data = {"email": "hkello123@gamil.com",
                 "password": "password123"}
    res = client_fixture.post("/users/", json=user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user