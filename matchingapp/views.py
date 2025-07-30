from django.shortcuts import render
import pandas as pd
import requests
import os

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

        # ⚠️ Seuls les champs nécessaires pour Hugging Face
        payload = {
            "data": [
                data['skills'],
                data['certifications'],
                data['field_of_study'],
                data['country'],
                data['gender']
            ]
        }

        try:
            url =  "https://rihemneji-projetdjango.hf.space/run/predict"
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                output = result['data'][0]
                lines = output.split('\n')
                jobs = [line.split(' | ')[0] for line in lines]
                scores = [line.split(' | ')[1] for line in lines]

                context = {
                    'name': data['name'],
                    'jobs': zip(jobs, scores)
                }
                return render(request, 'result.html', context)
            else:
                return HttpResponse(f"Erreur API HuggingFace : {response.status_code} - {response.text}")

        except Exception as e:
            return HttpResponse(f"Erreur lors de l’appel API : {e}")

    return render(request, 'formulaire.html')
def resultat(request):
    return render(request, 'result.html')
