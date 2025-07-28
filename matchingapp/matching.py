import os
from sentence_transformers import SentenceTransformer
import pandas as pd

# Chemin du fichier d'offres
df_jobs = pd.read_csv('matchingapp/data/jobs_cleaned.csv', on_bad_lines='skip')  # ⚠ adapte le chemin

model_path = os.path.join(os.path.dirname(__file__), 'model', 'saved_model')
model = SentenceTransformer(model_path)

def predict_match(text):
    embedding = model.encode([text])
    return embedding[0]
