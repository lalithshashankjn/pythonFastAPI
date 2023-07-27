
from fastapi import FastAPI, Response, status as HTTPStatus, HTTPException, Depends, APIRouter
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post,user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

cursor = None

while True:
    try:
        conn=psycopg2.connect(host="localhost",database="fastapidb",user="postgres",password="postgres", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        if cursor:
            print("Database Connection Successful")
            break
    except Exception as e:
        import time
        time.sleep(3)
        print(f"connection to database failed: {e}")
    
my_posts=[{"title":"title of post 1", "content":"content of post 1", "id":1},
          {"title":"favorite foods", "content":"I like pizza", "id":2}]

def findPostsByID(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def findPostIndex(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/") # Path should be unique, if duplicate, it will return first match
async def root(): # async is needed for async call, can be removed here. Optional in this context.
    return {"message":"Hello World"} # Fast API converts this to json

