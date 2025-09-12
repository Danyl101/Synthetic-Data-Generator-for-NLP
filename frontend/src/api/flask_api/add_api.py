from flask_cors import CORS
from flask import Flask
import json
import logging
from config_loader import config
from flask import Blueprint,request, jsonify
app = Flask(__name__)
CORS(app)

logger=logging.getLogger("Flask")

bp = Blueprint("add_api", __name__) #Defines blueprint which groups related API routes

@bp.route("/api/add-filter", methods=["POST"])
def add_goodlist():
    try:
        data=request.get_json() #Acquires data from the frontend
    except Exception as e:
        logger.error(f"Data not acquired from typescript API {e}")

    try:
        with open(config["paths"]['scraping']['site_filters'], "r", encoding="utf-8") as f:
            filter_data = json.load(f) #Loads data from json file
    except Exception as e:
        logger.error(f"Initial data load from json failed {e}")
        
    try:
        for new_filter in data: #Checks each input from user input
            if new_filter not in filter_data["goodlist"]: 
                filter_data["goodlist"].append(new_filter) #Appends inputs
                logger.info(f"Added new filter: {new_filter}")
    except Exception as e:
        logger.error(f"Filtering execution failed {e}")

    try:
        with open(config["paths"]['scraping']['site_filters'], "w", encoding="utf-8") as f:
            json.dump(filter_data, f) #Writes into json file
    except Exception as e:
        logger.error(f"Data write into json failed {e}")
        
    return jsonify({"status":"success"})


@bp.route("/api/add-site", methods=["POST"])
def add_websites():
    try:
        data=request.get_json()  #Acquires data from the frontend
    except Exception as e:
        logger.error("Data not acquired from typescript API",e)

    try:
        with open(config["paths"]['scraping']['site_filters'], "r", encoding="utf-8") as f:
            site_data=json.load(f) #Loads data from json file
    except Exception as e:
        logger.error("Initial data load from json failed",e)
        
    try:
        for new_site in data: #Checks each input from user input
            if new_site not in site_data["websites"]:
                site_data["websites"].append(new_site) #Appends inputs
    except Exception as e:
        logger.error("Filtering execution failed",e)

    try:
        with open(config["paths"]['scraping']['site_filters'], "w", encoding="utf-8") as f:
            json.dump(site_data, f) #Writes data into json
    except Exception as e:
        logger.error("Data write into json failed",e)

    return jsonify({"status":"success"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)