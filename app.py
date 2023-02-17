from flask import Flask, request, jsonify

import kettle
from database import Database


app = Flask(__name__)

kettle = kettle.Kettle()
db = Database()


@app.post("/api/turnOnKettle")
def turn_on_kettle():
    try:
        kettle.turn_on()
    except Exception as error:
        response = jsonify({"error": str(error)})
    else:
        response = jsonify({"message": "The kettle has been turned on."})
    finally:
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.post("/api/turnOffKettle")
def turn_off_kettle():
    try:
        kettle.turn_off()
    except Exception as error:
        response = jsonify({"error": str(error)})
    else:
        response = jsonify({"message": "The kettle has been turned off."})
    finally:
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.post("/api/fillKettle")
def fill_kettle():
    water_level = request.args.get("water_level")
    water_temperature = request.args.get("water_temperature")

    if water_level is None:
        response = jsonify({"error": "Water level has not been specified."})
    elif water_temperature is None:
        response = jsonify({"error": "Water temperature has not been specified."})
    else:
        kettle.set_water_level(float(water_level))
        kettle.set_water_temperature(float(water_temperature))
        response = jsonify({"message": f"The kettle water level has been set to {kettle.water_level} and water temperature to {kettle.water_temperature}."})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.get("/api/getKettleInfo")
def get_kettle_info():
    response = jsonify({"list": db.read_all_records()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.get("/api/getLastDatabaseRecord")
def get_last_database_record():
    response = jsonify(db.read_last_record())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response