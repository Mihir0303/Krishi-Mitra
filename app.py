from flask import Flask, request, jsonify
import arrow
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)

# Load dataset
DATA_PATH = r'C:\Users\Mihir\Downloads\Crop_recommendation3.csv'
data = pd.read_csv(DATA_PATH)
X = data[['N', 'ph']]
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=42)
dt_model = DecisionTreeClassifier()
dt_model.fit(X_train, y_train)

def fetch_soil_data(lat, long):
    time = arrow.now().to('UTC').timestamp()
    
    # Fetch soil moisture & temperature
    response_bio = requests.get(
        'https://api.stormglass.io/v2/bio/point',
        params={'lat': lat, 'lng': long, 'params': 'soilMoisture40cm,soilTemperature', 'start': time, 'end': time},
        headers={'Authorization': 'ef9d57be-de41-11ef-acf2-0242ac130003-ef9d587c-de41-11ef-acf2-0242ac130003'}
    ).json()
    
    # Fetch humidity
    response_weather = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={'lat': lat, 'lng': long, 'params': 'humidity', 'start': time, 'end': time},
        headers={'Authorization': 'ef9d57be-de41-11ef-acf2-0242ac130003-ef9d587c-de41-11ef-acf2-0242ac130003'}
    ).json()
    
    # Fetch nitrogen, pH, SOC
    nitrogen = requests.get("https://api.openepi.io/soil/property", params={"lat": lat, "lon": long, "depths": "5-15cm", "properties": "nitrogen", "values": "Q0.5"}).json()
    ph = requests.get("https://api.openepi.io/soil/property", params={"lat": lat, "lon": long, "depths": "15-30cm", "properties": "phh2o", "values": "Q0.5"}).json()
    
    nitrogen_value = nitrogen.get('properties', {}).get('layers', [{}])[0].get('depths', [{}])[0].get('values', {}).get('Q0.5')
    soil_Ph = ph.get('properties', {}).get('layers', [{}])[0].get('depths', [{}])[0].get('values', {}).get('Q0.5')

    if nitrogen_value is None or soil_Ph is None:
        return None, None  # Handle missing data

    soil_Ph = float(soil_Ph) / 10  # Convert to correct format

    return nitrogen_value, soil_Ph

@app.route('/predict', methods=['POST'])
def predict_crop():
    try:
        # ✅ Debugging: Check incoming request data
        print("Request JSON:", request.get_json())

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        lat = data.get("latitude")
        long = data.get("longitude")

        if lat is None or long is None:
            return jsonify({"error": "Latitude and Longitude are required"}), 400

        print(f"Latitude: {lat}, Longitude: {long}")  # ✅ Debugging

        nitrogen_value, soil_Ph = fetch_soil_data(lat, long)
        if nitrogen_value is None or soil_Ph is None:
            return jsonify({"error": "Soil data unavailable for this location"}), 500

        new_soil_data = [[nitrogen_value, soil_Ph]]
        probabilities = dt_model.predict_proba(new_soil_data)
        top_3_indices = probabilities[0].argsort()[-3:][::-1]
        top_3_crops = dt_model.classes_[top_3_indices]

        return jsonify({"recommended_crops": list(top_3_crops)})

    except Exception as e:
        print(f"Error in predict_crop: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
