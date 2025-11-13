import joblib
import numpy as np
import shap
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request
import os
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)

# 🔹 Load trained model
loaded_model = joblib.load(MODEL_OUTPUT_PATH)

# 🔹 Try initializing SHAP explainer safely
try:
    explainer = shap.TreeExplainer(loaded_model)
    shap_type = "tree"
except Exception as e:
    print(f"[INFO] Default TreeExplainer failed: {e}")
    explainer = None
    shap_type = "none"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # --------------- 🔹 Collect input features ----------------
        lead_time = int(request.form["lead_time"])
        no_of_special_request = int(request.form["no_of_special_request"])
        avg_price_per_room = float(request.form["avg_price_per_room"])
        arrival_month = int(request.form["arrival_month"])
        arrival_date = int(request.form["arrival_date"])
        market_segment_type = int(request.form["market_segment_type"])
        no_of_week_nights = int(request.form["no_of_week_nights"])
        no_of_weekend_nights = int(request.form["no_of_weekend_nights"])
        type_of_meal_plan = int(request.form["type_of_meal_plan"])
        room_type_reserved = int(request.form["room_type_reserved"])

        features = np.array([[lead_time, no_of_special_request, avg_price_per_room,
                              arrival_month, arrival_date, market_segment_type,
                              no_of_week_nights, no_of_weekend_nights,
                              type_of_meal_plan, room_type_reserved]])

        # --------------- 🔹 Prediction & Probabilities -------------
        prediction = loaded_model.predict(features)[0]

        # LightGBM predict_proba returns [[p0, p1]] usually
        if hasattr(loaded_model, "predict_proba"):
            probabilities = loaded_model.predict_proba(features)[0]
        else:
            # fallback for models without predict_proba
            probabilities = [1 - prediction, prediction]

        cancel_prob = round(float(probabilities[1]) * 100, 2)
        not_cancel_prob = round(float(probabilities[0]) * 100, 2)

        # --------------- 🔹 SHAP Explainability --------------------
        top_features = []
        try:
            if shap_type == "tree":
                shap_values = explainer.shap_values(features)
                feature_names = [
                    "lead_time", "no_of_special_request", "avg_price_per_room",
                    "arrival_month", "arrival_date", "market_segment_type",
                    "no_of_week_nights", "no_of_weekend_nights",
                    "type_of_meal_plan", "room_type_reserved"
                ]

                # LightGBM returns shap_values as list of arrays
                shap_arr = shap_values[1] if isinstance(shap_values, list) else shap_values
                feature_importance = sorted(
                    zip(feature_names, shap_arr[0]),
                    key=lambda x: abs(x[1]),
                    reverse=True
                )[:3]

                top_features = [
                    {"feature": f, "impact": round(float(v), 3)} for f, v in feature_importance
                ]
        except Exception as e:
            print(f"[WARN] SHAP explainability skipped: {e}")
            top_features = [{"feature": "N/A", "impact": 0}]

        # --------------- 🔹 Actionable Suggestion ------------------
        if cancel_prob > 75:
            suggestion = "⚠️ High risk of cancellation. Suggest requesting a prepayment or non-refundable rate."
        elif cancel_prob > 50:
            suggestion = "⚠️ Moderate risk. Recommend sending a confirmation email or reminder to customer."
        else:
            suggestion = "✅ Low risk. Booking seems stable."

        # --------------- 🔹 Render to Frontend ---------------------
        return render_template(
            'index.html',
            prediction="Will Cancel" if prediction == 1 else "Will Not Cancel",
            cancel_prob=cancel_prob,
            not_cancel_prob=not_cancel_prob,
            top_features=top_features,
            suggestion=suggestion
        )

    else:
        # GET method
        return render_template('index.html', prediction=None)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
