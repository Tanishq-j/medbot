"""Medical Knowledge Base & Clinical Reference Library.

Contains curated clinical reference guidelines rooted in evidence-based medicine,
clinical practice guidelines (AHA, ADA, WHO, ICMR), and safety protocols
consulted by the Medical Research Agent.
"""

from typing import Any, Dict, List

SAMPLE_MEDICAL_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "MED-DOC-CARDIO-001",
        "title": "Cardiovascular Health & Hypertension Clinical Guidelines",
        "category": "Cardiology & Preventive Medicine",
        "keywords": [
            "hypertension", "blood pressure", "systolic", "diastolic", "bp",
            "dash diet", "lifestyle", "ace inhibitor", "calcium channel blocker", "hypertensive crisis"
        ],
        "summary": "Clinical classification of blood pressure stages, lifestyle interventions, and hypertensive emergency indicators.",
        "content": (
            "1. Blood Pressure Classification (ACC/AHA & Clinical Consensus):\n"
            "   - Normal: Systolic < 120 mmHg and Diastolic < 80 mmHg.\n"
            "   - Elevated: Systolic 120-129 mmHg and Diastolic < 80 mmHg.\n"
            "   - Stage 1 Hypertension: Systolic 130-139 mmHg or Diastolic 80-89 mmHg.\n"
            "   - Stage 2 Hypertension: Systolic ≥ 140 mmHg or Diastolic ≥ 90 mmHg.\n"
            "   - Hypertensive Crisis: Systolic > 180 mmHg and/or Diastolic > 120 mmHg.\n"
            "2. First-Line Non-Pharmacological Interventions:\n"
            "   - Dietary Approaches to Stop Hypertension (DASH) diet: High in fruits, vegetables, whole grains; sodium intake < 2,300 mg/day (ideal < 1,500 mg/day).\n"
            "   - Physical Activity: At least 150 minutes/week of moderate-intensity aerobic exercise.\n"
            "   - Weight Reduction: Approximately 1 mmHg reduction in BP for every 1 kg lost in overweight individuals.\n"
            "3. First-Line Pharmacological Classes:\n"
            "   - Common first-line agents include Thiazide diuretics, ACE inhibitors (or ARBs), and Calcium Channel Blockers (CCBs).\n"
            "4. Red Flag Warning Signs (Hypertensive Emergency):\n"
            "   - Severe headache, chest pain, shortness of breath, blurred vision, or neurological deficits accompanying markedly elevated BP mandate immediate emergency room evaluation."
        )
    },
    {
        "id": "MED-DOC-DIABETES-002",
        "title": "Type 2 Diabetes Mellitus & Glycemic Control Standards (ADA/ICMR)",
        "category": "Endocrinology & Metabolic Health",
        "keywords": [
            "diabetes", "blood sugar", "glucose", "hba1c", "fasting", "postprandial",
            "hypoglycemia", "metformin", "rule of 15", "insulin"
        ],
        "summary": "Diagnostic thresholds, target HbA1c ranges, hypoglycemia acute management, and monitoring standards.",
        "content": (
            "1. Diagnostic Criteria for Diabetes Mellitus:\n"
            "   - Fasting Plasma Glucose (FPG) ≥ 126 mg/dL (7.0 mmol/L) after an 8-hour fast; OR\n"
            "   - 2-hour Post-load Plasma Glucose ≥ 200 mg/dL (11.1 mmol/L) during 75g OGTT; OR\n"
            "   - Glycated Hemoglobin (HbA1c) ≥ 6.5% (48 mmol/mol); OR\n"
            "   - Random Plasma Glucose ≥ 200 mg/dL accompanied by classic hyperglycemic symptoms (polyuria, polydipsia, weight loss).\n"
            "2. General Glycemic Targets for Non-Pregnant Adults:\n"
            "   - HbA1c: < 7.0% (individualized based on age, duration of disease, and hypoglycemia risk).\n"
            "   - Preprandial capillary plasma glucose: 80-130 mg/dL.\n"
            "   - Peak postprandial capillary plasma glucose: < 180 mg/dL.\n"
            "3. Acute Hypoglycemia Management (The 'Rule of 15'):\n"
            "   - Level 1 Hypoglycemia is defined as Blood Glucose < 70 mg/dL (3.9 mmol/L).\n"
            "   - Consume 15 grams of fast-acting simple carbohydrates (e.g., 4 glucose tablets, 1/2 cup fruit juice, or 3-4 candies).\n"
            "   - Recheck blood glucose after 15 minutes. If still < 70 mg/dL, repeat with another 15g of carbohydrates.\n"
            "   - If severe confusion, unresponsiveness, or seizure occurs, administer intramuscular glucagon or call emergency services; do not administer oral fluids."
        )
    },
    {
        "id": "MED-DOC-RESP-003",
        "title": "Acute Respiratory Tract Infections & Clinical Triage Protocol",
        "category": "Pulmonology & Infectious Disease",
        "keywords": [
            "cough", "fever", "respiratory", "bronchitis", "pneumonia", "shortness of breath",
            "dyspnea", "spo2", "oxygen", "wheezing", "antibiotics"
        ],
        "summary": "Differentiating upper vs lower respiratory infections, antibiotic stewardship, and respiratory distress red flags.",
        "content": (
            "1. Viral Bronchitis vs. Bacterial Pneumonia:\n"
            "   - Acute Bronchitis is predominantly viral (>90% of cases) self-limiting illness lasting 1-3 weeks. Routine antibiotic therapy is not recommended.\n"
            "   - Community-Acquired Pneumonia is characterized by localized crackles/rales, persistent high fever (>38.5°C), purulent sputum, pleuritic chest pain, and focal consolidation on chest imaging.\n"
            "2. Pulse Oximetry & Oxygenation Triage:\n"
            "   - Normal resting peripheral oxygen saturation (SpO2): 95% - 100% on room air.\n"
            "   - Mild Hypoxemia: SpO2 91% - 94% (warrants prompt clinical evaluation).\n"
            "   - Moderate to Severe Hypoxemia: SpO2 < 90% (indicates respiratory compromise requiring emergency supplemental oxygen).\n"
            "3. Red Flag Symptoms Mandating Immediate Urgent Care:\n"
            "   - Dyspnea or shortness of breath at rest, respiratory rate > 28 breaths/min, cyanosis (bluish lips/fingertips), hemoptysis (coughing up blood), stridor, or altered mental state.\n"
            "4. Symptomatic & Supportive Care:\n"
            "   - Oral hydration, saline nasal irrigation, honey for cough (in patients > 1 year old), and antipyretics (such as paracetamol) for fever discomfort."
        )
    },
    {
        "id": "MED-DOC-PHARM-004",
        "title": "Analgesic & NSAID Safety, Dosing, and Interaction Standards",
        "category": "Pharmacology & Medication Safety",
        "keywords": [
            "paracetamol", "acetaminophen", "nsaid", "ibuprofen", "naproxen", "gastric ulcer",
            "kidney", "renal", "liver", "hepatotoxicity", "contraindications"
        ],
        "summary": "Safe dosing limits for paracetamol, gastrointestinal and renal contraindications for NSAIDs, and drug safety warnings.",
        "content": (
            "1. Paracetamol (Acetaminophen) Safe Dosing Limits:\n"
            "   - Maximum adult dose: 4,000 mg (4 grams) per 24 hours from all combined sources; for elderly, underweight, or hepatic risk individuals, max 2,000 - 3,000 mg/day.\n"
            "   - Minimum dosing interval: 4-6 hours between doses.\n"
            "   - Major Risk: Acute hepatotoxicity resulting from inadvertent co-ingestion of multiple over-the-counter multi-symptom cold/flu formulations.\n"
            "2. Non-Steroidal Anti-Inflammatory Drugs (NSAIDs - e.g., Ibuprofen, Naproxen, Diclofenac):\n"
            "   - Mechanism: Inhibit COX-1 and COX-2 enzymes, reducing prostaglandin synthesis.\n"
            "   - Gastrointestinal Risks: Gastritis, peptic ulcers, and GI bleeding. Risk increases with age, higher doses, prolonged duration, and co-administration with corticosteroids or anticoagulants.\n"
            "   - Renal & Cardiovascular Precautions: NSAIDs can cause acute kidney injury (AKI) by decreasing renal blood flow (inhibiting afferent vasodilation); contraindicated in severe Chronic Kidney Disease (CKD), uncontrolled hypertension, and heart failure.\n"
            "3. Antibiotic Stewardship Principles:\n"
            "   - Antibiotics are ineffective against viral infections (common cold, influenza, acute viral bronchitis, uncomplicated sore throat). Never use leftover or unprescribed antibiotics."
        )
    },
    {
        "id": "MED-DOC-EMERGENCY-005",
        "title": "Emergency Medical Triage & Critical Red Flag Indicators",
        "category": "Emergency Medicine & Acute Care",
        "keywords": [
            "emergency", "red flag", "chest pain", "heart attack", "myocardial infarction",
            "stroke", "fast", "anaphylaxis", "head injury", "triage"
        ],
        "summary": "Identification of life-threatening clinical presentations including acute coronary syndrome, stroke FAST criteria, and anaphylaxis.",
        "content": (
            "1. Acute Coronary Syndrome (Heart Attack) Warning Signs:\n"
            "   - Sudden retrosternal chest pressure, heaviness, crushing sensation lasting > 10 minutes.\n"
            "   - Radiation of pain to left arm, neck, jaw, back, or epigastrium.\n"
            "   - Associated with diaphoresis (cold sweating), nausea, lightheadedness, or acute shortness of breath.\n"
            "   - Action: Immediate emergency medical activation (call ambulance); do not attempt to self-drive.\n"
            "2. Stroke Identification (FAST Protocol):\n"
            "   - F (Face Drooping): One side of the face droops or is numb; uneven smile.\n"
            "   - A (Arm Weakness): One arm drifts downward when both arms are raised.\n"
            "   - S (Speech Difficulty): Slurred speech, unable to speak, or difficulty comprehending simple sentences.\n"
            "   - T (Time to Call Emergency): Note the exact time symptoms began. Rapid thrombolytic/endovascular intervention window is typically within 3-4.5 hours.\n"
            "3. Severe Allergic Reaction (Anaphylaxis):\n"
            "   - Rapid onset of swelling of lips, tongue, or airway; hives; wheezing/difficulty breathing; profound drop in blood pressure (dizziness/collapse).\n"
            "   - Action: Immediate administration of intramuscular Epinephrine (EpiPen) into anterolateral thigh and emergency transport.\n"
            "4. Severe Head Trauma Red Flags:\n"
            "   - Loss of consciousness, persistent or worsening vomiting, unequal pupil size, seizures, clear fluid draining from nose/ears, or progressive confusion."
        )
    }
]

# Aliases for backwards compatibility
SAMPLE_LEGAL_DOCUMENTS = SAMPLE_MEDICAL_DOCUMENTS
