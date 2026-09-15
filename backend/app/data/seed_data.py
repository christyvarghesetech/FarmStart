"""
Curated Agricultural Datasets for FarmStart
Sources: Kerala Agricultural University (KAU) "Package of Practices",
ICAR, Kerala State Seed Development Authority (KSSDA), e-NAM, and Soil Health Card datasets.
"""

KERALA_DISTRICTS = {
    "Idukki": {
        "primary_soil": "Hill soil / Laterite loam",
        "soil_types": ["Hill soil", "Forest loam", "Laterite soil"],
        "default_npk": {"N": 75, "P": 42, "K": 58, "ph": 5.8},
        "climate_zone": "Highland / Cool Temperate",
        "avg_annual_rainfall_mm": 3200,
        "lat": 9.8494,
        "lon": 76.9814
    },
    "Wayanad": {
        "primary_soil": "Forest loam / Red loam",
        "soil_types": ["Forest loam", "Red loam", "Laterite soil"],
        "default_npk": {"N": 80, "P": 45, "K": 62, "ph": 5.7},
        "climate_zone": "Highland / Sub-tropical",
        "avg_annual_rainfall_mm": 2800,
        "lat": 11.6854,
        "lon": 76.1320
    },
    "Palakkad": {
        "primary_soil": "Black soil & Red loam",
        "soil_types": ["Black soil", "Red loam", "Laterite soil", "Alluvial soil"],
        "default_npk": {"N": 85, "P": 50, "K": 65, "ph": 6.8},
        "climate_zone": "Midland / Dry Plains",
        "avg_annual_rainfall_mm": 1800,
        "lat": 10.7867,
        "lon": 76.6548
    },
    "Thrissur": {
        "primary_soil": "Laterite soil & Kole wetlands",
        "soil_types": ["Laterite soil", "Kole wetland clay", "Alluvial soil"],
        "default_npk": {"N": 78, "P": 40, "K": 55, "ph": 6.2},
        "climate_zone": "Midland & Coastal",
        "avg_annual_rainfall_mm": 2900,
        "lat": 10.5276,
        "lon": 76.2144
    },
    "Ernakulam": {
        "primary_soil": "Coastal alluvium & Pokkali saline clay",
        "soil_types": ["Coastal alluvium", "Pokkali saline soil", "Laterite soil"],
        "default_npk": {"N": 72, "P": 38, "K": 50, "ph": 6.4},
        "climate_zone": "Coastal Lowland",
        "avg_annual_rainfall_mm": 3000,
        "lat": 9.9816,
        "lon": 76.2999
    },
    "Alappuzha": {
        "primary_soil": "Coastal sand & Kuttanad peaty clay",
        "soil_types": ["Kuttanad Kari/Kayal soil", "Coastal sand", "Alluvial soil"],
        "default_npk": {"N": 70, "P": 35, "K": 48, "ph": 5.4},
        "climate_zone": "Coastal & Lowland Wetland",
        "avg_annual_rainfall_mm": 2800,
        "lat": 9.4981,
        "lon": 76.3388
    },
    "Kottayam": {
        "primary_soil": "Laterite soil & Riverine alluvium",
        "soil_types": ["Laterite soil", "Riverine alluvium"],
        "default_npk": {"N": 80, "P": 44, "K": 60, "ph": 6.0},
        "climate_zone": "Midland",
        "avg_annual_rainfall_mm": 3100,
        "lat": 9.5916,
        "lon": 76.5222
    },
    "Kozhikode": {
        "primary_soil": "Laterite soil & Coastal sand",
        "soil_types": ["Laterite soil", "Coastal sand"],
        "default_npk": {"N": 76, "P": 40, "K": 52, "ph": 6.1},
        "climate_zone": "Coastal & Midland",
        "avg_annual_rainfall_mm": 3300,
        "lat": 11.2588,
        "lon": 75.7804
    },
    "Kannur": {
        "primary_soil": "Laterite soil",
        "soil_types": ["Laterite soil", "Coastal sand"],
        "default_npk": {"N": 75, "P": 38, "K": 50, "ph": 6.0},
        "climate_zone": "Coastal & Midland",
        "avg_annual_rainfall_mm": 3400,
        "lat": 11.8745,
        "lon": 75.3704
    },
    "Kasaragod": {
        "primary_soil": "Laterite soil & Coastal alluvium",
        "soil_types": ["Laterite soil", "Coastal alluvium"],
        "default_npk": {"N": 74, "P": 36, "K": 49, "ph": 5.9},
        "climate_zone": "Coastal & Midland",
        "avg_annual_rainfall_mm": 3500,
        "lat": 12.4996,
        "lon": 74.9869
    },
    "Malappuram": {
        "primary_soil": "Laterite soil",
        "soil_types": ["Laterite soil", "Riverine alluvium"],
        "default_npk": {"N": 77, "P": 39, "K": 53, "ph": 6.1},
        "climate_zone": "Midland",
        "avg_annual_rainfall_mm": 2900,
        "lat": 11.0510,
        "lon": 76.0711
    },
    "Kollam": {
        "primary_soil": "Laterite soil & Coastal alluvium",
        "soil_types": ["Laterite soil", "Coastal alluvium"],
        "default_npk": {"N": 75, "P": 42, "K": 56, "ph": 6.3},
        "climate_zone": "Coastal & Midland",
        "avg_annual_rainfall_mm": 2700,
        "lat": 8.8932,
        "lon": 76.6141
    },
    "Pathanamthitta": {
        "primary_soil": "Laterite soil & Hill soil",
        "soil_types": ["Laterite soil", "Hill soil"],
        "default_npk": {"N": 79, "P": 41, "K": 57, "ph": 5.9},
        "climate_zone": "Midland & Highland",
        "avg_annual_rainfall_mm": 2800,
        "lat": 9.2648,
        "lon": 76.7870
    },
    "Thiruvananthapuram": {
        "primary_soil": "Red loam & Laterite soil",
        "soil_types": ["Red loam", "Laterite soil", "Coastal sand"],
        "default_npk": {"N": 76, "P": 44, "K": 54, "ph": 6.5},
        "climate_zone": "Southern Midland & Coastal",
        "avg_annual_rainfall_mm": 1800,
        "lat": 8.5241,
        "lon": 76.9366
    }
}

