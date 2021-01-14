# WebsMusic
This project was built using the Django platform, having as data repository the Triplestore GraphDB imported from a file "dataset.rdf". All queries made to BD used the SPARQL language. Some information pages were created with RDFa. 

## Dependências do Python
	python interpreter: Python 3.8
	Django 3.1
	s4api
	SPARQLWrapper 1.8.5

## Executar
	Executar o GraphDB Free
	Importar o ficheiro "dataset.rdf" para um repositório no GraphDB Free chamado "xpand-music"
	Executar a WebApp (ex: python manage.py runserver)
