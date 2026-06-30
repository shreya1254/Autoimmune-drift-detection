import pandas as pd
from sklearn.ensemble import IsolationForest

# -------- LOAD MERGED DATA --------
df = pd.read_excel(
    r"C:\Users\shrey\OneDrive\Documents\4th sem\pathology\drift_project\drift_project.xlsx"
)

# -------- AGE GROUPS --------
df['age_group'] = pd.cut(
    df['age'],
    bins=[0, 12, 25, 45, 65, 120],
    labels=['Child', 'Young_Adult', 'Adult', 'Middle_Aged', 'Elderly']
)

# -------- FEATURES USED --------
features = [
    'WBC', 'lymphocytes', 'CRP',
    'vitamin_D',
    'TSH', 'Free_T3', 'Free_T4',
    'TPO_Ab', 'TG_Ab'
]

# Drop rows with missing values in selected features
df = df.dropna(subset=features)

# -------- OUTPUT COLUMNS --------
df['drift'] = 0                  # 0 = normal, 1 = drift
df['main_biomarker'] = 'Normal'
df['direction'] = 'Normal'
df['autoimmune_risk'] = 'None'

# -------- ISOLATION FOREST (AGE-WISE) --------
for group in df['age_group'].dropna().unique():

    subset = df[df['age_group'] == group]

    if len(subset) < 50:
        continue

    iso = IsolationForest(
        n_estimators=150,
        contamination=0.05,
        random_state=42,
        n_jobs=-1
    )

    preds = iso.fit_predict(subset[features])
    anomaly_idx = subset.index[preds == -1]

    medians = subset[features].median()
    q1 = subset[features].quantile(0.25)
    q3 = subset[features].quantile(0.75)

    for idx in anomaly_idx:
        df.loc[idx, 'drift'] = 1

        # -------- FIND MAIN CAUSE --------
        deviations = {
            f: abs(df.loc[idx, f] - medians[f]) / ((q3[f] - q1[f]) + 1e-6)
            for f in features
        }

        main_feature = max(deviations, key=deviations.get)
        df.loc[idx, 'main_biomarker'] = main_feature

        # Direction
        if df.loc[idx, main_feature] > medians[main_feature]:
            df.loc[idx, 'direction'] = 'Increase'
        else:
            df.loc[idx, 'direction'] = 'Decrease'

        # -------- AUTOIMMUNE DRIFT INTERPRETATION --------
        if main_feature in ['TPO_Ab', 'TG_Ab']:
            df.loc[idx, 'autoimmune_risk'] = 'Hashimoto’s Thyroiditis'

        elif main_feature in ['Free_T3', 'Free_T4'] and df.loc[idx, 'direction'] == 'Increase':
            df.loc[idx, 'autoimmune_risk'] = 'Graves’ Disease'

        elif main_feature == 'TSH' and df.loc[idx, 'direction'] == 'Increase':
            df.loc[idx, 'autoimmune_risk'] = 'Hypothyroid Autoimmune Pattern'

        elif main_feature in ['CRP', 'WBC', 'lymphocytes']:
            df.loc[idx, 'autoimmune_risk'] = 'Systemic Autoimmune Inflammation'

        elif main_feature == 'vitamin_D' and df.loc[idx, 'direction'] == 'Decrease':
            df.loc[idx, 'autoimmune_risk'] = 'Immune Dysregulation Risk'

# -------- FINAL OUTPUT --------
output = df[
    ['SEQN','age', 'gender', 'age_group',
     'main_biomarker', 'direction',
     'autoimmune_risk', 'drift']
]

output.to_excel(
    r"C:\Users\shrey\OneDrive\Documents\4th sem\pathology\thyroid_autoimmune_drift_results.xlsx",
    index=False
)

print("Autoimmune drift detection completed successfully!")
