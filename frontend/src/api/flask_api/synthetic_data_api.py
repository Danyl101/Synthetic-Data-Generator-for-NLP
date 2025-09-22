from flask_cors import CORS
from flask import Flask
import logging
from flask import Blueprint,request, jsonify

from BERT_Preprocess.preprocess_run import preprocess_run 
from BERT_Preprocess.paraphraser import get_paraphraser_model
from BERT_Preprocess.bert_semantic import get_sbert_model

app=Flask(__name__)
CORS(app)

logger=logging.getLogger("Flask")

bp=Blueprint('synthetic_data_api',__name__)

@bp.route("/api/run-synthetic_data", methods=["POST"]) #Web Link Endpoint
def scrape():
    try:
        get_paraphraser_model() #Loads model from paraphraser.py
        get_sbert_model() #Loads model from bert_semantic.py
        data=preprocess_run() #Runs python file from backend
        print("DEBUG: preprocess_run returned:", data)
        return jsonify({"status":"success","data":data})
    except Exception as e:
        logger.error(f"Failed to run preprocess {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
        
if __name__ == "__main__":
    app.run(debug=True, port=5000)