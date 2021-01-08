G01 - WebsMusic
Pedro Valente - 88858
Renato Valente - 89077
Samuel Duarte - 89222


-----------------------------------
Como executar/utilizar a aplicação 
-----------------------------------

Dependências do Python
	python interpreter: Python 3.8
	Django 3.1
	s4api
	SPARQLWrapper 1.8.5

Executar
	Executar o GraphDB Free
	Importar o ficheiro "dataset.rdf" para um repositório no GraphDB Free chamado "xpand-music"
	Executar a WebApp (ex: python manage.py runserver)




-------------------------
Tópicos mais importantes
-------------------------

Este projeto foi construído utilizando a plataforma Django, tendo como repositório de dados a Triplestore GraphDB importado de um ficheiro "dataset.rdf". Todas as queries feitas à BD utilizaram a linguagem SPARQL (queries de pesquisa, inserção e remoção). Foi também utilizado RDFa nas páginas com informação mais extensa. Por fim, foi usado o sparql endpoint através da biblioteca python "SPARQLwrapper" para recolher dados em runtime sobre álbuns não presentes na base de dados.


Páginas existentes e o que utilizam:

Nota: Em todas as páginas existe uma search bar que funciona à base de literais

-Home
Página de entrada da aplicação, escolhendo um dos álbuns recomendados o utilizador é remetido para uma página com informações sobre esse álbum, esta informação é recolhida em runtime à dbpedia pois estes álbuns não se encontram na base de dados.
Usa SPARQL (pesquisa de dados) e SPARQLwrapper (dbpedia em runtime).

-Artists
Página com todos os artistas presentes na BD (é possível ordenar), clicando no nome do artista o utilizador é remetido para uma página com todas as músicas do artista presentes na base de dados.
Ambas as páginas usam SPARQL (pesquisa de dados). 

-Songs
Página com todas as músicas presentes na BD (é possível ordenar), clicando no nome do artista o utilizador é remetido para uma página com todas as músicas do artista presentes na base de dados.
Usa SPARQL (pesquisa de dados).

-Albums
Página com todos os álbuns presentes na base de dados, seus artistas e alguns tópicos de informação.
Clicando no nome do álbum o utilizador é remetido para uma página com mais informação que pode ser pertinente, esta página é construída através de RDFa.
Usa SPAQRL (pesquisa de dados) e RDFa.

-Create Playlist
Página com todas as músicase seus artistas presentes na base de dados, o utilizador pode depois escolher músicas e juntá-las numa playlist com um nome à sua escolha, esta playlist é de seguida guardada na base de dados.
Usa SPARQL (pesquisa e inserção de dados).

-My Playlist
Página com todas as playlists criadas pelo utilizador, o utilizador pode também apagar uma playlist se assim o desejar, toda a informação é demonstrada através de RDFa.
Usa SPARQL (pesquisa e remoção de dados) e RDFa.

-Known Artists
Página que cria uma inferência, dado um artista pelo utilizador que esteja na base de dados é pesquisada as editoras desse artista e procura artistas que tenham editoras em comum. Para verificar a existência do artista introduzido pelo utilizador é feita uma querie do tipo ask á base de dados.
Usa SPARQL (pesquisa e inserção de dados).

