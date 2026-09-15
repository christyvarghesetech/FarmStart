"""
Train scikit-learn ML Crop Suitability Classifier
Predicts suitability/yield category ('High', 'Medium', 'Low')
Features: crop, district, soil_type, N, P, K, pH, temperature, humidity, rainfall.
Ground truth rules synthesized from Kerala Agricultural University (KAU) Package of Practices.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

# Agricultural agronomic bounds for Kerala conditions
CROP_OPTIMALS = {
    "tomato": {
        "ph": (5.8, 7.0),
        "temp": (18.0, 28.0),
        "rain": (80.0, 220.0),
        "n": (60, 120),
        "p": (30, 80),
        "k": (40, 90),
        "favored_districts": ["Idukki", "Wayanad", "Palakkad", "Kottayam"],
        "favored_soils": ["Hill soil", "Laterite soil", "Red loam", "Sandy loam"]
    },
    "rice": {
        "ph": (5.5, 7.2),
        "temp": (22.0, 35.0),
        "rain": (180.0, 380.0),
        "n": (70, 130),
        "p": (30, 75),
        "k": (35, 80),
        "favored_districts": ["Palakkad", "Alappuzha", "Thrissur", "Kottayam", "Ernakulam"],
        "favored_soils": ["Alluvial soil", "Black soil", "Kole wetland clay", "Kuttanad Kari/Kayal soil"]
    },
    "banana": {
        "ph": (6.0, 7.5),
        "temp": (20.0, 35.0),
        "rain": (120.0, 280.0),
        "n": (80, 150),
        "p": (30, 85),
        "k": (100, 220),
        "favored_districts": ["Thrissur", "Wayanad", "Palakkad", "Kottayam", "Malappuram", "Ernakulam", "Idukki"],
        "favored_soils": ["Laterite soil", "Riverine alluvium", "Red loam"]
    },
    "cardamom": {
        "ph": (5.0, 6.5),
        "temp": (15.0, 26.0),
        "rain": (150.0, 380.0),
        "n": (50, 100),
        "p": (25, 60),
        "k": (60, 140),
        "favored_districts": ["Idukki", "Wayanad"],
        "favored_soils": ["Hill soil", "Forest loam"]
    },
    "black_pepper": {
        "ph": (5.2, 6.5),
        "temp": (20.0, 32.0),
        "rain": (150.0, 320.0),
        "n": (60, 120),
        "p": (25, 65),
        "k": (70, 150),
        "favored_districts": ["Idukki", "Wayanad", "Kannur", "Kozhikode", "Kottayam"],
        "favored_soils": ["Hill soil", "Laterite soil", "Forest loam"]
    },
    "ginger": {
        "ph": (5.5, 6.8),
        "temp": (20.0, 30.0),
        "rain": (140.0, 300.0),
        "n": (60, 110),
        "p": (30, 70),
        "k": (60, 130),
        "favored_districts": ["Wayanad", "Idukki", "Palakkad"],
        "favored_soils": ["Laterite soil", "Forest loam", "Sandy loam"]
    },
    "tapioca": {
        "ph": (5.0, 7.0),
        "temp": (22.0, 36.0),
        "rain": (90.0, 260.0),
        "n": (50, 100),
        "p": (30, 70),
        "k": (70, 160),
        "favored_districts": ["Kollam", "Thiruvananthapuram", "Kottayam", "Pathanamthitta"],
        "favored_soils": ["Laterite soil", "Red loam"]
    },
    "okra": {
        "ph": (6.0, 7.2),
        "temp": (22.0, 34.0),
        "rain": (80.0, 220.0),
        "n": (50, 100),
        "p": (30, 70),
        "k": (40, 80),
        "favored_districts": ["Palakkad", "Thrissur", "Ernakulam", "Idukki"],
        "favored_soils": ["Sandy loam", "Laterite soil", "Red loam"]
    },
    "chilli": {
        "ph": (6.0, 7.0),
        "temp": (20.0, 32.0),
        "rain": (70.0, 190.0),
        "n": (60, 110),
        "p": (30, 70),
        "k": (40, 90),
        "favored_districts": ["Palakkad", "Idukki", "Thrissur"],
        "favored_soils": ["Sandy loam", "Laterite soil", "Red loam"]
    }
}

DISTRICTS = [
    "Idukki", "Wayanad", "Palakkad", "Thrissur", "Ernakulam", 
    "Alappuzha", "Kottayam", "Kozhikode", "Kannur", "Kasaragod", 
    "Malappuram", "Kollam", "Pathanamthitta", "Thiruvananthapuram"
]

SOILS = [
    "Hill soil", "Forest loam", "Laterite soil", "Red loam",
    "Black soil", "Alluvial soil", "Coastal sand", "Kole wetland clay",
    "Kuttanad Kari/Kayal soil", "Sandy loam", "Riverine alluvium"
]


def score_profile(crop, district, soil, ph, temp, rain, n, p, k, humidity):
    """Calculates biological fitness score 0-100 to label dataset accurately."""
    opt = CROP_OPTIMALS.get(crop, CROP_OPTIMALS["tomato"])
    score = 0.0

    # 1. District compatibility (15%)
    if district in opt["favored_districts"]:
        score += 15.0
    else:
        score += 7.0

    # 2. Soil compatibility (15%)
    if soil in opt["favored_soils"]:
        score += 15.0
    elif "Laterite" in soil or "loam" in soil:
        score += 9.0
    else:
        score += 4.0

    # 3. pH compatibility (15%)
    min_ph, max_ph = opt["ph"]
    if min_ph <= ph <= max_ph:
        score += 15.0
    elif (min_ph - 0.5) <= ph <= (max_ph + 0.5):
        score += 9.0
    else:
        score += 3.0

    # 4. Temperature compatibility (20%)
    min_t, max_t = opt["temp"]
    if min_t <= temp <= max_t:
        score += 20.0
    elif (min_t - 3.0) <= temp <= (max_t + 3.0):
        score += 11.0
    else:
        score += 2.0

    # 5. Rainfall compatibility (20%)
    min_r, max_r = opt["rain"]
    if min_r <= rain <= max_r:
        score += 20.0
    elif (min_r * 0.7) <= rain <= (max_r * 1.3):
        score += 11.0
    else:
        score += 2.0

    # 6. NPK Nutrition (15%)
    n_match = 1.0 if opt["n"][0] <= n <= opt["n"][1] else 0.5
    p_match = 1.0 if opt["p"][0] <= p <= opt["p"][1] else 0.5
    k_match = 1.0 if opt["k"][0] <= k <= opt["k"][1] else 0.5
    score += (n_match + p_match + k_match) * 5.0

    # Humidity penalty for high-fungal crops
    if crop in ["tomato", "chilli"] and humidity > 88:
        score -= 8.0

    score = max(5.0, min(98.0, score))

    if score >= 75.0:
        category = "High"
    elif score >= 50.0:
        category = "Medium"
    else:
        category = "Low"

    return score, category


def generate_training_data(n_samples=5000):
    np.random.seed(42)
    rows = []
    crop_keys = list(CROP_OPTIMALS.keys())

    for _ in range(n_samples):
        crop = np.random.choice(crop_keys)
        district = np.random.choice(DISTRICTS)
        soil = np.random.choice(SOILS)

        # Generate realistic values with variation
        opt = CROP_OPTIMALS[crop]
        # 60% of the time generate values close to optimal, 40% random realistic
        if np.random.rand() < 0.6:
            ph = np.random.uniform(opt["ph"][0] - 0.4, opt["ph"][1] + 0.4)
            temp = np.random.uniform(opt["temp"][0] - 2, opt["temp"][1] + 2)
            rain = np.random.uniform(opt["rain"][0] - 30, opt["rain"][1] + 50)
            n = np.random.uniform(opt["n"][0] - 15, opt["n"][1] + 20)
            p = np.random.uniform(opt["p"][0] - 10, opt["p"][1] + 15)
            k = np.random.uniform(opt["k"][0] - 15, opt["k"][1] + 25)
            humidity = np.random.uniform(60, 85)
        else:
            ph = np.random.uniform(4.5, 8.5)
            temp = np.random.uniform(14.0, 38.0)
            rain = np.random.uniform(30.0, 450.0)
            n = np.random.uniform(20, 160)
            p = np.random.uniform(10, 95)
            k = np.random.uniform(20, 240)
            humidity = np.random.uniform(40, 98)

        # Add noise
        ph = round(float(ph), 2)
        temp = round(float(temp), 1)
        rain = round(float(rain), 1)
        n = round(float(n), 1)
        p = round(float(p), 1)
        k = round(float(k), 1)
        humidity = round(float(humidity), 1)

        raw_score, category = score_profile(crop, district, soil, ph, temp, rain, n, p, k, humidity)

        rows.append({
            "crop": crop,
            "district": district,
            "soil_type": soil,
            "ph": ph,
            "nitrogen": n,
            "phosphorus": p,
            "potassium": k,
            "temperature": temp,
            "humidity": humidity,
            "rainfall": rain,
            "suitability_category": category,
            "raw_score": raw_score
        })

    return pd.DataFrame(rows)


def train_model():
    print("Generating biological agronomic dataset...")
    df = generate_training_data(n_samples=8000)

    print("Data distribution by category:")
    print(df["suitability_category"].value_counts())

    # Categorical encoders
    crop_encoder = LabelEncoder()
    district_encoder = LabelEncoder()
    soil_encoder = LabelEncoder()

    df["crop_enc"] = crop_encoder.fit_transform(df["crop"])
    df["district_enc"] = district_encoder.fit_transform(df["district"])
    df["soil_enc"] = soil_encoder.fit_transform(df["soil_type"])

    feature_cols = [
        "crop_enc", "district_enc", "soil_enc",
        "ph", "nitrogen", "phosphorus", "potassium",
        "temperature", "humidity", "rainfall"
    ]

    X = df[feature_cols]
    y = df["suitability_category"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=16,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"\nModel Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, preds))

    # Save artifacts
    save_dir = os.path.join(os.path.dirname(__file__), "..", "app", "data", "ml_models")
    os.makedirs(save_dir, exist_ok=True)
    model_file = os.path.join(save_dir, "suitability_model.pkl")

    bundle = {
        "model": clf,
        "feature_cols": feature_cols,
        "crop_encoder": crop_encoder,
        "district_encoder": district_encoder,
        "soil_encoder": soil_encoder,
        "classes": list(clf.classes_)
    }

    joblib.dump(bundle, model_file)
    print(f"\nModel bundle successfully saved to: {model_file}")


if __name__ == "__main__":
    train_model()
