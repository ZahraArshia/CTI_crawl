from fastapi import FastAPI, Path, HTTPException
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import subprocess

app = FastAPI()

from typing import List

@app.get("/items")
async def get_items():
    # Connect to MongoDB and retrieve items
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["mongo-sandbox"]
        collection = db["thehackernews"]
        items = list(collection.find())

    # Convert ObjectId to string before returning the JSON response
    items_with_str_id = [dict(item, _id=str(item["_id"])) for item in items]

    return dumps(items_with_str_id)

@app.get("/items/{item_id}")
async def get_item(item_id: str = Path(..., description="The ID of the item to get")):
    # Validate 'item_id' and convert it to a valid ObjectId
    try:
        item_id = ObjectId(item_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid item ID")

    # Connect to MongoDB and retrieve the item by ID
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["mongo-sandbox"]
        collection = db["thehackernews"]
        item = collection.find_one({"_id": item_id})

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Convert ObjectId to string before returning the JSON response
    item_with_str_id = dict(item, _id=str(item["_id"]))

    return dumps(item_with_str_id)

# @app.post("/items")
# async def create_item():
#     # Run the 'scrapy crawl main.py' command using subprocess
#     try:
#         result = subprocess.run(["scrapy", "crawl", "main"], capture_output=True, text=True, cwd="manesh_new")

#         if result.returncode != 0:
#             raise HTTPException(status_code=400, detail=f"Error 400 occurred while running the command: {result.stderr}")

#         return {"status": "success", "output": result.stdout}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error 500 occurred while running the command: {str(e)}")


@app.post("/crawl")
async def crawl():
    try:
        result = subprocess.run(["scrapy", "crawl", "main"], capture_output=True, text=True, cwd="theHackerNews")

        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=f"Error 400 occurred while running the command: {result.stderr}")

        return {"status": "success", "output": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error 500 occurred while running the command: {str(e)}")
    
# @app.get("/items")
# def get_items():
#     # Connect to MongoDB and retrieve items
#     with MongoClient("mongodb://localhost:27017") as client:
#         db = client["mongo-sandbox"]
#         collection = db["thehackernews"]
#         items = list(collection.find())
#     return items

# @app.post("/items")
# async def create_item(item: dict):
#     # Connect to MongoDB and insert item
#     with MongoClient("your_mongo_uri") as client:
#         db = client["your_database_name"]
#         collection = db["thehackernews"]
#         result = collection.insert_one(item)
#     return {"id": str(result.inserted_id)}

# ... Define other endpoints as needed
