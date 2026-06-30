import pandas as pd

# -------- FILE PATHS (UPDATE IF NEEDED) --------
demo_path = r"C:\Users\shrey\Downloads\DEMO_E.xpt"
cbc_path  = r"C:\Users\shrey\Downloads\CBC_E.xpt"
crp_path  = r"C:\Users\shrey\Downloads\CRP_E.xpt"
thy_path  = r"C:\Users\shrey\Downloads\THYROD_E.xpt"
vid_path  = r"C:\Users\shrey\Downloads\VID_E.xpt"

output_path = r"C:\Users\shrey\OneDrive\Documents\4th sem\pathology\drift_project.xlsx"


# Load NHANES XPT files
demo = pd.read_sas(demo_path)
cbc  = pd.read_sas(cbc_path)
crp  = pd.read_sas(crp_path)
thy  = pd.read_sas(thy_path)
vid  = pd.read_sas(vid_path)

# Merge datasets using SEQN
df = (
    demo
    .merge(cbc, on='SEQN', how='inner')
    .merge(crp, on='SEQN', how='inner')
    .merge(thy, on='SEQN', how='inner')
    .merge(vid, on='SEQN', how='inner')
)

# Rename important columns
df = df.rename(columns={
    'RIDAGEYR': 'age',
    'RIAGENDR': 'gender',
    'LBXWBCSI': 'WBC',
    'LBXLYPCT': 'lymphocytes',
    'LBXCRP': 'CRP',
    'LBXTSH1': 'TSH',
    'LBXT4F': 'Free_T4',
    'LBXT3F': 'Free_T3',
    'LBXTT4': 'Total_T4',
    'LBXTT3': 'Total_T3',
    'LBXTPO': 'TPO_Ab',
    'LBXATG': 'TG_Ab',
    'LBXVIDMS': 'vitamin_D'
})

# Keep only relevant columns
df = df[
     ['SEQN', 'age', 'gender',
     'WBC', 'lymphocytes', 'CRP',
     'vitamin_D',
     'TSH', 'Free_T3', 'Free_T4',
     'TPO_Ab', 'TG_Ab']
]

# Save to Excel
df.to_excel(output_path, index=False)

print("Merged dataset saved successfully!")
print("Final shape:", df.shape)
