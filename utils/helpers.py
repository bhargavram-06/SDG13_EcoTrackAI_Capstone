def calculate_transportation_emissions(distance, vehicle_type):
    # Emissions factor in kg CO2 per km
    factors = {
        "Petrol Car": 0.17,
        "Diesel Car": 0.16,
        "Electric Vehicle": 0.05,
        "Motorcycle": 0.10,
        "Bus/Train": 0.03,
        "Walking/Bicycle": 0.00
    }
    return distance * factors.get(vehicle_type, 0.0)

def calculate_electricity_emissions(kwh):
    # Global average emission factor: ~0.45 kg CO2 per kWh
    return kwh * 0.45

def calculate_diet_emissions(diet_type, days=1):
    # Daily emission estimates in kg CO2
    factors = {
        "Heavy Meat Eater": 7.2,
        "Average Meat Eater": 5.6,
        "Pescatarian (Fish)": 3.8,
        "Vegetarian": 3.2,
        "Vegan": 2.1
    }
    return factors.get(diet_type, 3.0) * days