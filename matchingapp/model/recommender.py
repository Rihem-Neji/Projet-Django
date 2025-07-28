import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Fonction utilitaire
def clean_text(s):
    if pd.isna(s):
        return ""
    return str(s).lower().strip()

def prepare_text(df, fields):
    return df[fields].fillna('').agg(' '.join, axis=1).apply(clean_text)

# Charger le modèle depuis le dossier
model_path = os.path.join(os.path.dirname(__file__), 'saved_model')
model = SentenceTransformer(model_path)

def recommend_jobs(df_candidate, df_jobs, top_k=3):
    candidates_text = prepare_text(df_candidate, ['skills', 'certifications', 'field_of_study', 'country', 'gender'])
    jobs_text = prepare_text(df_jobs, ['skills', 'Qualifications', 'location', 'Preference', 'Job Title'])

    cand_embeddings = model.encode(candidates_text.tolist(), show_progress_bar=False)
    job_embeddings = model.encode(jobs_text.tolist(), show_progress_bar=False)

    similarity_matrix = cosine_similarity(cand_embeddings, job_embeddings)

    top_jobs_titles = []
    top_jobs_scores = []

    for i in range(len(df_candidate)):
        sorted_indices = np.argsort(similarity_matrix[i])[::-1]
        unique_titles = []
        scores = []

        for idx in sorted_indices:
            title = df_jobs.iloc[idx]['Job Title']
            score = similarity_matrix[i, idx]

            if title not in unique_titles:
                unique_titles.append(title)
                scores.append(round(score, 4))

            if len(unique_titles) >= top_k:
                break

        top_jobs_titles.append(unique_titles)
        top_jobs_scores.append(scores)

    df_candidate['top_matched_jobs'] = top_jobs_titles
    df_candidate['top_similarity_scores'] = top_jobs_scores

    return df_candidate[['skills', 'top_matched_jobs', 'top_similarity_scores']]
