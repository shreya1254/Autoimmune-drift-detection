import pandas as pd

# Load
thyroid = pd.read_excel(r"C:\Users\shrey\OneDrive\Documents\4th sem\pathology\drift_project\Thyroid\thyroid_results.xlsx")
diabetes = pd.read_excel(r"C:\Users\shrey\OneDrive\Documents\4th sem\pathology\drift_project\diabetes\diabetes_result.xlsx")

# Rename thyroid columns
thyroid = thyroid.rename(columns={
    'main_biomarker':'thyroid_cause',
    'direction':'thyroid_direction',
    'drift':'thyroid_drift'
})

# Rename diabetes columns
diabetes = diabetes.rename(columns={
    'cause':'diabetes_cause',
    'direction':'diabetes_direction',
    'drift':'diabetes_drift'
})

# Select only required columns
thyroid = thyroid[['SEQN','thyroid_drift','thyroid_cause','thyroid_direction']]
diabetes = diabetes[['SEQN','diabetes_drift','diabetes_cause','diabetes_direction']]

# Merge
combined = thyroid.merge(diabetes, on='SEQN', how='outer')
combined.fillna(0, inplace=True)

# Risk Score
combined['total_autoimmune_score'] = (
    combined['thyroid_drift'] +
    combined['diabetes_drift']
)

# Disease detection
def detect(row):
    diseases = []
    reasons = []

    if row['thyroid_drift'] == 1:
        diseases.append("Thyroid Disorder")
        reasons.append(f"{row['thyroid_cause']} ({row['thyroid_direction']})")

    if row['diabetes_drift'] == 1:
        diseases.append("Diabetes Mellitus")
        reasons.append(f"{row['diabetes_cause']} ({row['diabetes_direction']})")

    if not diseases:
        return "No Significant Drift", "Within Normal Limits"

    return ", ".join(diseases), "; ".join(reasons)

combined[['Likely_Disease','Reason']] = combined.apply(
    lambda x: pd.Series(detect(x)), axis=1
)

combined.to_excel(r"C:\Users\shrey\OneDrive\Documents\4th sem\pathology\drift_project\final_autoimmune_results.xlsx", index=False)

print("Final combined model completed successfully.")