from django.shortcuts import render
from django.http import HttpResponse
from .matching import predict_match  # 👈 on importe la fonction
import pandas as pd
import requests

from matchingapp.model.recommender import recommend_jobs

# Chargement du dataset
df_jobs = pd.read_csv("matchingapp/data/jobs_cleaned.csv")



def formulaire(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'skills': request.POST.get('skills'),
            'certifications': request.POST.get('certifications'),
            'field_of_study': request.POST.get('field_of_study'),
            'experience_years': request.POST.get('experience_years'),
            'desired_salary_min': request.POST.get('desired_salary_min'),
            'gender': request.POST.get('gender'),
            'country': request.POST.get('country')
        }

         # 👇 Formatage des inputs pour Hugging Face
        payload = {
            "data": [
                data['skills'],
                data['certifications'],
                data['field_of_study'],
                data['country'],
                data['gender']
            ]
        }

        # 👇 Appel à l'API Hugging Face
        url = "https://RihemNeji-ProjetDjango.hf.space/run/predict"
        response = requests.post(url, json=payload)
        result = response.json()

        # 👇 Récupération des jobs + scores
        output = result['data'][0]  # tu retournes une string formatée dans app.py
        lines = output.split('\n')
        jobs = [line.split(' | ')[0] for line in lines]
        scores = [float(line.split(' | ')[1]) for line in lines]

        context = {
            'name': data['name'],
            'jobs': zip(jobs, scores)
        }
        return render(request, 'result.html', context)
    
    return render(request, 'formulaire.html')


def resultat(request):
    # Optionnel, utile seulement si tu affiches un historique
    return render(request, 'result.html')