CROPS_CATALOG = [
    {
        "id": "tomato",
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "category": "Vegetables",
        "ideal_soil_types": ["Hill soil", "Laterite soil", "Red loam", "Sandy loam"],
        "ideal_ph_range": [5.8, 7.0],
        "ideal_temp_c": [18, 28],
        "ideal_monthly_rainfall_mm": [100, 220],
        "sowing_season": "Post-Monsoon / Cool Season (September to November)",
        "promising_districts": ["Idukki", "Wayanad", "Palakkad", "Kottayam"],
        "recommended_varieties": ["PKM-1", "Vellayani Vijay", "Anagha", "Akshaya (F1 Hybrid)", "Manulakshmi"],
        "maturity_days": "75 - 90 days",
        "notes": "Sensitive to waterlogging and high humidity fungal blight. Raised beds with mulching are recommended in highland areas like Idukki."
    },
    {
        "id": "rice",
        "name": "Rice (Paddy)",
        "scientific_name": "Oryza sativa",
        "category": "Cereals",
        "ideal_soil_types": ["Alluvial soil", "Black soil", "Kole wetland clay", "Kuttanad Kari/Kayal soil"],
        "ideal_ph_range": [5.5, 7.2],
        "ideal_temp_c": [22, 35],
        "ideal_monthly_rainfall_mm": [180, 350],
        "sowing_season": "Virippu (May-June), Mundakan (Sept-Oct), Puncha (Dec-Jan)",
        "promising_districts": ["Palakkad", "Alappuzha", "Thrissur", "Kottayam", "Ernakulam"],
        "recommended_varieties": ["Jyothi", "Uma (MO 16)", "Prathyasha", "Kanchana", "Shreyas", "Ezhome-1"],
        "maturity_days": "115 - 135 days",
        "notes": "Needs standing water during vegetative stage; tolerant to clayey wetland soils."
    },
    {
        "id": "banana",
        "name": "Banana",
        "scientific_name": "Musa acuminata",
        "category": "Fruits",
        "ideal_soil_types": ["Laterite soil", "Riverine alluvium", "Red loam"],
        "ideal_ph_range": [6.0, 7.5],
        "ideal_temp_c": [20, 35],
        "ideal_monthly_rainfall_mm": [150, 280],
        "sowing_season": "August to October (Nendran) and April to May",
        "promising_districts": ["Thrissur", "Wayanad", "Palakkad", "Kottayam", "Malappuram", "Ernakulam"],
        "recommended_varieties": ["Nendran", "Grand Naine", "Robusta", "Poovan", "Red Banana (Chenkadali)"],
        "maturity_days": "270 - 330 days",
        "notes": "Requires deep well-drained fertile loam rich in potassium and organic matter."
    },
    {
        "id": "cardamom",
        "name": "Cardamom (Small)",
        "scientific_name": "Elettaria cardamomum",
        "category": "Spices",
        "ideal_soil_types": ["Hill soil", "Forest loam"],
        "ideal_ph_range": [5.0, 6.5],
        "ideal_temp_c": [15, 26],
        "ideal_monthly_rainfall_mm": [150, 350],
        "sowing_season": "June to July (onset of monsoon planting of suckers)",
        "promising_districts": ["Idukki", "Wayanad", "Palakkad"],
        "recommended_varieties": ["Appangala-1", "IISR Vijetha", "Mudigere-1", "Njallani (Green Gold)"],
        "maturity_days": "Perennial (first harvest at 2-3 years)",
        "notes": "Known as the Queen of Spices. Thrives under partial forest canopy in high altitude (600-1500m) cool hill slopes."
    },
    {
        "id": "black_pepper",
        "name": "Black Pepper",
        "scientific_name": "Piper nigrum",
        "category": "Spices",
        "ideal_soil_types": ["Hill soil", "Laterite soil", "Forest loam"],
        "ideal_ph_range": [5.5, 6.5],
        "ideal_temp_c": [20, 32],
        "ideal_monthly_rainfall_mm": [150, 300],
        "sowing_season": "May to June (onset of South-West monsoon)",
        "promising_districts": ["Idukki", "Wayanad", "Kannur", "Kozhikode", "Kottayam"],
        "recommended_varieties": ["Panniyur-1", "Panniyur-5", "Karimunda", "IISR Thevam", "Vijay"],
        "maturity_days": "Perennial vine",
        "notes": "Requires good drainage; susceptible to Phytophthora foot rot if soil remains waterlogged."
    },
    {
        "id": "ginger",
        "name": "Ginger",
        "scientific_name": "Zingiber officinale",
        "category": "Spices",
        "ideal_soil_types": ["Laterite soil", "Forest loam", "Sandy loam"],
        "ideal_ph_range": [5.5, 6.8],
        "ideal_temp_c": [20, 30],
        "ideal_monthly_rainfall_mm": [150, 300],
        "sowing_season": "First fortnight of April with pre-monsoon showers",
        "promising_districts": ["Wayanad", "Idukki", "Palakkad", "Kottayam"],
        "recommended_varieties": ["Maran", "Rio-de-Janeiro", "Mahima", "Varada", "Karthika"],
        "maturity_days": "210 - 240 days",
        "notes": "Heavy mulching with green leaves is essential to conserve moisture and suppress weeds."
    },
    {
        "id": "tapioca",
        "name": "Tapioca (Cassava)",
        "scientific_name": "Manihot esculenta",
        "category": "Tubers",
        "ideal_soil_types": ["Laterite soil", "Red loam"],
        "ideal_ph_range": [5.0, 7.0],
        "ideal_temp_c": [22, 35],
        "ideal_monthly_rainfall_mm": [100, 250],
        "sowing_season": "April-May (Monsoon crop) or Sept-Oct (Second crop)",
        "promising_districts": ["Kollam", "Thiruvananthapuram", "Kottayam", "Pathanamthitta", "Malappuram"],
        "recommended_varieties": ["M-4", "Sree Padmanabha", "Sree Pavithra", "Sree Raksha", "Vellayani Hraswa"],
        "maturity_days": "180 - 270 days",
        "notes": "Extremely hardy and drought-tolerant once established. High starch content."
    },
    {
        "id": "okra",
        "name": "Okra (Bhindi)",
        "scientific_name": "Abelmoschus esculentus",
        "category": "Vegetables",
        "ideal_soil_types": ["Sandy loam", "Laterite soil", "Alluvial soil", "Red loam"],
        "ideal_ph_range": [6.0, 7.2],
        "ideal_temp_c": [22, 34],
        "ideal_monthly_rainfall_mm": [80, 200],
        "sowing_season": "February - March (Summer) and June - July (Kharif)",
        "promising_districts": ["Palakkad", "Thrissur", "Ernakulam", "Kollam", "Idukki"],
        "recommended_varieties": ["Susthira", "Kiran", "Arka Anamika", "Varsha Uphar"],
        "maturity_days": "50 - 65 days",
        "notes": "Fast yielding cash vegetable. Resistant to Yellow Vein Mosaic Virus (YVMV) recommended."
    },
    {
        "id": "chilli",
        "name": "Chilli",
        "scientific_name": "Capsicum annuum",
        "category": "Vegetables",
        "ideal_soil_types": ["Sandy loam", "Laterite soil", "Red loam"],
        "ideal_ph_range": [6.0, 7.0],
        "ideal_temp_c": [20, 32],
        "ideal_monthly_rainfall_mm": [80, 180],
        "sowing_season": "September - October and January - February",
        "promising_districts": ["Palakkad", "Idukki", "Thrissur", "Thiruvananthapuram"],
        "recommended_varieties": ["Ujjwala", "Vellayani Athulya", "Jwalamukhi", "Anugraha"],
        "maturity_days": "75 - 90 days",
        "notes": "Requires well-drained soil. High bacterial wilt resistance in Kerala varieties like Ujjwala."
    }
]

