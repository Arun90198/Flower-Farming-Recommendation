from flask import Flask, render_template, request, send_file
from weasyprint import HTML
import os

app = Flask(__name__)

# Predefined Flower Data
flower_data = {
    "Rose": {
        "N": 20, "P": 9, "K": 16, "pH": 6, "demand": "High", 
        "avg_price": 50, "duration": "90 days",
        "farming_type": "Greenhouse/Open Field",
        "irrigation": "Drip Irrigation",
        "harvesting": "Harvest in early morning; cut at 45-degree angle"
    },
    "Chrysanthemum": {
        "N": 12, "P": 39, "K": 19, "pH": 7, "demand": "Medium", 
        "avg_price": 40, "duration": "120 days",
        "farming_type": "Greenhouse/Open Field",
        "irrigation": "Sprinkler Irrigation",
        "harvesting": "Harvest before full bloom; use sharp tools"
    },
    "Marigold": {
        "N": 8, "P": 4, "K": 8, "pH": 6, "demand": "High", 
        "avg_price": 30, "duration": "60 days",
        "farming_type": "Open Field",
        "irrigation": "Drip/Sprinkler Irrigation",
        "harvesting": "Pluck flowers manually when fully bloomed"
    },
    "Tuberose": {
        "N": 20, "P": 8, "K": 15, "pH": 6, "demand": "Low", 
        "avg_price": 35, "duration": "150 days",
        "farming_type": "Greenhouse/Open Field",
        "irrigation": "Drip Irrigation",
        "harvesting": "Cut spikes when the first few flowers open"
    },
    "Gladiolus": {
        "N": 20, "P": 20, "K": 20, "pH": 8, "demand": "Medium", 
        "avg_price": 45, "duration": "100 days",
        "farming_type": "Greenhouse/Open Field",
        "irrigation": "Sprinkler Irrigation",
        "harvesting": "Harvest when lower buds show color"
    },
    "Crossandra": {
        "N": 5, "P": 10, "K": 6, "pH": 7, "demand": "High", 
        "avg_price": 25, "duration": "80 days",
        "farming_type": "Open Field",
        "irrigation": "Drip Irrigation",
        "harvesting": "Pick flowers manually every 2-3 days"
    }
}

