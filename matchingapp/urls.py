from django.shortcuts import redirect
from django.urls import path
from . import views
def home_redirect(request):
    return redirect('formulaire')

urlpatterns = [
    path('', home_redirect),  # redirige la racine vers /formulaire/
    path('formulaire/', views.formulaire, name='formulaire'),
    path('result/', views.resultat, name='result'),
]
