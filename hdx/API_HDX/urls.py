from django.urls import path

from API_HDX import views

urlpatterns = [
    path('', views.paises, name='index'),
    path('data', views.data, name='data'),
    path('insertar_consulta_usuario', views.insertar_consulta_usuario, name='insertar_consulta_usuario'),
    path('queries', views.lista_propuestas, name='queries')
]