import json
from pprint import pprint

import pymongo
import pygraphviz


client = pymongo.MongoClient()

db = client['literature']


def read_articles():
    def get_authors(a):
        for author_name in a['authors']:
            
            author = db.authors.find_one({'name': author_name})
            
            if author is None:
            
                r = db.authors.insert({'name':author_name})

                author = db.authors.find_one({'name': author_name})

            print(author)

            yield author

    with open('articles.json') as f:
        d = json.load(f)
    
    # new data
    for a in d['articles']:
        if not a['title']: continue
        
        a['authors'] = [author['_id'] for author in get_authors(a)]

        article = db.articles.find_one({'title': a['title']})

        if article is not None:
            print('article found')
        else:
            pprint(a)
            db.articles.insert(a)

    with open('articles.json', 'w') as f:
        json.dump({"articles":[{"title":"","notes":"","year":0,"authors":[]}],"the rest":d["the rest"]}, f, indent=8, sort_keys=True)
   

read_articles()
    
def author_id(s):
    return only(db.authors.find({'name':s}))['_id']

def list_articles():
    for a in db.articles.find():
        print('{} {}'.format(a['_id'], a['title']))



def plot(filt):

    c = db.articles.find(filt)
    
    g = pygraphviz.AGraph(directed=True)

    for a in c:
        g.add_node(str(a['_id']), label = a['title'], shape = 'box')

        for author_id in a['authors']:
            author = db.authors.find_one({'_id': author_id})
            g.add_edge(author['name'], str(a['_id']))
        
    for a in c:
        for b in a.get('references', []):
            g.add_edge(str(a['_id']), str(b['_id']))

    g.layout()
    g.draw('articles.png')


