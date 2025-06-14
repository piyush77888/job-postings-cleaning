import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Open file picker
Tk().withdraw()
file_path = askopenfilename(title="Select the job postings CSV")

# Load the file
df = pd.read_csv(file_path)
print(df.shape)
print(df.head())
print(df.columns)
print("\nMissing values per column:")
print(df.isnull().sum())
# Drop columns with too many missing values
df.drop(columns=['salary_range', 'telecommuting', 'has_company_logo'], inplace=True, errors='ignore')
import re

def clean_text(text):
    if pd.isnull(text):
        return ""
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'\s+', ' ', text)   # Remove extra spaces
    text = re.sub(r'[^A-Za-z0-9., ]+', '', text)  # Keep only words, numbers, basic punctuation
    return text.strip()

# Apply to multiple columns
for col in ['title', 'location', 'company_profile', 'description', 'requirements', 'benefits']:
    df[col] = df[col].apply(clean_text)
# Fill missing categorical fields with 'Unknown'
for col in ['department', 'employment_type', 'required_education']:
    df[col] = df[col].fillna('Unknown')
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_csv("cleaned_job_postings.csv", index=False)
print("✅ Saved as cleaned_job_postings.csv")

