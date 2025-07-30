import os
import requests
from django.shortcuts import render
from django.http import HttpResponse


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
            # 🔐 Appel Hugging Face API
            url = os.environ.get("HUGGINGFACE_API_URL") or "https://rihemneji-projetdjango.hf.space/run/predict"

            response = requests.post(url, json=payload, timeout=20)

            if response.status_code != 200:
                return HttpResponse(f"Erreur API HuggingFace : {response.status_code} - {response.text}", status=500)

            result = response.json()
            output = result['data'][0]

            if not isinstance(output, str):
                return HttpResponse(f"Réponse API invalide : {output}", status=500)

            lines = output.strip().split('\n')
            jobs = [line.split(' | ')[0] for line in lines]
            scores = [float(line.split(' | ')[1]) for line in lines]

            context = {
                'name': data['name'],
                'jobs': zip(jobs, scores)
            }

            return render(request, 'result.html', context)

        except Exception as e:
            return HttpResponse(f"Erreur lors du traitement de la requête : {str(e)}", status=500)

    return render(request, 'formulaire.html')
def resultat(request):
    return render(request, 'result.html')
