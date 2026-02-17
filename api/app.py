from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from pathlib import Path
import numpy as np

app = Flask(__name__)
CORS(app) # Allow requests from extension

# Load models from same directory as app.py
pipeline = joblib.load("pipeline.pkl")

@app.route("/")
def home():
    return "API is running"

@app.route('/predict', methods=['POST'])
def predict():
	try:
		data = request.json
		title = data.get('title', '')
		description = data.get('description', '')

		# Combine title and description (same as training)
		text = f"{title} {description}"

		# Predict
		prediction = pipeline.predict([text])
		probabilities = pipeline.predict_probab([text])

		# Map prediction to label
		labels = ['Beginner', 'Intermediate', 'Advanced']

		return jsonify({
			'prediction': prediction[0],
			'confidence': float(max(probabilities))
		})

	except Exception as e:
		return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
	return jsonify({'status': 'healthy'})


if __name__ == "__main__":
	app.run(debug=True, port=5000)