SEED_PRICES = [
    {
        "crop_id": "tomato",
        "crop_name": "Tomato",
        "region": "Idukki",
        "min_price": 350.0,
        "max_price": 450.0,
        "modal_price": 390.0,
        "unit": "per 100g certified seed",
        "source": "KSSDA / e-NAM Reference Rate",
        "varieties": [
            {"variety": "PKM-1", "price": 360.0, "type": "Open Pollinated"},
            {"variety": "Vellayani Vijay", "price": 380.0, "type": "KAU Certified"},
            {"variety": "Akshaya (F1 Hybrid)", "price": 440.0, "type": "Commercial Hybrid"}
        ]
    },
    {
        "crop_id": "tomato",
        "crop_name": "Tomato",
        "region": "Wayanad",
        "min_price": 340.0,
        "max_price": 430.0,
        "modal_price": 380.0,
        "unit": "per 100g certified seed",
        "source": "KSSDA Reference Rate",
        "varieties": [
            {"variety": "PKM-1", "price": 350.0, "type": "Open Pollinated"},
            {"variety": "Anagha", "price": 390.0, "type": "KAU Certified"}
        ]
    },
    {
        "crop_id": "tomato",
        "crop_name": "Tomato",
        "region": "Palakkad",
        "min_price": 330.0,
        "max_price": 420.0,
        "modal_price": 375.0,
        "unit": "per 100g certified seed",
        "source": "e-NAM APMC Palakkad",
        "varieties": [
            {"variety": "PKM-1", "price": 340.0, "type": "Open Pollinated"},
            {"variety": "Akshaya", "price": 415.0, "type": "Commercial Hybrid"}
        ]
    },
    {
        "crop_id": "rice",
        "crop_name": "Rice (Paddy)",
        "region": "Palakkad",
        "min_price": 42.0,
        "max_price": 58.0,
        "modal_price": 48.0,
        "unit": "per kg foundation/certified seed",
        "source": "Kerala State Seed Development Authority (KSSDA)",
        "varieties": [
            {"variety": "Jyothi", "price": 46.0, "type": "Certified"},
            {"variety": "Uma (MO 16)", "price": 48.0, "type": "Certified"},
            {"variety": "Kanchana", "price": 52.0, "type": "Certified"}
        ]
    },
    {
        "crop_id": "rice",
        "crop_name": "Rice (Paddy)",
        "region": "Alappuzha",
        "min_price": 44.0,
        "max_price": 60.0,
        "modal_price": 50.0,
        "unit": "per kg foundation/certified seed",
        "source": "KSSDA / Krishi Bhavan Alappuzha",
        "varieties": [
            {"variety": "Uma (MO 16)", "price": 48.0, "type": "Certified"},
            {"variety": "Prathyasha", "price": 54.0, "type": "Certified"}
        ]
    },
    {
        "crop_id": "banana",
        "crop_name": "Banana",
        "region": "Thrissur",
        "min_price": 18.0,
        "max_price": 28.0,
        "modal_price": 22.0,
        "unit": "per tissue culture sucker / plantlet",
        "source": "KAU Vellanikkara Nursery Rates",
        "varieties": [
            {"variety": "Nendran (TC)", "price": 24.0, "type": "Tissue Culture"},
            {"variety": "Grand Naine", "price": 20.0, "type": "Tissue Culture"},
            {"variety": "Robusta", "price": 19.0, "type": "Tissue Culture"}
        ]
    },
    {
        "crop_id": "banana",
        "crop_name": "Banana",
        "region": "Idukki",
        "min_price": 20.0,
        "max_price": 30.0,
        "modal_price": 25.0,
        "unit": "per tissue culture sucker / plantlet",
        "source": "VFPCK / KAU Nursery",
        "varieties": [
            {"variety": "Nendran (TC)", "price": 26.0, "type": "Tissue Culture"},
            {"variety": "Red Banana", "price": 28.0, "type": "Sucker"}
        ]
    },
    {
        "crop_id": "cardamom",
        "crop_name": "Cardamom (Small)",
        "region": "Idukki",
        "min_price": 110.0,
        "max_price": 175.0,
        "modal_price": 135.0,
        "unit": "per clonal plantlet / nursery bag seedling",
        "source": "Spices Board Spices Park Puttady / ICAR-IISR",
        "varieties": [
            {"variety": "Appangala-1", "price": 130.0, "type": "Clonal certified"},
            {"variety": "IISR Vijetha", "price": 140.0, "type": "Viral tolerant"},
            {"variety": "Njallani", "price": 160.0, "type": "High yielding clone"}
        ]
    },
    {
        "crop_id": "black_pepper",
        "crop_name": "Black Pepper",
        "region": "Idukki",
        "min_price": 25.0,
        "max_price": 45.0,
        "modal_price": 32.0,
        "unit": "per rooted cutting in polybag",
        "source": "ICAR-IISR Kozhikode & KAU Cardamom Research Station",
        "varieties": [
            {"variety": "Panniyur-1", "price": 30.0, "type": "Rooted cutting"},
            {"variety": "Karimunda", "price": 32.0, "type": "Rooted cutting"},
            {"variety": "IISR Thevam", "price": 40.0, "type": "Tolerant variety"}
        ]
    },
    {
        "crop_id": "ginger",
        "crop_name": "Ginger",
        "region": "Wayanad",
        "min_price": 115.0,
        "max_price": 155.0,
        "modal_price": 130.0,
        "unit": "per kg healthy seed rhizome",
        "source": "Wayanad Seed Market / e-NAM",
        "varieties": [
            {"variety": "Maran", "price": 125.0, "type": "Local selection"},
            {"variety": "Rio-de-Janeiro", "price": 135.0, "type": "Certified rhizome"},
            {"variety": "Mahima", "price": 145.0, "type": "Nematode resistant"}
        ]
    },
    {
        "crop_id": "okra",
        "crop_name": "Okra (Bhindi)",
        "region": "Palakkad",
        "min_price": 170.0,
        "max_price": 250.0,
        "modal_price": 210.0,
        "unit": "per 100g certified seed",
        "source": "KSSDA",
        "varieties": [
            {"variety": "Susthira", "price": 195.0, "type": "KAU Certified"},
            {"variety": "Arka Anamika", "price": 180.0, "type": "IIHR Certified"}
        ]
    },
    {
        "crop_id": "chilli",
        "crop_name": "Chilli",
        "region": "Idukki",
        "min_price": 260.0,
        "max_price": 360.0,
        "modal_price": 300.0,
        "unit": "per 100g certified seed",
        "source": "KSSDA",
        "varieties": [
            {"variety": "Ujjwala", "price": 290.0, "type": "KAU Wilt-Resistant"},
            {"variety": "Vellayani Athulya", "price": 320.0, "type": "KAU High Yield"}
        ]
    }
]

