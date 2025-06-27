from django.shortcuts import render
from API_HDX.models import Ingresar
import cx_Oracle

import requests

def index(request):
    try:
        connection = cx_Oracle.connect("system", "pythonoracle", "localhost/XE")
        cursor = connection.cursor()

        # para obtener usuarios
        cursor.execute("SELECT id_usuario, nombre, apellido, email FROM usuarioApp")
        usuarios = [{'id_usuario': row[0], 'nombre': row[1], 'apellido': row[2], 'email': row[3]} for row in
                    cursor.fetchall()]

        # obtener consultas
        cursor.execute("SELECT id_consulta, pais FROM consultaApp")
        consultas = [{'id_consulta': row[0], 'pais': row[1]} for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        contexto = {
            'usuarios': usuarios,
            'consultas': consultas
        }
        return render(request, "web/index.html", contexto)

    except cx_Oracle.Error as error:
        messages.error(request, f"Error al cargar datos: {str(error)}")

def paises(request):
    from requests.exceptions import HTTPError
    try:
        url = 'https://api.worldbank.org/v2/country?format=Json'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()[1]
        contexto = {
            'lista_paises':data,
        }
        return render(request, "web/index.html", contexto)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')

def data (request):
    from requests.exceptions import HTTPError
    try:
        # URL para genar la lista de búsqueda
        url_paises = 'https://api.worldbank.org/v2/country?format=Json'
        response = requests.get(url_paises)
        # response.raise_for_status()
        data_paises = response.json()[1]

        # URL para obtener income por ISO de Pais
        url_iso= 'https://api.worldbank.org/v2/country/'
        pais = request.POST['cmbPais']
        url_pais_iso = url_iso+pais+'?format=Json'
        response = requests.get(url_pais_iso)
        data = response.json()[1]

        # URL para búsqueda de indicadores
        url_indicators = 'https://api.worldbank.org/v2/country/'
        #variables para GDP y Population
        gdp = 'NY.GDP.PCAP.CD'
        pop = 'SP.POP.TOTL'
        pais = request.POST['cmbPais']

        # Para obtener dato GDP
        url_gdp = url_indicators + pais + '/indicator/' + gdp + '?format=Json'
        response = requests.get(url_gdp)
        data_gdp = response.json()[1]

        # Para obtener dato POP
        url_pop = url_indicators + pais + '/indicator/' + pop + '?format=Json'
        response = requests.get(url_pop)
        data_pop = response.json()[1]
        contexto = {
            'lista_paises': data_paises,
            'info_income': data[0],
            'info_gdp': data_gdp[1],
            'info_pop': data_pop[1]
        }
        return render(request, "web/index.html", contexto)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')

def insertar_consulta_usuario(request):
    # URL para genar la lista de búsqueda
    url_paises = 'https://api.worldbank.org/v2/country?format=Json'
    response = requests.get(url_paises)
    # response.raise_for_status()
    data_paises = response.json()[1]

    name = request.POST['txtName']
    lastname = request.POST['txtLastname']
    email = request.POST['txtEmail']
    pais = request.POST['country']
    income = request.POST['income']
    gdp = request.POST['gdp']
    population = request.POST.getlist('population')
    datos_api =", ".join([pais, income, gdp, str(population)])
    i = Ingresar()
    resultado = i.guardar_consulta(name, lastname, email, datos_api)
    contexto = {
        'lista_paises': data_paises,
        'datos_enviados': resultado
    }
    return render(request, "web/index.html", contexto)

def lista_propuestas(request):
    try:
        i = Ingresar()
        data = i.consulta()
        contexto = {'consultas': data}
        return render(request, 'web/lista_propuestas.html', contexto)
    except cx_Oracle.Error as error:
        print(request, f"Error al cargar propuestas: {str(error)}")
        return render(request, 'web/lista_propuestas.html', {'propuestas': []})
