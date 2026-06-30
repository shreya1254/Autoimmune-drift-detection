import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

path = r"C:\Users\shrey\OneDrive\Documents\4th sem\pathology\drift_project\diabetes\diabetes_model.xlsx"

df = pd.read_excel(path)

print("File loaded successfully")
print(df.head())

df['Gender'] = df['Gender'].map({1:0, 2:1})


features = ['HbA1c', 'Fasting_Glucose', 'Insulin', 'C_Peptide', 'Age']

X = df[features].copy()


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


iso = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)

df['drift'] = iso.fit_predict(X_scaled)


df['drift'] = df['drift'].map({1:0, -1:1})

medians = X.median()

df['cause'] = "Normal"
df['direction'] = "Normal"

for i in df.index:
    if df.loc[i, 'drift'] == 1:
        deviations = {}
        for col in features:
            deviations[col] = abs(df.loc[i, col] - medians[col])
        
        main_feature = max(deviations, key=deviations.get)
        df.loc[i, 'cause'] = main_feature
        
        if df.loc[i, main_feature] > medians[main_feature]:
            df.loc[i, 'direction'] = "Increase"
        else:
            df.loc[i, 'direction'] = "Decrease"


output_path = r"C:\Users\shrey\OneDrive\Documents\4th sem\pathology\drift_project\diabetes\results.xlsx"

df.to_excel(output_path, index=False)

print("Results saved successfully.")