SOWING_CALENDARS = [
    {
        "crop_id": "tomato",
        "region": "Idukki",
        "season_name": "Post-Monsoon Winter Sowing",
        "start_date": "09-15", # Sept 15
        "end_date": "11-15",   # Nov 15
        "safe_rainfall_min_mm": 50,
        "safe_rainfall_max_mm": 200,
        "safe_temp_min_c": 16,
        "safe_temp_max_c": 28,
        "sowing_tips": "Ideal sowing window in Idukki high ranges. Construct raised beds (15-20cm height) with silver-black plastic mulch to avoid soil-borne pathogens."
    },
    {
        "crop_id": "tomato",
        "region": "General",
        "season_name": "Cool Season Vegetable Window",
        "start_date": "09-20",
        "end_date": "11-30",
        "safe_rainfall_min_mm": 40,
        "safe_rainfall_max_mm": 220,
        "safe_temp_min_c": 18,
        "safe_temp_max_c": 30,
        "sowing_tips": "Transplant 25-30 day old sturdy seedlings in evening hours. Protect from heavy cloudbursts."
    },
    {
        "crop_id": "rice",
        "region": "Palakkad",
        "season_name": "Mundakan (Winter Paddy)",
        "start_date": "09-15",
        "end_date": "10-25",
        "safe_rainfall_min_mm": 120,
        "safe_rainfall_max_mm": 350,
        "safe_temp_min_c": 22,
        "safe_temp_max_c": 34,
        "sowing_tips": "Mundakan season planting using medium duration varieties like Uma (MO 16) or Jyothi."
    },
    {
        "crop_id": "rice",
        "region": "Alappuzha",
        "season_name": "Puncha Season (Summer Paddy)",
        "start_date": "11-15",
        "end_date": "12-31",
        "safe_rainfall_min_mm": 50,
        "safe_rainfall_max_mm": 180,
        "safe_temp_min_c": 23,
        "safe_temp_max_c": 33,
        "sowing_tips": "Dewater Kuttanad polders, level soil, and sow pre-germinated seeds."
    },
    {
        "crop_id": "cardamom",
        "region": "Idukki",
        "season_name": "South-West Monsoon Planting",
        "start_date": "06-01",
        "end_date": "07-31",
        "safe_rainfall_min_mm": 200,
        "safe_rainfall_max_mm": 500,
        "safe_temp_min_c": 15,
        "safe_temp_max_c": 26,
        "sowing_tips": "Plant suckers in pits with compost and rock phosphate along contour terraces."
    },
    {
        "crop_id": "black_pepper",
        "region": "Idukki",
        "season_name": "Monsoon Vine Planting",
        "start_date": "05-25",
        "end_date": "07-15",
        "safe_rainfall_min_mm": 180,
        "safe_rainfall_max_mm": 450,
        "safe_temp_min_c": 18,
        "safe_temp_max_c": 32,
        "sowing_tips": "Plant 2-3 rooted pepper cuttings on North-Eastern side of live support trees."
    },
    {
        "crop_id": "banana",
        "region": "Thrissur",
        "season_name": "Onam Season Crop Planting",
        "start_date": "08-15",
        "end_date": "10-15",
        "safe_rainfall_min_mm": 100,
        "safe_rainfall_max_mm": 300,
        "safe_temp_min_c": 22,
        "safe_temp_max_c": 35,
        "sowing_tips": "Select sword suckers of 3-4 months age or certified tissue culture plantlets."
    }
]

