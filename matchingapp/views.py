import os
import requests
from django.http import HttpResponse
from django.shortcuts import render
from gradio_client import Client, handle_file # Importez le client

def formulaire(request):
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),
            'skills': request.POST.get('skills'),
            'certifications': request.POST.get('certifications'),
            'field_of_study': request.POST.get('field_of_study'),
            'experience_years': request.POST.get('experience_years'),
            'desired_salary_min': request.POST.get('desired_salary_min'),
            'gender': request.POST.get('gender'),
            'country': request.POST.get('country')
        }
        
        try:
            # --- 1. Initialisation du client ---
            # On pointe vers le nom du Space, pas l'URL de l'API.
            # On passe le token directement ici pour l'authentification.
            hf_token = os.environ.get("HUGGINGFACE_TOKEN")
            if not hf_token:
                return HttpResponse("Erreur de configuration serveur : Le jeton d'accès Hugging Face est manquant.", status=500)
            
            print("--- INFO: Connexion au Space Gradio via le client ---")
            client = Client("RihemNeji/ProjetDjango", hf_token=hf_token)

            # --- 2. Appel de la fonction 'predict' de manière bloquante ---
            # Le client gère l'attente pour nous. Il ne renverra que le résultat final.
            # Les arguments sont passés directement par leur nom.
            print("--- INFO: Lancement de la prédiction et attente du résultat... ---")
            result = client.predict(
                skills=form_data['skills'],
                certifications=form_data['certifications'],
                field=form_data['field_of_study'],
                country=form_data['country'],
                gender=form_data['gender'],
                api_name="/predict"
            )
            
            # Le résultat sera directement la chaîne de caractères renvoyée par votre app.py
            # Ex: "Métier 1 | 95.2%\n..."
            print(f"--- INFO: Résultat reçu : {result} ---")
            output_string = result
            
            # --- 3. Analyse du résultat (même code qu'avant) ---
            lines = output_string.strip().split('\n')
            job_scores = []
            for line in lines:
                if ' | ' in line:
                    parts = line.split(' | ', 1)
                    if len(parts) == 2:
                        job_scores.append((parts[0], parts[1]))

            # --- 4. Envoi au template ---
            context = {
                'name': form_data['name'],
                'jobs': job_scores
            }
            return render(request, 'result.html', context)

        except Exception as e:
            # Cette exception attrapera les erreurs de connexion, de timeout, etc.
            return HttpResponse(f"Une erreur est survenue lors de l'exécution de la tâche sur Hugging Face : {e}", status=500)


    return render(request, 'formulaire.html')


def resultat(request):
    return render(request, 'result.html')