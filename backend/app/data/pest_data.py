# -*- coding: utf-8 -*-
"""
Kerala Agricultural University (KAU) Integrated Pest Management (IPM) Dataset
Contains pest and disease profiles for Kerala crops, meteorological triggers,
and dual-track (Organic Bio-remedy vs. Emergency Chemical) control protocols.
"""

KAU_PEST_PROFILES = [
    # --- TOMATO ---
    {
        "id": "tomato_fruit_borer",
        "crop_ids": ["tomato"],
        "name": "Tomato Fruit Borer",
        "scientific_name": "Helicoverpa armigera",
        "category": "Insect Pest",
        "symptom_part": "fruit",
        "severity": "HIGH",
        "symptoms": [
            "Circular bore holes on developing and ripe fruits",
            "Caterpillars seen feeding with only anterior body inside the tomato",
            "Rotting of attacked fruit due to secondary bacterial invasion",
            "Premature flower and bud dropping"
        ],
        "weather_triggers": {
            "min_temp_c": 20.0,
            "max_temp_c": 32.0,
            "min_humidity_pct": 50,
            "max_humidity_pct": 85,
            "description": "Warm, sunny days following light intermittent showers favor rapid egg hatching and larval activity."
        },
        "organic_remedy": {
            "title": "Neem-Garlic Soap Emulsion + Bt Spray",
            "preparation": "Crush 20g garlic cloves and mix with 50ml neem oil (Azadirachtin 1500 ppm). Dilute in 1 liter of water containing 10g dissolved bar soap. Alternatively, spray Bacillus thuringiensis (Bt) @ 2g/liter in evening hours.",
            "application_interval": "Spray twice at 10-day intervals during flowering and early fruit set."
        },
        "chemical_remedy": {
            "title": "Chlorantraniliprole 18.5% SC",
            "dosage": "0.3 ml per liter of water (60 ml/acre)",
            "phi_days": 3,
            "safety_note": "Target early instar larvae. Do not spray during peak honeybee foraging hours (morning 8–11 AM)."
        },
        "preventative_ipm": [
            "Install yellow and blue sticky traps (10 traps/acre)",
            "Set up Helilure pheromone traps @ 5 traps/acre for adult moth monitoring",
            "Plant African Marigold (Tagetes erecta) as a trap crop around tomato borders (1 row every 16 rows)"
        ]
    },
    {
        "id": "tomato_late_blight",
        "crop_ids": ["tomato"],
        "name": "Late Blight / Fungal Blight",
        "scientific_name": "Phytophthora infestans",
        "category": "Fungal Blight",
        "symptom_part": "leaf",
        "severity": "HIGH",
        "symptoms": [
            "Water-soaked irregular pale green lesions on leaves turning dark brown/purplish",
            "White downy fungal growth on the underside of leaves during cool, moist mornings",
            "Dark brown, firm lesions with greasy appearance on green fruits",
            "Rapid collapse and rotting of entire foliage (looks frost-burned)"
        ],
        "weather_triggers": {
            "min_temp_c": 12.0,
            "max_temp_c": 24.0,
            "min_humidity_pct": 80,
            "max_humidity_pct": 100,
            "description": "Prolonged leaf wetness, cool nights (15-20°C), and relative humidity above 80% create an extreme fungal outbreak risk."
        },
        "organic_remedy": {
            "title": "Bordeaux Mixture 1% / Pseudomonas fluorescens",
            "preparation": "Dissolve 100g copper sulfate in 5L water and 100g quicklime in 5L water; pour copper solution into lime solution while stirring continuously. Spray fresh. Alternatively, spray liquid Pseudomonas fluorescens @ 20g/L.",
            "application_interval": "Apply prophylactically before rainy spells, repeat after 7–10 days."
        },
        "chemical_remedy": {
            "title": "Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ)",
            "dosage": "2.0 g per liter of water",
            "phi_days": 7,
            "safety_note": "Use as an emergency rescue spray when active lesions exceed 5% of leaf canopy."
        },
        "preventative_ipm": [
            "Use raised beds with silver-black polyethylene mulch to prevent soil splashing onto foliage",
            "Avoid overhead sprinkler irrigation; use drip lines at the base",
            "Maintain 60cm plant spacing for adequate air circulation in high-altitude zones like Idukki"
        ]
    },
    {
        "id": "tomato_bacterial_wilt",
        "crop_ids": ["tomato", "chilli", "okra"],
        "name": "Bacterial Wilt",
        "scientific_name": "Ralstonia solanacearum",
        "category": "Bacterial Wilt",
        "symptom_part": "stem",
        "severity": "HIGH",
        "symptoms": [
            "Sudden daytime wilting of entire plant while leaves remain green",
            "Vascular discoloration: vascular ring inside stem turns dark brown",
            "Bacterial ooze test: white milky bacterial streams emerge when cut stem is placed in clear water glass",
            "Stunted growth and irreversible collapse within 2–4 days"
        ],
        "weather_triggers": {
            "min_temp_c": 24.0,
            "max_temp_c": 35.0,
            "min_humidity_pct": 70,
            "max_humidity_pct": 95,
            "description": "Warm soil temperatures and high soil moisture accelerate root invasion and xylem blockage."
        },
        "organic_remedy": {
            "title": "Pseudomonas fluorescens + Lime Soil Drench",
            "preparation": "Mix 20g Pseudomonas fluorescens talc formulation per liter of water and drench seedling root zone. Broadcast agricultural lime @ 250 kg/acre 2 weeks before planting to adjust soil pH above 6.2.",
            "application_interval": "Drench at planting and repeat at 20 and 40 days after transplanting."
        },
        "chemical_remedy": {
            "title": "Streptocycline + Copper Oxychloride",
            "dosage": "Streptocycline @ 0.1g + Copper Oxychloride 50% WP @ 2.5g per liter of water",
            "phi_days": 10,
            "safety_note": "Soil drench the base of neighboring plants to quarantine infection pockets."
        },
        "preventative_ipm": [
            "Select KAU wilt-resistant varieties: 'Anagha', 'Akshaya', and 'Sakthi'",
            "Rotate crops with non-solanaceous crops (e.g., Rice/Paddy or Maize)",
            "Rogue out and burn infected plants immediately; do not compost wilted vines"
        ]
    },

    # --- RICE / PADDY ---
    {
        "id": "rice_brown_planthopper",
        "crop_ids": ["rice"],
        "name": "Brown Planthopper (BPH)",
        "scientific_name": "Nilaparvata lugens",
        "category": "Insect Pest",
        "symptom_part": "stem",
        "severity": "HIGH",
        "symptoms": [
            "Circular patches of dried, golden-brown plants known as 'hopperburn'",
            "Large clusters of small brown nymphs and adults crowding the base of tillers above water level",
            "Sooty mold fungus developing on honeydew secreted by hoppers",
            "Chaffy, unfilled grains and lodging of plants"
        ],
        "weather_triggers": {
            "min_temp_c": 22.0,
            "max_temp_c": 33.0,
            "min_humidity_pct": 75,
            "max_humidity_pct": 98,
            "description": "High humidity, dense canopy microclimate, and cloudy weather trigger rapid population explosions."
        },
        "organic_remedy": {
            "title": "Beauveria bassiana / Neem Kernel Extract (NSKE 5%)",
            "preparation": "Spray Beauveria bassiana entomopathogenic fungus @ 5g/liter directed specifically at the base of tillers. Alternatively, spray 5% Neem Seed Kernel Extract (NSKE).",
            "application_interval": "Apply when hopper count exceeds 1–2 nymphs per tiller."
        },
        "chemical_remedy": {
            "title": "Triflumuron 20% + Pymetrozine 50% WDG",
            "dosage": "0.6 g per liter of water (120 g/acre)",
            "phi_days": 15,
            "safety_note": "Drain standing water from field before spraying directly at the tiller base."
        },
        "preventative_ipm": [
            "Form 'alleyways' (skip one row every 2 meters) to allow sunlight and wind penetration into the canopy",
            "Avoid excessive nitrogen fertilizer (urea); split application into 3 doses with potassium balance",
            "Conserve natural predators: Mirid bugs (Cyrtorhinus lividipennis) and spiders"
        ]
    },
    {
        "id": "rice_blast",
        "crop_ids": ["rice"],
        "name": "Rice Blast Disease",
        "scientific_name": "Magnaporthe oryzae",
        "category": "Fungal Blight",
        "symptom_part": "leaf",
        "severity": "HIGH",
        "symptoms": [
            "Spindle-shaped (eye-shaped) spots on leaves with greyish-white centers and dark reddish-brown margins",
            "Neck rot: panicle node turns black and breaks, causing empty, upright whitish panicles",
            "Lesions coalescing to scorch the entire leaf blade"
        ],
        "weather_triggers": {
            "min_temp_c": 18.0,
            "max_temp_c": 28.0,
            "min_humidity_pct": 85,
            "max_humidity_pct": 100,
            "description": "Continuous dew, high relative humidity (>85%), and cool night temperatures favor spore germination."
        },
        "organic_remedy": {
            "title": "Pseudomonas fluorescens Seed & Foliar Spray",
            "preparation": "Seed treatment with Pseudomonas fluorescens @ 10g/kg seed. Foliar spray liquid formulation @ 10ml/L at tillering and boot leaf stage.",
            "application_interval": "Apply at the first appearance of leaf spots."
        },
        "chemical_remedy": {
            "title": "Tricyclazole 75% WP",
            "dosage": "0.6 g per liter of water (120 g/acre)",
            "phi_days": 21,
            "safety_note": "Most effective preventative fungicide against neck blast stage."
        },
        "preventative_ipm": [
            "Grow resistant varieties approved for Kerala: 'Uma (MO 16)', 'Jyothi', and 'Kanchana'",
            "Avoid late sowing and excessive top-dressing of urea during cloudy monsoon weeks"
        ]
    },

    # --- BANANA ---
    {
        "id": "banana_pseudostem_weevil",
        "crop_ids": ["banana"],
        "name": "Banana Pseudostem Weevil",
        "scientific_name": "Odoiporus longicollis",
        "category": "Insect Pest",
        "symptom_part": "stem",
        "severity": "HIGH",
        "symptoms": [
            "Pin-head sized holes on the lower pseudostem with transparent jelly-like sap exudation",
            "Extensive internal tunneling and rotting of the central core by creamy-white grubs",
            "Premature yellowing and drying of outer leaves",
            "Stem snapped in moderate breeze, failing to support bunch weight"
        ],
        "weather_triggers": {
            "min_temp_c": 20.0,
            "max_temp_c": 35.0,
            "min_humidity_pct": 60,
            "max_humidity_pct": 90,
            "description": "Weevils are active year-round in humid tropical Kerala, with peak egg-laying starting from the 5th month of planting."
        },
        "organic_remedy": {
            "title": "Beauveria bassiana / Entomopathogenic Nematodes (EPN)",
            "preparation": "Swab or spray Beauveria bassiana (10^8 spores/ml) @ 20ml/L on the pseudostem. Insert longitudinal split pseudostem traps (50cm pieces) smeared with Beauveria @ 20 traps/acre.",
            "application_interval": "Apply starting from the 5th month after planting at 45-day intervals."
        },
        "chemical_remedy": {
            "title": "Chlorpyrifos 20% EC or Fipronil 5% SC",
            "dosage": "Chlorpyrifos @ 2.5 ml/L applied into the leaf axils of the lower stem",
            "phi_days": 30,
            "safety_note": "Do not spray pseudostem within 30 days of fruit harvest."
        },
        "preventative_ipm": [
            "Clean and pare banana suckers: peel outer dead layers and dip in hot water (50°C for 10 min) before planting",
            "Remove dried drooping leaves from the lower stem to destroy weevil hiding shelters",
            "Destroy and chop harvested pseudostems into small pieces to dry out larvae"
        ]
    },
    {
        "id": "banana_sigatoka",
        "crop_ids": ["banana"],
        "name": "Sigatoka Leaf Spot",
        "scientific_name": "Pseudocercospora musae",
        "category": "Fungal Blight",
        "symptom_part": "leaf",
        "severity": "MODERATE",
        "symptoms": [
            "Tiny yellowish-green specks on the 3rd or 4th leaf, expanding into brown streaks",
            "Streaks turn into oval dark brown or black sunken spots with grey ash-colored centers",
            "Premature drying and burning of functional leaves, leading to underdeveloped small bunches"
        ],
        "weather_triggers": {
            "min_temp_c": 22.0,
            "max_temp_c": 30.0,
            "min_humidity_pct": 80,
            "max_humidity_pct": 100,
            "description": "Continuous South-West and North-East monsoon rain with high atmospheric humidity accelerates airborne ascospores."
        },
        "organic_remedy": {
            "title": "Bordeaux Mixture 1% + Mineral Oil",
            "preparation": "Spray 1% Bordeaux mixture or copper hydroxide @ 2g/L combined with agricultural mineral spray oil @ 10ml/L.",
            "application_interval": "Apply at 3-week intervals during the rainy season."
        },
        "chemical_remedy": {
            "title": "Propiconazole 25% EC",
            "dosage": "1.0 ml per liter of water",
            "phi_days": 20,
            "safety_note": "Rotate with Mancozeb to prevent fungicide resistance."
        },
        "preventative_ipm": [
            "Deleafing: cut off and burn heavily spotted lower leaves to reduce spore inoculum",
            "Ensure proper drainage in banana basins to avoid waterlogging and humid microclimate"
        ]
    },

    # --- CARDAMOM ---
    {
        "id": "cardamom_thrips",
        "crop_ids": ["cardamom"],
        "name": "Cardamom Thrips",
        "scientific_name": "Sciothrips cardamomi",
        "category": "Insect Pest",
        "symptom_part": "fruit",
        "severity": "HIGH",
        "symptoms": [
            "Scab formation (corky greyish encrustation) on capsule skin reducing market value",
            "Stunted, shed, or malformed flowers and panicles ('cardamom itch')",
            "Lacerated flower petals and aborted capsules"
        ],
        "weather_triggers": {
            "min_temp_c": 16.0,
            "max_temp_c": 28.0,
            "min_humidity_pct": 50,
            "max_humidity_pct": 80,
            "description": "Dry sunny spells from January to May in the Western Ghats favor massive thrips population spikes."
        },
        "organic_remedy": {
            "title": "Lecanicillium lecanii / Neem Oil 1%",
            "preparation": "Spray entomopathogenic fungus Lecanicillium lecanii @ 5g/L or cold-pressed neem oil @ 10ml/L targeting panicles and shoot crevices.",
            "application_interval": "Spray monthly during dry spells before monsoon onset."
        },
        "chemical_remedy": {
            "title": "Spinetoram 11.7% SC or Quinalphos 25% EC",
            "dosage": "Spinetoram @ 0.5 ml/L or Quinalphos @ 2.0 ml/L",
            "phi_days": 25,
            "safety_note": "Spray directed at the panicles creeping on the soil floor."
        },
        "preventative_ipm": [
            "Remove dry panicles, dead leaves, and pseudostem sheaths ('thirumu') before summer",
            "Maintain 50% shade canopy using native shade trees (Karani, Vellakil)"
        ]
    },
    {
        "id": "cardamom_azhukal",
        "crop_ids": ["cardamom"],
        "name": "Azhukal / Capsule Rot",
        "scientific_name": "Phytophthora nicotianae",
        "category": "Fungal Blight",
        "symptom_part": "fruit",
        "severity": "HIGH",
        "symptoms": [
            "Water-soaked lesions on young developing capsules which rot and drop off prematurely",
            "Rotting of panicles and pseudostem bases giving off a foul smell",
            "Shredding of leaf tips into ragged brown fibers"
        ],
        "weather_triggers": {
            "min_temp_c": 14.0,
            "max_temp_c": 24.0,
            "min_humidity_pct": 90,
            "max_humidity_pct": 100,
            "description": "Continuous heavy monsoon downpours and thick canopy shade in Idukki/Wayanad hills lead to severe rotting."
        },
        "organic_remedy": {
            "title": "Trichoderma viride + 1% Bordeaux Mixture",
            "preparation": "Soil incorporate Trichoderma viride-enriched neem cake compost (1 kg/clump) in May. Spray 1% Bordeaux mixture on leaves and panicles in June before South-West monsoon.",
            "application_interval": "Pre-monsoon (May-June) followed by mid-monsoon (August) repeat."
        },
        "chemical_remedy": {
            "title": "Potassium Phosphonate (Akomin) 40%",
            "dosage": "3.0 ml per liter of water for both foliar spray and root drenching",
            "phi_days": 14,
            "safety_note": "Drench basin with 3–5 liters of solution per clump."
        },
        "preventative_ipm": [
            "Regulate shade: prune excess canopy branches before monsoon onset to allow sunlight to reach cardamom clump base",
            "Clear mulch away from the immediate collar region during heavy rainfall months"
        ]
    },

    # --- BLACK PEPPER ---
    {
        "id": "pepper_quick_wilt",
        "crop_ids": ["black_pepper"],
        "name": "Quick Wilt / Foot Rot",
        "scientific_name": "Phytophthora capsici",
        "category": "Fungal Blight",
        "symptom_part": "root",
        "severity": "HIGH",
        "symptoms": [
            "Sudden blackening of collar and root system causing the entire vine to collapse in 7–10 days",
            "Dark brown circular spots with fringed edges ('fimbriate margins') on leaves",
            "Defoliation: leaves and pepper spikes drop rapidly leaving bare vines"
        ],
        "weather_triggers": {
            "min_temp_c": 20.0,
            "max_temp_c": 28.0,
            "min_humidity_pct": 85,
            "max_humidity_pct": 100,
            "description": "Heavy monsoon rains and water stagnation around vine bases trigger catastrophic zoospore infection."
        },
        "organic_remedy": {
            "title": "Trichoderma harzianum + 1% Bordeaux Paste",
            "preparation": "Apply 50g Trichoderma harzianum mixed with 1kg well-rotted farmyard manure per vine. Paint vine base with 1% Bordeaux paste up to 50cm height.",
            "application_interval": "Apply in May-June before monsoon and repeat in August-September."
        },
        "chemical_remedy": {
            "title": "Metalaxyl-Mancozeb (Ridomil) 0.2%",
            "dosage": "2.0 g per liter of water (drench 5 to 10 liters per vine basin)",
            "phi_days": 21,
            "safety_note": "Drench both the vine collar and surrounding root feeder zone."
        },
        "preventative_ipm": [
            "Ensure excellent surface drainage away from pepper standards",
            "Plant tolerant varieties: 'IISR Thevam', 'IISR Shakthi', or grafted pepper on Piper colubrinum rootstock"
        ]
    },

    # --- GINGER ---
    {
        "id": "ginger_rhizome_rot",
        "crop_ids": ["ginger"],
        "name": "Soft Rot / Rhizome Rot",
        "scientific_name": "Pythium aphanidermatum",
        "category": "Fungal Blight",
        "symptom_part": "root",
        "severity": "HIGH",
        "symptoms": [
            "Collar region of pseudostem becomes water-soaked and soft, pulling out easily with a light tug",
            "Yellowing starts at margins of lower leaves and advances upwards",
            "Internal tissues of seed rhizome turn into a brown, foul-smelling soft mush"
        ],
        "weather_triggers": {
            "min_temp_c": 22.0,
            "max_temp_c": 30.0,
            "min_humidity_pct": 80,
            "max_humidity_pct": 98,
            "description": "High soil moisture and waterlogging during June-August monsoons favor Pythium fungal zoospores."
        },
        "organic_remedy": {
            "title": "Trichoderma viride Rhizome Treatment + Green Mulching",
            "preparation": "Treat seed rhizomes before planting with Trichoderma viride @ 10g/kg. Drench beds with Trichoderma liquid culture (10ml/L) along with heavy green leaf mulching.",
            "application_interval": "Seed treatment at sowing; drench beds at 45 and 90 days."
        },
        "chemical_remedy": {
            "title": "Mancozeb 75% WP or Metalaxyl 35% WS",
            "dosage": "Mancozeb @ 3.0 g per liter of water for bed drenching",
            "phi_days": 30,
            "safety_note": "Immediately remove and destroy rotten clumps with surrounding soil before drenching."
        },
        "preventative_ipm": [
            "Prepare raised beds of 15cm height with deep drainage channels between beds",
            "Select disease-free seed rhizomes from certified plots; discard any rhizome showing collar discoloration"
        ]
    },

    # --- OKRA / BHINDI ---
    {
        "id": "okra_yvmv",
        "crop_ids": ["okra"],
        "name": "Yellow Vein Mosaic Virus (YVMV)",
        "scientific_name": "Begomovirus (Whitefly-transmitted)",
        "category": "Viral Disease",
        "symptom_part": "leaf",
        "severity": "HIGH",
        "symptoms": [
            "Network of bright yellow veins on green leaf blades ('vein clearing')",
            "Severely affected leaves turn completely chlorotic/yellow and small",
            "Fruits become stunted, hard, pale yellowish-white and unmarketable"
        ],
        "weather_triggers": {
            "min_temp_c": 24.0,
            "max_temp_c": 36.0,
            "min_humidity_pct": 45,
            "max_humidity_pct": 75,
            "description": "Hot, dry weather favors massive population explosions of the vector whitefly (Bemisia tabaci)."
        },
        "organic_remedy": {
            "title": "Yellow Sticky Traps + Neem Oil 2% Emulsion",
            "preparation": "Spray 2% cold-pressed neem oil (20ml neem oil + 5g soap per liter of water) targeting the underside of leaves where whiteflies colonize.",
            "application_interval": "Spray every 7 days from the 2nd week of germination."
        },
        "chemical_remedy": {
            "title": "Acetamiprid 20% SP or Imidacloprid 17.8% SL",
            "dosage": "Acetamiprid @ 0.3g/L or Imidacloprid @ 0.4 ml/L",
            "phi_days": 7,
            "safety_note": "Target whitefly vector. Do not spray during pod harvest days."
        },
        "preventative_ipm": [
            "Use YVMV-resistant Kerala varieties: 'Salkeerthi', 'Arka Anamika', and 'Susthira'",
            "Install yellow sticky traps @ 12 traps/acre to trap whiteflies early",
            "Rogue out and destroy infected seedlings in the first 30 days"
        ]
    },

    # --- CHILLI ---
    {
        "id": "chilli_anthracnose",
        "crop_ids": ["chilli"],
        "name": "Anthracnose / Fruit Rot / Dieback",
        "scientific_name": "Colletotrichum capsici",
        "category": "Fungal Blight",
        "symptom_part": "fruit",
        "severity": "HIGH",
        "symptoms": [
            "Circular sunken spots with black concentric rings of fungal fruiting bodies on ripe fruits",
            "Fruits turn bleached white, dry up, and drop prematurely",
            "Dieback: twigs dry from top downwards into a pale brown straw color"
        ],
        "weather_triggers": {
            "min_temp_c": 22.0,
            "max_temp_c": 32.0,
            "min_humidity_pct": 75,
            "max_humidity_pct": 95,
            "description": "Warm temperatures combined with intermittent rain and dew favor rapid fruit infection."
        },
        "organic_remedy": {
            "title": "Trichoderma Seed Dip + 1% Bordeaux Mixture",
            "preparation": "Seed treatment with Trichoderma @ 10g/kg seed. Spray 1% Bordeaux mixture or copper oxychloride @ 2.5g/L on branches and developing green chillies.",
            "application_interval": "Spray twice: once at flowering and once at fruit development stage."
        },
        "chemical_remedy": {
            "title": "Azoxystrobin 23% SC",
            "dosage": "1.0 ml per liter of water",
            "phi_days": 5,
            "safety_note": "Provides translaminar protection against fruit rot."
        },
        "preventative_ipm": [
            "Collect and destroy diseased fruits and dry twigs from the field",
            "Select certified seeds of resistant varieties like 'Ujjwala' and 'Jwalamukhi'"
        ]
    }
]
