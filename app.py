from flask import Flask, render_template, request, jsonify
from predict import predict_water_quality

app = Flask(__name__)

FEATURES = [
    "Temperature",
    "Turbidity (cm)",
    "Dissolved Oxygen (mg L-1)",
    "Biochemical Oxygen Demand (mg L-1)",
    "Carbon Dioxide (mg L-1)",
    "pH",
    "Total Alkalinity (mg L-1 as CaCO3)",
    "Total Hardness (mg L-1 as CaCO3)",
    "Calcium (mg L-1)",
    "Estimated Magnesium (mg L-1)",
    "Ammonia (mg L-1)",
    "Nitrite (mg L-1)",
    "Phosphorus (mg L-1)",
    "Hydrogen Sulphide (mg L-1)",
    "Plankton Abundance (No. L-1)"
]

DEFAULTS = {
    "Temperature": 28.5,
    "Turbidity (cm)": 25.0,
    "Dissolved Oxygen (mg L-1)": 6.5,
    "Biochemical Oxygen Demand (mg L-1)": 5.0,
    "Carbon Dioxide (mg L-1)": 6.0,
    "pH": 7.4,
    "Total Alkalinity (mg L-1 as CaCO3)": 180.0,
    "Total Hardness (mg L-1 as CaCO3)": 300.0,
    "Calcium (mg L-1)": 80.0,
    "Estimated Magnesium (mg L-1)": 40.0,
    "Ammonia (mg L-1)": 0.5,
    "Nitrite (mg L-1)": 0.05,
    "Phosphorus (mg L-1)": 0.2,
    "Hydrogen Sulphide (mg L-1)": 0.02,
    "Plankton Abundance (No. L-1)": 800.0
}

CLASS_INFO = {
    "Highly Suitable":       {"color": "#22c55e", "icon": "✅"},
    "Suitable":              {"color": "#3b82f6", "icon": "🔵"},
    "Restricted / Stressed": {"color": "#f59e0b", "icon": "⚠️"},
    "Unsuitable / Critical": {"color": "#ef4444", "icon": "🚨"},
}

@app.route("/")
def index():
    return render_template("index.html",
        features=FEATURES,
        defaults=DEFAULTS,
        class_info=CLASS_INFO
    )

@app.route("/predict", methods=["POST"])
def predict():
    try:
        params = {f: float(request.form.get(f, 0)) for f in FEATURES}
        result = predict_water_quality(params)
        result["info"] = CLASS_INFO.get(result.get("classification", ""), {})
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("🌊 Running at http://localhost:5000")
    app.run(debug=True, port=5000)