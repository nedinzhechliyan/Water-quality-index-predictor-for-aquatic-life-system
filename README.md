# Water-quality-index-predictor-for-aquatic-life-system
water_quality_app/
├ app.py
 predict.py
 requirements.txt
 .env
 templates/
 index.html
.Recalculated_Aquaculture_Water_Suitability_Signals_WQI_Derived.csv
Takes 15 water quality parameters as input
Finds 3 most similar historical cases from the dataset of 4,300 records
Sends parameters and similar cases to NVIDIA Nemotron-3-Ultra-550B as context
Returns classification, confidence level, reason and class probabilities

Tech Stack

Frontend: HTML, CSS, JavaScript
Backend: Python, Flask
AI Model: NVIDIA Nemotron-3-Ultra-550B-A55B via NVIDIA NIM
Data Processing: Pandas
Dataset: Recalculated Aquaculture Water Suitability Signals WQI Derived (4,300 records)

So the data set is collected from Kaggle. 
