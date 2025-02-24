flower_data = {
    "Rose": {"N": 20, "P": 9, "K": 16, "pH": 6, "demand": "High", "avg_price": 50, "duration": "90 days"},
    "Chrysanthemum": {"N": 12, "P": 39, "K": 19, "pH": 7, "demand": "Medium", "avg_price": 40, "duration": "120 days"},
    "Marigold": {"N": 8, "P": 4, "K": 8, "pH": 6, "demand": "High", "avg_price": 30, "duration": "60 days"},
    "Tuberose": {"N": 20, "P": 8, "K": 15, "pH": 6, "demand": "Low", "avg_price": 35, "duration": "150 days"},
    "Gladiolus": {"N": 20, "P": 20, "K": 20, "pH": 8, "demand": "Medium", "avg_price": 45, "duration": "100 days"},
    "Crossandra": {"N": 5, "P": 10, "K": 6, "pH": 7, "demand": "High", "avg_price": 25, "duration": "80 days"}
}

fertilizers = {
    "N": {"name": "Urea", "composition": 46},
    "P": {"name": "Single Super Phosphate (SSP)", "composition": 16},
    "K": {"name": "Muriate of Potash (MOP)", "composition": 60}
}

def calculate_fertilizer(input_n, input_p, input_k, input_ph, flower_name, area_acres):
    if flower_name not in flower_data:
        return "Flower not found in database."
    
    flower = flower_data[flower_name]
    area_m2 = area_acres * 4047  # Convert acres to square meters
    
    deficit = {
        "N": flower["N"] - input_n,
        "P": flower["P"] - input_p,
        "K": flower["K"] - input_k
    }
    
    fertilizer_needed = {}
    soil_fertility_good = all(value <= 0 for value in deficit.values())
    
    if not soil_fertility_good:
        for nutrient, value in deficit.items():
            if value > 0:
                fert = fertilizers[nutrient]
                required_amount = (value * area_m2) / (fert["composition"] / 100)
                fertilizer_needed[nutrient] = {"fertilizer": fert["name"], "amount_kg": round(required_amount, 2)}
    else:
        return {
            "message": "Your soil fertility is good. No additional fertilizers are needed.",
            "flower_name": flower_name,
            "area_acres": area_acres,
            "area_m2": area_m2,
            "user_input": {"N": input_n, "P": input_p, "K": input_k, "pH": input_ph},
            "required_values": {"N": flower["N"], "P": flower["P"], "K": flower["K"], "pH": flower["pH"]},
            "market_demand": flower["demand"],
            "avg_price": flower["avg_price"],
            "flowering_duration": flower["duration"]
        }
    
    return {
        "flower_name": flower_name,
        "area_acres": area_acres,
        "area_m2": area_m2,
        "user_input": {"N": input_n, "P": input_p, "K": input_k, "pH": input_ph},
        "required_values": {"N": flower["N"], "P": flower["P"], "K": flower["K"], "pH": flower["pH"]},
        "deficit": deficit,
        "fertilizer_recommendation": fertilizer_needed,
        "market_demand": flower["demand"],
        "avg_price": flower["avg_price"],
        "flowering_duration": flower["duration"]
    }

# Example usage
user_input = {
    "input_n": 10, "input_p": 7, "input_k": 16, "input_ph": 7, "flower_name": "Rose", "area_acres": 2
}

result = calculate_fertilizer(**user_input)
print(result)
