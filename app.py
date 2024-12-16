import uuid
from flask import Flask, request
from flask_smorest import abort
from db import bikes, dimensions

app = Flask(__name__)

############BIKES##############

@app.get("/bike") #This is a FLASK Route, endpoint

def get_bikes():
    return bikes #This will return the store

@app.get("/bike/<string:bike_id>")

def get_bike(bike_id):
    try:
        return bikes[bike_id]
    except KeyError:
        abort(404, message="Bike not found")

@app.post("/bike")

def create_bike():
    bike_data = request.get_json()
    if "make" not in bike_data:
        abort(
            400,
            message="Bad Request. Bike Name is not included"
        )

    for bike in bikes.values():
        if(
            bike_data["make"] == bike["make"]
            and bike_data["model"] == bike["model"]
        ):
            abort(
                400,
                message = "Duplicate Request"
            )

    bike_id = uuid.uuid4().hex
    bike = {**bike_data}

    bikes[bike_id] = bike
    return bikes, 201

@app.delete("/bike/<string:bike_id>")

def delete_bike(bike_id):
    try:
        del bikes[bike_id]
        return {"message": "Bike deleted"}
    except KeyError:
        abort(404, message="Bike not found")\

@app.put("/bike/<string:bike_id>")

def update_bikes(bike_id):

    bike_data = request.get_json()

    if (
        "make" not in bike_data
        or "model" not in bike_data
    ):
        abort(
            400,
            message="Bad request. Ensure make and model are included"
        )
    
    if bike_id not in bikes:
        abort(
            400,
            message="Bad request. Dimensions not found"            
        )

    bike = {**bike_data}
    bikes[bike_id] = bike

    return bikes, 201

############DIMENSIONS##############       

@app.get("/dimension")
def get_all_dimensions():
    return dimensions

@app.get("/dimension/<string:dimension_id>")

def get_dimension(dimension_id):
    try:
        return dimensions[dimension_id]
    except KeyError:
        abort(404, message="Dimensions not found")

@app.post("/dimensions") #This will put a new dimension into the object
def create_dimension():
    dimension_data = request.get_json()

    if (
        "stack" not in dimension_data
        or "reach" not in dimension_data
        # or "name" not in dimension_data
    ):
        abort(
            400,
            message="Bad request. Ensure stack, reach, and name are included"
        )

    if dimension_data["bike_id"] not in bikes:
        abort(404, message="Store not found")

    dimension_id = uuid.uuid4().hex
    dimension = {**dimension_data}

    for dimension in dimensions.values():
        if (
            dimension_data["bike_id"] == dimension["bike_id"]
        ):
            abort(
                400,
                message="Duplicate Bike Dimension."
            )

    dimensions[dimension_id] = dimension
    return dimensions, 201

@app.delete("/dimension/<string:dimension_id>")

def delete_dimension(dimension_id):
    try:
        del dimensions[dimension_id]
        return {"message": "Dimensions deleted"}
    except KeyError:
        abort(404, message="Dimensions not found")

@app.put("/dimension/<string:dimension_id>")

def update_dimension(dimension_id):

    dimension_data = request.get_json()

    if (
        "stack" not in dimension_data
        or "reach" not in dimension_data
        # or "bike_id" not in dimension_data
    ):
        abort(
            400,
            message="Bad request. Ensure stack, reach, and name are included"
        )
    
    try:
        dimensions[dimension_id].update(**dimension_data)
        return dimensions, 201
    except KeyError:
        abort(
            404,
            message="Bad request. Dimensions not found"            
        )
