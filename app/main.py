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

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"Message": "Hello World. Welcome to my FastApi creation. Testingbeing done on docker as well....if this can be seen then it is working. Thanks for watching."}