GOVERNMENT_SCHEMES = [
    {
        "id": "subhiksha-keralam",
        "title": "Subhiksha Keralam Integrated Food Security Mission",
        "department": "Department of Agriculture Development and Farmers' Welfare, Govt. of Kerala",
        "target_crops": ["tomato", "rice", "banana", "tapioca", "vegetables"],
        "eligibility": "First-time farmers, individual cultivators, Kudumbashree groups and self-help collectives in Kerala",
        "benefits": "Financial assistance of ₹20,000 - ₹30,000 per hectare for fallow land vegetable and tuber farming, subsidized seed packets and micro-irrigation kits.",
        "application_mode": "Online via AIMS Portal (aims.kerala.gov.in) or nearest Krishi Bhavan",
        "documentation": "Aadhaar, Land possession certificate / Lease deed, Bank passbook"
    },
    {
        "id": "pm-kisan",
        "title": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "department": "Ministry of Agriculture & Farmers Welfare, Govt. of India",
        "target_crops": ["all"],
        "eligibility": "All landholding farmer families with cultivable land holdings",
        "benefits": "Direct income support of ₹6,000 per year paid in three equal installments of ₹2,000 directly into Aadhaar-linked bank accounts.",
        "application_mode": "pmkisan.gov.in or Akshaya / CSC Centres",
        "documentation": "Aadhaar Card, Land ownership record (RoR), Bank details"
    },
    {
        "id": "pmfby-crop-insurance",
        "title": "Pradhan Mantri Fasal Bima Yojana (PMFBY / Restructured WBCIS)",
        "department": "Agricultural Insurance Company of India / State Agriculture Dept",
        "target_crops": ["rice", "banana", "cardamom", "black_pepper", "ginger", "tapioca"],
        "eligibility": "All farmers growing notified crops in notified areas (both loanee and non-loanee)",
        "benefits": "Comprehensive risk insurance against unseasonal rainfall, floods, landslides, drought. Farmers pay nominal premium (1.5% - 2% for food crops, 5% for horticultural crops).",
        "application_mode": "Krishi Bhavan or pmfby.gov.in before cutoff date",
        "documentation": "Land tax receipt, Sowing certificate from Agricultural Officer, Aadhaar"
    },
    {
        "id": "midh-horticulture",
        "title": "Mission for Integrated Development of Horticulture (MIDH - SHM Kerala)",
        "department": "State Horticulture Mission Kerala",
        "target_crops": ["tomato", "chilli", "cardamom", "black_pepper", "banana"],
        "eligibility": "Small and marginal farmers establishing polyhouses, drip irrigation, or shade-net nurseries",
        "benefits": "Up to 50% capital subsidy for drip irrigation systems, plastic mulching, polyhouse setup, and precision farming infrastructure.",
        "application_mode": "Through District Mission Director / State Horticulture Mission",
        "documentation": "Project proposal, Land documents, Bank account, Soil test report"
    },
    {
        "id": "kssda-seed-subsidy",
        "title": "KSSDA Certified Seed Distribution Subsidy",
        "department": "Kerala State Seed Development Authority",
        "target_crops": ["rice", "tomato", "okra", "chilli", "vegetables"],
        "eligibility": "Small and marginal farmers registered with local Krishi Bhavan",
        "benefits": "Subsidized certified seeds at 25% - 50% discount compared to open market retail rates.",
        "application_mode": "Direct purchase at local Krishi Bhavan or KSSDA retail outlets",
        "documentation": "Farmer registration card / Aadhaar"
    }
]
