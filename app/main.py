from fastapi import FastAPI
from . import models
from .database import engine
from . routers import auth, post, user, vote
from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
      

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.on_event("startup")    #This is a decorator that registers the function to be called when the application starts up. In this case, it will create the database tables defined in the models.
def startup():
    models.Base.metadata.create_all(bind=engine)    #This line creates all the tables in the database that are defined in the models. It uses the metadata from the models to create the tables in the database specified by the engine. This ensures that the database is set up and ready to use when the application starts.


@app.get("/")
async def root():
    return {"Message": "Hello World. This is my FastAPI application. The application is running successfully. This is the root endpoint. You can access this endpoint by going to http://localhost:8000/ in your browser or by using a tool like curl or Postman to send a GET request to the root endpoint. This also runs on my own public IP address. Thank You for visiting an have a nice day!"}



