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
import datetime

# from lxml import etree
# from urllib.request import urlopen
# import datetime

_endpoint = "http://localhost:7200"
_repositorio = "xpand-music"

client = ApiClient(endpoint=_endpoint)
accessor = GraphDBApi(client)


# Create your views here.

def home(request):
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
        info[unquote(m['tname']['value'])]['embed'] = "https://www.youtube.com/embed/" + unquote(m['youtube']['value'])

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
        temp['nome'] = a['albumName']['value']
        info[unquote(a['albumName']['value'])] = temp
        # info[a['id']['value']] = unquote(a['aname']['value'])

    tparams = {
        'albums': info,
        'frase': "Albums:",
    }
    return render(request, "albums.html", tparams)


def albumInfo(request):
    id = str(request.GET.get('id'))
    print(request.GET)
    tparams = dict()
    query_BasicInfo = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX cs: <http://www.xpand.com/rdf/>
                            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                            select ?album ?idArt ?aname ?wiki ?bio ?data ?genero ?prevAlbum ?nextAlbum ?count ?img ?recorder ?producer
                            where {
                                ?album foaf:name "%s" .
                                ?album rdf:type cs:Album .
                                ?album cs:MusicArtist ?idArt .
                                ?idArt foaf:name ?aname .
                                ?album cs:WikiData ?wiki .
                                ?album cs:biography ?bio .
                                ?album cs:datePublished ?data .
                                ?album cs:genre ?genero .
                                optional{
                                    ?album cs:previousAlbum ?prevAlbum .
                                }
                                optional{
                                    ?album cs:nextAlbum ?nextAlbum .
                                }
                                ?album cs:playCount ?count .
                                optional{
                                     ?album cs:producer ?producer .
                                }
                            #    ?album cs:similarAlbum ?simAlbum .
                                ?album foaf:Image ?img .

                            }''' % (quote(id))
    _body = {"query": query_BasicInfo}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)
    res = res['results']['bindings'][0]
    print(res)
    tparams['name'] = id
    tparams['uri'] = res['album']['value']
    tparams['idArtista'] = res['idArt']['value']
    tparams['aname'] = unquote(res['aname']['value'])
    tparams['img'] = res['img']['value']
    tparams['bio'] = unquote(res['bio']['value'])
    tparams['data'] = res['data']['value']
    tparams['genero'] = unquote(res['genero']['value'])
    tparams['playCount'] = res['count']['value']
    tparams['prevAlbum'] = None
    tparams['nextAlbum'] = None
    tparams['producer'] = None
    print(res.keys())
    if ('prevAlbum' in res.keys()):
        tparams['prevAlbum'] = unquote(res['prevAlbum']['value'])
    if ('nextAlbum' in res.keys()):
        tparams['nextAlbum'] = unquote(res['nextAlbum']['value'])
    if ('producer' in res.keys()):
        tparams['producer'] = unquote(res['producer']['value'])

    query_Tags = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX cs: <http://www.xpand.com/rdf/>
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                        select ?idTag ?tag 
                        where {
                            ?album foaf:name "%s" .
                            ?album rdf:type cs:Album .
                            ?album cs:Tag ?idTag .
                            ?idTag foaf:name ?tag .
                        }
                        ''' % (quote(id))

    _body = {"query": query_Tags}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    tags = dict()
    for t in res['results']['bindings']:
        tags[unquote(t['tag']['value'])] = t['idTag']['value']
    tparams['tags'] = tags

    query_simAlbums = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX cs: <http://www.xpand.com/rdf/>
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                        select ?simAlbum ?name
                        where {
                            ?album foaf:name "%s" .
                            ?album rdf:type cs:Album .
                            ?album cs:similarAlbum ?simAlbum .
                            ?simAlbum foaf:name ?name .
                        } ''' % (quote(id))

    _body = {"query": query_simAlbums}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    simAlbums = dict()
    for a in res['results']['bindings']:
        temp = dict()
        temp['uri'] = a['simAlbum']['value']
        temp['id'] = a['name']['value']
        simAlbums[unquote(a['name']['value'])] = temp
    tparams['simAlbums'] = simAlbums

    query_recorders = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX cs: <http://www.xpand.com/rdf/>
                            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                            select ?recorder
                            where {
                                ?album foaf:name "%s" .
                                ?album rdf:type cs:Album .
                                ?album cs:recorder ?recorder .

                            }  ''' % (quote(id))

    _body = {"query": query_recorders}
    res = accessor.sparql_select(body=_body, repo_name=_repositorio)
    res = json.loads(res)

    recorders = []
    for r in res['results']['bindings']:
        recorders.append(unquote(r['recorder']['value']))
    tparams['recorders'] = recorders

    return render(request, "albumRDFa.html", tparams)


def criarPlayList(request):
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
        info[unquote(m['tname']['value'])] = dict()
        info[unquote(m['tname']['value'])]["artista"] = unquote(m['aname']['value'])
        info[unquote(m['tname']['value'])]["id"] = m['id']['value']

    if 'playlistName' in request.POST:
        nomes = request.POST.getlist('nameMusica')
        playlistNome = request.POST['playlistName']
        # print(len(nomes))
        print(nomes)
        if len(nomes) == 0 or playlistNome == "":
            tparams = {
                'tracks': info,
                'frase': "Songs:",
                'erro': True
            }
            return render(request, "criarPlayList.html", tparams)
        else:
            tparams = {
                'tracks': info,
                'frase': "Songs:",
                'erro': False
            }

            querysIDS = """
                        PREFIX cs: <http://www.xpand.com/rdf/>
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        select * where { 
                            ?p rdf:type cs:Playlist
                        } 
                    """
            _body = {"query": querysIDS}
            res = accessor.sparql_select(body=_body, repo_name=_repositorio)
            res = json.loads(res)


            id = "http://www.xpand.com/playlist/" + playlistNome

            for i in res['results']['bindings']:
                if id == i['p']['value']:
                    tparams = {
                        'tracks': info,
                        'frase': "Songs:",
                        'erro': True
                    }
                    return render(request, "criarPlayList.html", tparams)

            query_insert = """
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX cs: <http://www.xpand.com/rdf/>
                            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

                            insert data {
                                <%s> rdf:type cs:Playlist .
                                <%s> foaf:name "%s" .
                                <%s> cs:NumItems "%s" .
                                <%s> cs:datePublished "%s"
                            }
                            """ % (id, id, playlistNome, id, len(nomes), id, str(datetime.date.today()))
            _body = {"update": query_insert}
            res1 = accessor.sparql_update(body=_body, repo_name=_repositorio)

            for musica in nomes:
                query_de_insert = """
                                PREFIX cs: <http://www.xpand.com/rdf/>
                                insert data {<%s> cs:Track <%s>}
                            """ % (id, musica)
                print(musica)
                print(id)
                # listArtistas.append(a['outras']['value'])
                _body = {"update": query_de_insert}
                res1 = accessor.sparql_update(body=_body, repo_name=_repositorio)

            return render(request, "criarPlayList.html", tparams)
    else:
        tparams = {
            'tracks': info,
            'frase': "Songs",
            'erro': False
        }
        return render(request, "criarPlayList.html", tparams)


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

    # listArtistas = []
    art = res['results']['bindings'][0]['banda']['value']
    print(art)
    for a in res['results']['bindings']:
        if a['outras']['value'] != art:
            query_insert = """
                        insert data {<%s> foaf:knows <%s>}
                    """ % (art, a['outras']['value'])
            # listArtistas.append(a['outras']['value'])
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
