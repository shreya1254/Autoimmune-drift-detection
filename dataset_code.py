import pandas as pd

# Load files
lab = pd.read_sas(r"C:\Users\shrey\OneDrive\Documents\4th sem\pathology\drift_project\diabetes\L10_2_B.xpt")
demo = pd.read_sas(r"C:\Users\shrey\OneDrive\Documents\4th sem\pathology\drift_project\diabetes\DEMO_B.xpt")

# Select required columns
lab = lab[['SEQN','LB2GH','LB2GLU','LB2CP','LB2IN']]
demo = demo[['SEQN','RIDAGEYR','RIAGENDR']]

# Merge
df = pd.merge(lab, demo, on='SEQN', how='inner')

# Rename for clarity
df.rename(columns={
    'LB2GH':'HbA1c',
    'LB2GLU':'Fasting_Glucose',
    'LB2CP':'C_Peptide',
    'LB2IN':'Insulin',
    'RIDAGEYR':'Age',
    'RIAGENDR':'Gender'
}, inplace=True)

# Encode gender
df['Gender'] = df['Gender'].map({1:0, 2:1})

# Remove missing
df.dropna(inplace=True)

# Save
df.to_excel(r"C:\Users\shrey\Desktop\diabetes_model.xlsx", index=False)

print("Diabetes dataset ready.")