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
    
    deficit = {"N": flower["N"] - input_n, "P": flower["P"] - input_p, "K": flower["K"] - input_k}
    
    fertilizer_needed = {}
    soil_fertility_good = all(value <= 0 for value in deficit.values())
    
    if not soil_fertility_good:
        for nutrient, value in deficit.items():
            if value > 0:
                fert = fertilizers[nutrient]
                required_amount = (value * area_m2) / (fert["composition"] / 100)
                fertilizer_needed[nutrient] = {"fertilizer": fert["name"], "amount_kg": round(required_amount, 2)}
    else:
        return {"message": "Your soil fertility is good. No additional fertilizers are needed.", "flower_name": flower_name}
    
    return {
        "flower_name": flower_name,
        "area_acres": area_acres,
        "fertilizer_recommendation": fertilizer_needed
    }

def precise_fertilization(flower_name, area_acres, soil_inputs):
    if flower_name not in flower_data:
        return "Flower not found in database."
    
    section_area = area_acres / 4  # Divide the farm into 4 sections
    results = {}
    
    for section, values in soil_inputs.items():
        results[section] = calculate_fertilizer(values['N'], values['P'], values['K'], values['pH'], flower_name, section_area)
    
    return results

# Example usage

def main():
    farm_type = input("Choose farm type (1. Complete Farm, 2. Division Farm): ")
    flower_name = input("Enter flower name: ")
    area_acres = float(input("Enter farm area size (in acres): "))
    
    if farm_type == "1":
        input_n = float(input("Enter Nitrogen (N) level: "))
        input_p = float(input("Enter Phosphorus (P) level: "))
        input_k = float(input("Enter Potassium (K) level: "))
        input_ph = float(input("Enter pH level: "))
        result = calculate_fertilizer(input_n, input_p, input_k, input_ph, flower_name, area_acres)
    
    elif farm_type == "2":
        soil_inputs = {}
        for section in ["NE", "NW", "SW", "SE"]:
            print(f"Enter soil data for {section} section:")
            n = float(input("Enter Nitrogen (N) level: "))
            p = float(input("Enter Phosphorus (P) level: "))
            k = float(input("Enter Potassium (K) level: "))
            ph = float(input("Enter pH level: "))
            soil_inputs[section] = {"N": n, "P": p, "K": k, "pH": ph}
        
        result = precise_fertilization(flower_name, area_acres, soil_inputs)
    
    else:
        result = "Invalid selection."
    
    print(result)

if __name__ == "__main__":
    main()
