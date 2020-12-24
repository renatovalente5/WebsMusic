# import base64
import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from urllib.parse import unquote, quote
# from BaseXClient import BaseXClient
from lxml import etree
import xmltodict
# import requests
import random

# from lxml import etree
# from urllib.request import urlopen
# import datetime

_endpoint = "http://localhost:7200"
_repositorio = "xpand-music"

client = ApiClient(endpoint=_endpoint)
accessor = GraphDBApi(client)


# Create your views here.

def home(request):
    # return HttpResponse("GOOD LUCK")
    # input = "xquery import module namespace funcsPlaylist = 'com.funcsPlaylist.my.index'; funcsPlaylist:home()"
    # query = session.execute(input)
    # # print(query)
    # info = dict()
    # res = xmltodict.parse(query)
    # # print(res)
    # for i in range(8):
    #     c = random.choice(res["root"]["elem"])
    #     info[c["name"]] = dict()
    #     info[c["name"]]["url"] = c["spotify"]
    #     info[c["name"]]["imagem"] = c["url"][2]
    #     info[c["name"]]["artistas"] = dict()
    #     if isinstance(c["artista"], list):
    #         for art in c["artista"]:
    #             info[c["name"]]["artistas"][art["name"]] = art["id"]
    #     else:
    #         info[c["name"]]["artistas"][c["artista"]["name"]] = c["artista"]["id"]

    query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX cs: <http://www.xpand.com/rdf/>
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
                    select ?id ?tname ?aname ?youtube
                    where { 
                        ?id rdf:type cs:Track .
                        ?id foaf:name ?tname .
                        ?id cs:youtubeVideo ?youtube .
                        ?id cs:MusicArtist ?artist .
                        ?artist foaf:name ?aname 
                        
                    }'''

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    print(res)
    info = dict()

    for i in range(8):
        m = random.choice(res['results']['bindings'])
        info[unquote(m['tname']['value'])] = dict()
        info[unquote(m['tname']['value'])]['artista'] = unquote(m['aname']['value'])
        info[unquote(m['tname']['value'])]['url'] = "https://www.youtube.com/watch?v=" + unquote(m['youtube']['value'])

    tparams = {
        'tracks': info,
        'frase': "Songs",
    }
    return render(request, "home.html", tparams)


def musicas(request):
    query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX cs: <http://www.xpand.com/rdf/>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                
                select ?id ?tname ?aname
                where { 
                    ?id rdf:type cs:Track .
                    ?id foaf:name ?tname .
                    ?id cs:MusicArtist ?artist .
                    ?artist foaf:name ?aname
                }'''

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    # print(res);
    info = dict()

    for m in res['results']['bindings']:
        info[unquote(m['tname']['value'])] = unquote(m['aname']['value'])

    tparams = {
        'tracks': info,
        'frase': "Songs",
    }
    return render(request, "tracks.html", tparams)


def artist_tracks(request):
    id = str(request.GET.get('id'))
    query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX cs: <http://www.xpand.com/rdf/>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                
                select ?id ?track ?music ?video
                where {
                    ?id foaf:name  "%s".
                    ?track cs:MusicArtist ?id .
                    ?track foaf:name ?music .
                    ?track cs:youtubeVideo ?video .
                }''' % (quote(id))

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    # print(res)
    info = dict()
    for t in res['results']['bindings']:
        info[unquote(t['music']['value'])] = "https://www.youtube.com/embed/" + t['video']['value']
    tparams = {
        'tracks': info,
        'frase': "Músicas do Artista: " + id
    }
    return render(request, "artist_tracks.html", tparams)


def artistas(request):
    query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX cs: <http://www.xpand.com/rdf/>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                
                select ?id ?aname ?img
                where { 
                    ?id rdf:type cs:MusicArtist .
                    ?id foaf:name ?aname .
                    ?id foaf:Image ?img
                }'''

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    # print(res);
    info = dict()
    for a in res['results']['bindings']:
        temp = dict()
        temp['id'] = a['id']['value']
        temp['img'] = a['img']['value']
        info[unquote(a['aname']['value'])] = temp
        # info[a['id']['value']] = unquote(a['aname']['value'])

    # print(info)
    tparams = {
        'info': info,
        'frase': "Artistas:",
    }
    return render(request, "artistas.html", tparams)


