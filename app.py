from flask import Flask, render_template, request, jsonify
import pandas as pd
import datetime
from transformers import pipeline

app = Flask(__name__)

# Load the language model using Hugging Face transformers (adjust model for your needs)
recommendation_model = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")  # Adjust model if necessary

# Define a helper function to get month index
def month_index(month_name):
    return datetime.strptime(month_name, "%B").month

# Defining the dataset directly in the code
crop_data = pd.DataFrame({
    'Crop Name': ['Rice', 'Wheat', 'Sugarcane', 'Banana', 'Cotton', 'Maize', 'Tomato', 'Soybean', 
                  'Groundnut', 'Pulses', 'Chili', 'Millets', 'Turmeric', 'Sorghum', 'Mustard', 'Barley'],
    'Region': ['Cauvery Delta', 'Cauvery Delta', 'Cauvery Delta', 'Cauvery Delta', 
               'Maharashtra', 'Madhya Pradesh', 'Punjab', 'Uttar Pradesh', 
               'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 
               'Tamil Nadu', 'Tamil Nadu'],
    'Start Month': ['January', 'February', 'March', 'April', 'June', 'May', 'March', 'May',
                    'June', 'July', 'June', 'May', 'February', 'June', 'August', 'September'],
    'End Month': ['March', 'May', 'June', 'December', 'September', 'October', 'July', 'August',
                  'November', 'September', 'July', 'September', 'November', 'July', 'October', 'December'],
    'Water Requirement': ['High', 'Normal', 'Low', 'Normal', 'Low', 'Normal', 'High', 'Low',
                          'Medium', 'Medium', 'High', 'Medium', 'Low', 'Normal', 'Medium', 'Normal'],
    'Maintenance Level': ['High', 'Low', 'High', 'Medium', 'Low', 'Medium', 'High', 'Low',
                          'Low', 'Low', 'Medium', 'High', 'High', 'Medium', 'Low', 'Low'],
    'Profit Level': ['High', 'High', 'Low', 'High', 'Medium', 'High', 'Medium', 'High',
                     'Low', 'Medium', 'High', 'Medium', 'Low', 'Medium', 'High', 'High'],
    'Expected Yield (tons/acre)': [3.0, 2.0, 8.0, 18.0, 1.5, 2.5, 8.0, 2.5,
                                   1.0, 0.8, 3.5, 1.5, 2.5, 2.0, 2.5, 1.8],
    'Expected Investment (₹/acre)': [25000, 30000, 50000, 60000, 35000, 25000, 40000, 20000, 
                                     20000, 15000, 30000, 25000, 20000, 35000, 22000, 23000],
    'Fertilizer Requirements': ['Nitrogen, Phosphorus', 'Potassium, Nitrogen', 'Phosphorus, Magnesium', 
                                'Nitrogen, Magnesium', 'Phosphorus, Potassium', 'Nitrogen, Potassium', 
                                'Phosphorus, Nitrogen', 'Magnesium, Nitrogen', 'Nitrogen, Potassium',
                                'Phosphorus, Magnesium', 'Potassium, Mag nesium', 'Nitrogen, Phosphorus',
                                'Magnesium, Nitrogen', 'Phosphorus, Potassium', 'Nitrogen, Potassium',
                                'Nitrogen, Phosphorus']
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    region = data['region']
    start_month = data['start_month']
    end_month = data['end_month']
    land_area = data['land_area']
    
    # Filter data based on region and months
    filtered_data = crop_data[(crop_data['Region'] == region) & 
                              (crop_data['Start Month'] <= start_month) & 
                              (crop_data['End Month'] >= end_month)]
    
    # Select a sample crop for recommendation (for demonstration)
    sample_crop = filtered_data.iloc[0]
    crop_name = sample_crop['Crop Name']
    
    # Generate a crop recommendation message with LLM
    prompt = (f"Suggest the best way to cultivate {crop_name} in {region} region from "
              f"{start_month} to {end_month} for {land_area} acres.")
    llm_output = recommendation_model(prompt, max_length=100, num_return_sequences=1)
    
    response = {
        "recommendation": llm_output[0]['generated_text'],
        "crop_data": sample_crop.to_dict()  # Include crop data for additional context if needed
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)  