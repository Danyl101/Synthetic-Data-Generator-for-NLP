from flask_cors import CORS
from flask import Flask
import json
import logging
from flask import Blueprint,request, jsonify
app = Flask(__name__)
CORS(app)
from config_loader import config

logger=logging.getLogger("Flask")

bp = Blueprint("remove_api", __name__)

@bp.route("/api/remove-filter", methods=["POST"]) #Web Link Endpoint
def remove_goodlist():
    try:
        data = request.get_json() #Acquires input from frontend
        logger.info("Data acquired from frontend")
    except Exception as e:
        logger.error(f"Data not acquiried from frontend {e}")

    try:
        with open(config["paths"]['scraping']['site_filters'], "r") as f: 
            filter_data=json.load(f)  #Reads Json file
            logger.info("Data loading from json successful")
    except Exception as e:
        logger.error(f"Data loading from json failed {e}")
     
    try:   
        original_len = len(filter_data["goodlist"]) #Checks length of list
        filter_data["goodlist"] = [
            item for item in filter_data["goodlist"] if item not in data
        ] #Removes filter 
        removed_count = original_len - len(filter_data["goodlist"]) #returns filter number removed
        logger.info(f"Removed {removed_count} filters")
    except Exception as e:
            logger.error(f"Removal of filter failed {e}")

    try:
        with open(config["paths"]['scraping']['site_filters'],"w")as f:
            json.dump(filter_data,f) #Writes data into json 
            logger.info("Data writing into json successful")
    except Exception as e:
        logger.error(f"Data writing into json failed {e}")

    return jsonify({"status": "success"})

@bp.route("/api/remove-site", methods=["POST"]) #Web Link Endpoint
def remove_websites():
    try:
        data = request.get_json() #Acquires input from frontend 
        logger.info("Data acquired from frontend")
    except Exception as e:
        logger.error(f"Data not acquiried from frontend {e}")

    try:
        with open(config["paths"]['scraping']['site_filters'], "r") as f: 
            site_data=json.load(f) #Reads Json file
            logger.info("Data loading from json successful")
    except Exception as e:
        logger.error(f"Data loading from json failed {e}")

    try:   
        original_len = len(site_data["websites"]) #Checks length of list
        site_data["websites"] = [
            item for item in site_data["websites"] if item not in data
        ] #Removes filter 
        removed_count = original_len - len(site_data["websites"]) #Returns filter number removed
        logger.info(f"Removed {removed_count} websites")
    except Exception as e:
            logger.error(f"Removal of site failed {e}")

    try:
        with open(config["paths"]['scraping']['site_filters'],"w")as f:
            json.dump(site_data,f) #Writes data into json
            logger.info("Data writing into json successful")
    except Exception as e:
        logger.error(f"Data writing into json failed {e}")

    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
