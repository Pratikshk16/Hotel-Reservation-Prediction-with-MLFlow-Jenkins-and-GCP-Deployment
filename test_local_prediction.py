import requests

# Local Flask app URL (use your IP if testing on network)
url = "http://127.0.0.1:8080/"

data = {
    "lead_time": 45,
    "no_of_special_request": 1,
    "avg_price_per_room": 120.0,
    "arrival_month": 6,
    "arrival_date": 12,
    "market_segment_type": 4,
    "no_of_week_nights": 3,
    "no_of_weekend_nights": 1,
    "type_of_meal_plan": 0,
    "room_type_reserved": 2
}

response = requests.post(url, data=data)

print("Status Code:", response.status_code)
print("Response Text (truncated):")
print(response.text[:1000])