def albums(request):
    query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX cs: <http://www.xpand.com/rdf/>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                
                select ?albumName ?aname ?producer ?recorder ?data ?count
                where {
                    ?album rdf:type cs:Album .
                    ?album foaf:name ?albumName .
                    ?album cs:MusicArtist ?idArt .
                    ?idArt foaf:name ?aname .
                    ?album cs:producer ?producer .
                    ?album cs:recorder ?recorder .
                    ?album cs:datePublished ?data .
                    ?album cs:playCount ?count .
                }'''

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    # print(res);
    info = dict()
    for a in res['results']['bindings']:
        temp = dict()
        temp['artista'] = unquote(a['aname']['value'])
        temp['producer'] = unquote(a['producer']['value'])
        temp['recorder'] = unquote(a['recorder']['value'])
        temp['data'] = a['data']['value']
        temp['streams'] = a['count']['value']
        info[unquote(a['albumName']['value'])] = temp
        # info[a['id']['value']] = unquote(a['aname']['value'])

    tparams = {
        'albums': info,
        'frase': "Albums:",
    }
    return render(request, "albums.html", tparams)


def criarPlayList(request):
    return None
    # lastID = "xquery import module namespace funcsPlaylist = 'com.funcsPlaylist.my.index'; funcsPlaylist:last-playlistID()"
    # query = session.execute(lastID)
    #
    # # Verifica se esta alguma playlist na BD, se nao coloca o primeiro id a 1
    # if query != '':
    #     res = xmltodict.parse(query)
    #     id = str(int(res["id"]) + 1)
    # else:
    #     id = "1"
    #
    # input = "xquery import module namespace funcsPlaylist = 'com.funcsPlaylist.my.index'; funcsPlaylist:musicas()"
    # query = session.execute(input)
    # # print(query)
    # info = dict()
    # res = xmltodict.parse(query)
    #
    # for c in res["root"]["elem"]:
    #     info[c["name"]] = dict()
    #     info[c["name"]]["url"] = c["spotify"]
    #     info[c["name"]]["id"] = c["id"]
    #     info[c["name"]]["imagem"] = c["url"][2]
    #     info[c["name"]]["artistas"] = dict()
    #     if isinstance(c["artista"], list):
    #         for art in c["artista"]:
    #             info[c["name"]]["artistas"][art["name"]] = art["id"]
    #     else:
    #         info[c["name"]]["artistas"][c["artista"]["name"]] = c["artista"]["id"]
    # #print(request.POST)
    #
    # if 'playlistName' in request.POST:
    #     nomes = request.POST.getlist('nameMusica')
    #     playlistNome = request.POST['playlistName']
    #     print(len(nomes))
    #     if len(nomes) == 0 or playlistNome == "":
    #         tparams = {
    #             'artistas': True,
    #             'tracks': info,
    #             'frase': "Songs from Playlist Pokémon LoFi:",
    #             'erro': True
    #         }
    #         return render(request, "criarPlayList.html", tparams)
    #
    #     musicas = dict()
    #     for nMusicas in nomes:
    #         print(nMusicas)
    #         input = "xquery import module namespace funcsPlaylist = 'com.funcsPlaylist.my.index'; funcsPlaylist:info-musica('{}')".format(
    #             nMusicas)
    #         query = session.execute(input)
    #         res = xmltodict.parse(query)
    #         print(res["root"]["elem"])
    #         musica = res["root"]["elem"]
    #         musicas[musica["name"]] = dict()
    #         musicas[musica["name"]]["id"] = musica["id"]
    #         musicas[musica["name"]]["externalUrl"] = musica["spotify"]
    #         musicas[musica["name"]]["img"] = musica["url"]
    #         musicas[musica["name"]]["artistas"] = dict()
    #         if isinstance(musica["artista"], list):
    #             for art in musica["artista"]:
    #                 musicas[musica["name"]]["artistas"][art["name"]] = art["id"]
    #         else:
    #             musicas[musica["name"]]["artistas"][musica["artista"]["name"]] = musica["artista"]["id"]
    #
    #     criarxml(id, playlistNome, str(len(nomes)), musicas)
    #     return redirect(myPlayList)
    # else:
    #     tparams = {
    #         'artistas': True,
    #         'tracks': info,
    #         'frase': "Songs from Playlist Pokémon LoFi:",
    #         'erro': False
    #     }
    #     return render(request, "criarPlayList.html", tparams)


def insertKnowsArtist(artista):
    query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX cs: <http://www.xpand.com/rdf/>
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                        select ?banda  ?outras
                        where
                        {
                            ?banda foaf:name "%s" .
                            ?banda cs:recorder ?recorder .
                            ?outras cs:recorder ?recorder .
                            ?outras rdf:type cs:MusicArtist .
                        }''' % (quote(artista))

    _body = {"query": query}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    print(res)

    #listArtistas = []
    art = res['results']['bindings'][0]['banda']['value']
    for a in res['results']['bindings']:
        if a['outras']['value'] != art:
            query_insert = """
                        insert data {<%s> foaf:knows <%s>}
                    """ % (art, a['outras']['value'])
            #listArtistas.append(a['outras']['value'])
        _body = {"update": query_insert}
        res1 = accessor.sparql_update(body=_body, repo_name=_repositorio)



