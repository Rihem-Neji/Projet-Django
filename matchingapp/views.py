import os
import requests
from django.http import HttpResponse
from django.shortcuts import render

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
            "inputs": {
                "source_sentence": f"{data['skills']}, {data['certifications']}, {data['field_of_study']}",
                "sentences": [
                    "Data Scientist",
                    "Software Engineer",
                    "Project Manager",
                    "Marketing Specialist"
                    # Ajoutez ici une liste d'intitulés de poste potentiels
                ]
            }
        }
        
        # Le modèle que vous utilisiez n'est pas fait pour la "sentence-similarity pipeline"
        # J'ai remplacé par un modèle adapté à cette tâche.
        # Vous pouvez trouver d'autres modèles ici: https://huggingface.co/models?pipeline_tag=sentence-similarity
        url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        
        # Récupération sécurisée du jeton d'accès
        hf_token = os.environ.get("HUGGINGFACE_TOKEN")
        if not hf_token:
            return HttpResponse("Erreur : Le jeton d'accès Hugging Face n'est pas configuré.", status=500)

        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                scores = response.json()
                jobs = payload['inputs']['sentences']

                # Crée une liste de tuples (job, score) et la trie par score décroissant
                job_scores = sorted(zip(jobs, scores), key=lambda item: item[1], reverse=True)

                context = {
                    'name': data['name'],
                    'job_scores': job_scores
                }
                # Assurez-vous d'avoir un template 'result.html' qui peut itérer sur 'job_scores'
                return render(request, 'result.html', context)
            else:
                return HttpResponse(f"Erreur API Hugging Face : {response.status_code} - {response.text}")

        except Exception as e:
            return HttpResponse(f"Erreur lors de l’appel API : {e}")

    return render(request, 'formulaire.html')

def resultat(request):
    return render(request, 'result.html')