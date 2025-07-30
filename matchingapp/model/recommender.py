import pandas as pd
import requests

def recommend_jobs(df_candidate, df_jobs, top_k=3):
    # Préparation du texte candidat
    skills = df_candidate.iloc[0].get("skills", "")
    certifications = df_candidate.iloc[0].get("certifications", "")
    field = df_candidate.iloc[0].get("field_of_study", "")
    country = df_candidate.iloc[0].get("country", "")
    gender = df_candidate.iloc[0].get("gender", "")

    # Payload pour Hugging Face
    payload = {
        "data": [skills, certifications, field, country, gender]
    }

    # 🔗 Lien API Hugging Face
    url = os.environ.get("HUGGINGFACE_API_URL")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        output = result['data'][0]  # output = "Offre A | 94.3%\nOffre B | 88.1%\nOffre C | 81.5%"
        lines = output.strip().split('\n')

        # Séparer titres et scores
        jobs = [line.split(' | ')[0] for line in lines]
        scores = [float(line.split(' | ')[1].replace('%', '')) for line in lines]

        df_candidate['top_matched_jobs'] = [jobs]
        df_candidate['top_similarity_scores'] = [scores]

        return df_candidate[['skills', 'top_matched_jobs', 'top_similarity_scores']]

    except Exception as e:
        print(f"[ERREUR] Appel HuggingFace échoué : {e}")
        return df_candidate
