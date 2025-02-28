import arrow
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

lat=float(input("Enter the latitude: "))
long=float(input("Enter the Longitude: "))


time = arrow.now()



response_bio = requests.get(
  'https://api.stormglass.io/v2/bio/point',
  params={
    'lat': lat,   
    'lng':  long,
    'params': ','.join(['soilMoisture40cm','soilTemperature']),
    'start': time.to('UTC').timestamp(),  
    'end': time.to('UTC').timestamp()  
  },
  headers={
    'Authorization': 'ef9d57be-de41-11ef-acf2-0242ac130003-ef9d587c-de41-11ef-acf2-0242ac130003' #Using GMAIL:-namananil2005@gmail.com
  }
)

response_weather = requests.get(
    'https://api.stormglass.io/v2/weather/point',
    params={
        'lat': lat,
        'lng': long,
        'params': 'humidity',
        'start': time.to('UTC').timestamp(),
        'end': time.to('UTC').timestamp()
    },
    headers={
        'Authorization': 'ef9d57be-de41-11ef-acf2-0242ac130003-ef9d587c-de41-11ef-acf2-0242ac130003' #Using GMAIL:-namananil2005@gmail.com
  }
)


# print(response_weather.json())

Soil_Moisture=response_bio.json()['hours'][0]['soilMoisture40cm']['noaa']
Soil_percentage=Soil_Moisture*100
print(f"Soil Moisture: {Soil_percentage}%")

Soil_Temp=response_bio.json()['hours'][0]['soilTemperature']['noaa']
print(f"Soil Temperature: {Soil_Temp}")

humidity=response_weather.json()['hours'][0]['humidity']['noaa']
print(f"Humidity: {humidity}%")


Nitrogen = requests.get(
        url="https://api.openepi.io/soil/property",
        params={
            "lat": lat,
            "lon": long,
            "depths": "5-15cm",
            "properties": "nitrogen",
            "values": "Q0.5",
        },
    )

ph = requests.get(
        url="https://api.openepi.io/soil/property",
        params={
            "lat": lat,
            "lon": long,
            "depths": "15-30cm",
            "properties": "phh2o",
            "values": "Q0.5",
        },
    )

soc = requests.get(
        url="https://api.openepi.io/soil/property",
        params={
            "lat": lat,
            "lon": long,
            "depths": "5-15cm",
            "properties": "soc",
            "values": "Q0.5",
        },
    )

# print(response.status_code)

nitrogen_value = Nitrogen.json()['properties']['layers'][0]['depths'][0]['values']['Q0.5'] 
print(f"Nitrogen value is:{nitrogen_value}")

# soil_Nitrogen = response.json()['properties']['layers'][4]['depths'][3]['values']['Q0.5']
# print(f"nitrogen at 15-30cm: {soil_Nitrogen} cg/kg")

soil_Ph = ph.json()['properties']['layers'][0]['depths'][0]['values']['Q0.5']
soil_Ph=float(soil_Ph/10)
print(f"PH at 15-30cm: {soil_Ph}")

soil_SOC= soc.json()['properties']['layers'][0]['depths'][0]['values']['Q0.5']
print(f"SOC at 5-15cm: {soil_SOC} dg/kg")







# Load your dataset (replace 'crop_data.csv' with your actual dataset)
data = pd.read_csv(r'c:\Users\Mihir\Downloads\Crop_recommendation3.csv')

# Display the first few rows of the dataset
print(data.head())

# Split the dataset into features (X) and target (y)
# Assuming your dataset has features like 'moisture', 'temperature', 'nitrogen', etc., and the target column is 'crop'
X = data[['N', 'ph']]  # Add other soil features if you have more
y = data['label']  # Target variable - crop to recommend

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=42)

# Initialize the Decision Tree Classifier
dt_model = DecisionTreeClassifier()

# Train the model
dt_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = dt_model.predict(X_test)

# Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Show detailed classification report
print(classification_report(y_test, y_pred))

# Example: Make a prediction on a new set of soil data from API
# Replace with the values you receive from the API
new_soil_data = [[nitrogen_value, soil_Ph]]  # Example input for nitrogen and pH

# Use predict_proba to get probability estimates for each crop
probabilities = dt_model.predict_proba(new_soil_data)

# Get the indices of the top 3 crops with the highest probability
top_3_indices = probabilities[0].argsort()[-3:][::-1]

# Get the corresponding crop labels
top_3_crops = dt_model.classes_[top_3_indices]

# Print the top 3 recommended crops
print("Top 3 Recommended Crops:")
for i, crop in enumerate(top_3_crops, 1):
    print(f"{i}. {crop}")