fertilizers = {
    "N": {"name": "Urea", "composition": 46},
    "P": {"name": "Single Super Phosphate (SSP)", "composition": 16},
    "K": {"name": "Muriate of Potash (MOP)", "composition": 60}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    farm_type = request.form.get('farm_type', '').strip()
    area = float(request.form.get('area', 0))
    area_m2 = area * 4047
    section_area_m2 = area_m2 / 4
    section_acre = area / 4

    if farm_type.lower() == "complete":
        flower_name = request.form.get('flower_name', '').strip()
        if flower_name not in flower_data:
            return "Invalid flower name selected.", 400
        
        flower = flower_data[flower_name]
        n = float(request.form.get('n', 0))
        p = float(request.form.get('p', 0))
        k = float(request.form.get('k', 0))
        ph = float(request.form.get('ph', 0))
        
        deficit = {"N": max(0, flower["N"] - n), "P": max(0, flower["P"] - p), "K": max(0, flower["K"] - k)}
        fertilizer_recommendation = {}
        for nutrient, value in deficit.items():
            if value > 0:
                fert = fertilizers[nutrient]
                required_amount = (value * area_m2 // 1000) / (fert["composition"] / 100)
                fertilizer_recommendation[nutrient] = {"fertilizer": fert["name"], "amount_kg": round(required_amount, 2)}

        result = {
            "flower_name": flower_name,
            "farm_type": "Complete Farm",
            "area_acres": area,
            "deficit": deficit,
            "fertilizer_recommendation": fertilizer_recommendation if fertilizer_recommendation else "Soil fertility is good",
            "market_demand": flower["demand"],  
            "avg_price": flower["avg_price"],  
            "flowering_duration": flower["duration"],
            "farming_type": flower["farming_type"],
            "irrigation": flower["irrigation"],
            "harvesting": flower["harvesting"],
        }

    elif farm_type.lower() == "division":
        sections = ["NE", "NW", "SW", "SE"]
        division_results = {}
        for section in sections:
            flower_name = request.form.get(f'flower_name_{section}', '').strip()
            if flower_name not in flower_data:
                return f"Invalid flower name for {section} section.", 400
            
            flower = flower_data[flower_name]
            n = float(request.form.get(f'n_{section}', 0))
            p = float(request.form.get(f'p_{section}', 0))
            k = float(request.form.get(f'k_{section}', 0))
            ph = float(request.form.get(f'ph_{section}', 0))
            
            deficit = {"N": max(0, flower["N"] - n), "P": max(0, flower["P"] - p), "K": max(0, flower["K"] - k)}
            fertilizer_recommendation = {}
            for nutrient, value in deficit.items():
                if value > 0:
                    fert = fertilizers[nutrient]
                    required_amount = (value * section_area_m2 // 1000) / (fert["composition"] / 100)
                    fertilizer_recommendation[nutrient] = {"fertilizer": fert["name"], "amount_kg": round(required_amount, 2)}

            division_results[section] = {
                "flower_name": flower_name,
        
                "N": n,
                "P": p,
                "K": k,
                "pH": ph,
                "deficit": deficit,
                "fertilizer_recommendation": fertilizer_recommendation if fertilizer_recommendation else "Soil fertility is good",
                "market_demand": flower["demand"],
                "avg_price": flower["avg_price"],
                "flowering_duration": flower["duration"],
                "farming_type": flower["farming_type"],
                "irrigation": flower["irrigation"],
                "harvesting": flower["harvesting"],
            }
        result = {"farm_type": "Division Farm", "area_acres": section_acre, "division_results": division_results}

    else:
        return "Invalid farm type selected.", 400
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request, send_file
# from weasyprint import HTML
# import os

# app = Flask(__name__)

# # Predefined Flower Data
# flower_data = {
#     "Rose": {"N": 20, "P": 9, "K": 16, "pH": 6, "demand": "High", "avg_price": 50, "duration": "90 days"},
#     "Chrysanthemum": {"N": 12, "P": 39, "K": 19, "pH": 7, "demand": "Medium", "avg_price": 40, "duration": "120 days"},
#     "Marigold": {"N": 8, "P": 4, "K": 8, "pH": 6, "demand": "High", "avg_price": 30, "duration": "60 days"},
#     "Tuberose": {"N": 20, "P": 8, "K": 15, "pH": 6, "demand": "Low", "avg_price": 35, "duration": "150 days"},
#     "Gladiolus": {"N": 20, "P": 20, "K": 20, "pH": 8, "demand": "Medium", "avg_price": 45, "duration": "100 days"},
#     "Crossandra": {"N": 5, "P": 10, "K": 6, "pH": 7, "demand": "High", "avg_price": 25, "duration": "80 days"}
# }

# fertilizers = {
#     "N": {"name": "Urea", "composition": 46},
#     "P": {"name": "Single Super Phosphate (SSP)", "composition": 16},
#     "K": {"name": "Muriate of Potash (MOP)", "composition": 60}
# }

# # Function to Calculate Fertilizer Requirement
# def calculate_fertilizer(input_n, input_p, input_k, input_ph, flower_name, area_acres):
#     if flower_name not in flower_data:
#         return {"message": "Flower not found in database."}

#     flower = flower_data[flower_name]
#     area_m2 = area_acres * 4047  # Convert acres to square meters

#     deficit = {
#         "N": max(0, flower["N"] - input_n),
#         "P": max(0, flower["P"] - input_p),
#         "K": max(0, flower["K"] - input_k)
#     }

#     fertilizer_needed = {}
#     soil_fertility_good = all(value == 0 for value in deficit.values())

#     if not soil_fertility_good:
#         for nutrient, value in deficit.items():
#             if value > 0:
#                 fert = fertilizers[nutrient]
#                 required_amount = (value * area_m2//1000) / (fert["composition"] / 100)
#                 fertilizer_needed[nutrient] = {"fertilizer": fert["name"], "amount_kg": round(required_amount, 2)}

#     return {
#         "flower_name": flower_name,
#         "area_acres": area_acres,
#         "area_m2": area_m2,
#         "user_input": {"N": input_n, "P": input_p, "K": input_k, "pH": input_ph},
#         "required_values": {"N": flower["N"], "P": flower["P"], "K": flower["K"], "pH": flower["pH"]},
#         "deficit": deficit,
#         "fertilizer_recommendation": fertilizer_needed if not soil_fertility_good else "Soil fertility is good",
#         "market_demand": flower["demand"],
#         "avg_price": flower["avg_price"],
#         "flowering_duration": flower["duration"]
#     }

# # Flask Routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/recommend', methods=['POST'])
# def recommend():
#     flower_name = request.form['flower_name']
#     n = float(request.form['n'])
#     p = float(request.form['p'])
#     k = float(request.form['k'])
#     ph = float(request.form['ph'])
#     area = float(request.form['area'])

#     result = calculate_fertilizer(n, p, k, ph, flower_name, area)

#     return render_template('result.html', result=result)

# @app.route('/download_pdf', methods=['POST'])
# def download_pdf():
#     recommendation_text = request.form['recommendation']

#     html_content = f"""
#     <h2>Flower Farming Recommendation</h2>
#     <p>{recommendation_text}</p>
#     """

#     pdf_filename = "recommendation.pdf"
#     pdf_path = os.path.join(os.getcwd(), pdf_filename)

#     HTML(string=html_content).write_pdf(pdf_path)

#     return send_file(pdf_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