def knowArtists(request):
    info = dict()
    if 'ArtistName' in request.POST:
        artistNome = request.POST['ArtistName']
        print(artistNome)

        if artistNome == "":
            tparams = {
                'info': info,
                'frase': "Artists",
                'erro': True
            }
            return render(request, "knowArtists.html", tparams)

        insertKnowsArtist(artistNome)
        query = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX cs: <http://www.xpand.com/rdf/>
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                    select ?banda  ?anome ?img
                    where
                    {
                        ?banda foaf:name "%s" .
                        ?banda foaf:knows ?outra .
                        ?outra foaf:name ?anome .
                        ?outra foaf:Image ?img .
                    }''' % (quote(artistNome))

        _body = {"query": query}
        res = accessor.sparql_select(body=_body, repo_name=_repositorio)
        res = json.loads(res)
        print(res)

        for a in res['results']['bindings']:
            info[unquote(a['anome']['value'])] = a['img']['value']

    tparams = {
        'info': info,
        'frase': "Artists:",
        'erro': False
    }
    return render(request, "knowArtists.html", tparams)


def myPlayList(request):
    return None
    # input = "xquery <root>{for $a in collection('SpotifyPlaylist')//playlistDemo return $a }</root>"
    # query = session.execute(input)
    #
    # xml = etree.fromstring(query)
    # xslt_file = etree.parse("files/myPlayList.xsl")
    # transform = etree.XSLT(xslt_file)
    # html = transform(xml)
    #
    # tparams = {
    #     'playlist': html,
    #     'frase': "Playlists:",
    # }
    # return render(request, "myPlayList.html", tparams)


def delete(request):
    return None
    # id = request.GET['id']
    # print(id)
    # delete = "xquery import module namespace funcsPlaylist = 'com.funcsPlaylist.my.index'; funcsPlaylist:delete-playlist({})".format(id)
    # session.execute(delete)
    #
    # return redirect(myPlayList)

# def pageRSS(request):
#     url = 'https://pitchfork.com/rss/news/'
#     resp = requests.get(url)
#
#     xml = etree.fromstring(resp.content)
#
#     xslt_file = etree.parse("files/pageRSS.xsl")
#     transform = etree.XSLT(xslt_file)
#     html = transform(xml)
#
#     tparams = {
#         'pageRSS': html,
#         'frase': "Page RSS:",
#     }
#     return render(request, "pageRSS.html", tparams)
