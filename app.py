from flask import Flask, request

import kettle
from database import Database


app = Flask(__name__)

kettle = kettle.Kettle()
db = Database()


@app.post("/api/turnOnKettle")
def turn_on_kettle():
    kettle.turn_on()
    return "<p>The kettle has been turned on</p>"

@app.post("/api/turnOffKettle")
def turn_off_kettle():
    kettle.turn_off()
    return "<p>The kettle has been turned off</p>"

@app.post("/api/fillKettle")
def fill_kettle():
    kettle.set_water_level(float(request.args.get("water_level")))
    kettle.set_water_temperature(float(request.args.get("water_temperature")))
    return f"<p>The kettle water level has been set to {kettle.water_level} and water temperature to {kettle.water_temperature}</p>"

@app.get("/api/getKettleInfo")
def get_kettle_info():
    return db.read_all_records()