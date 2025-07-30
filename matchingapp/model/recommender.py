import pandas as pd
import os
import requests

def recommend_jobs(df_candidate, top_k=3):
    url = os.environ.get("https://rihemneji-projetdjango.hf.space/run/predict")

    payload = {
        "data": [
            df_candidate.iloc[0]['skills'],
            df_candidate.iloc[0]['certifications'],
            df_candidate.iloc[0]['field_of_study'],
            df_candidate.iloc[0]['country'],
            df_candidate.iloc[0]['gender']
        ]
    }

    response = requests.post(url, json=payload)
    result = response.json()

    output = result['data'][0]  # Exemple: "Offre A | 93%\nOffre B | 85%"
    lines = output.strip().split('\n')

    jobs = [line.split(' | ')[0] for line in lines]
    scores = [float(line.split(' | ')[1].replace('%', '')) for line in lines]

    df_candidate['top_matched_jobs'] = [jobs]
    df_candidate['top_similarity_scores'] = [scores]
    return df_candidate[['skills', 'top_matched_jobs', 'top_similarity_scores']]
