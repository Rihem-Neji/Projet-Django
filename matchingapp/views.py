from django.shortcuts import render
from django.http import HttpResponse
from .matching import predict_match  # 👈 on importe la fonction
import pandas as pd

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

        df_candidate = pd.DataFrame([data])
        df_candidate = recommend_jobs(df_candidate, df_jobs)

        top_jobs = df_candidate.loc[0, 'top_matched_jobs']
        top_scores = df_candidate.loc[0, 'top_similarity_scores']

        context = {
            'name': data['name'],
            'jobs': zip(top_jobs, top_scores)
        }
        return render(request, 'result.html', context)
    
    return render(request, 'formulaire.html')


def resultat(request):
    # Optionnel, utile seulement si tu affiches un historique
    return render(request, 'result.html')

