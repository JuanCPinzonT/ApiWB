#Búsqueda de Organizaciones

identifier =  'cHJ1ZWJhOmp1YW5jYW1pbG8tOTk1QGhvdG1haWwuY29t'
url_orgs = 'https://hapi.humdata.org/api/v2/coordination-context/operational-presence?app_identifier='
quantity = input('Please enter max results (max 10000)')
format = '&output_format=json&limit='+quantity+'&offset=0'

url_orgs_final = url_orgs +identifier+ format
print(url_orgs_final)

#Poverty rate
url_poverty = 'https://hapi.humdata.org/api/v2/food-security-nutrition-poverty/poverty-rate?app_identifier='
url_poverty_final = url_poverty +identifier+ format

#Population
url_population = 'https://hapi.humdata.org/api/v2/geography-infrastructure/baseline-population?app_identifier='
url_population_final = url_poverty +identifier+ format

