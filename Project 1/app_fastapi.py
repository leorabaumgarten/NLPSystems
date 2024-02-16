"""
FastAPI interface to spaCy NER and dependency parser
"""

import json
from fastapi import FastAPI, Response
from pydantic import BaseModel
import ner

app = FastAPI()


class Item(BaseModel):
    text: str = ''


@app.get('/')
def index(pretty: bool = False):
    command = 'curl -X POST -H "Content-Type: application/json"'
    ner_url = 'http://127.0.0.1:8000/ner'
    dep_url = 'http://127.0.0.1:8000/dep'
    answer = {
        'description': 'Interface to the spaCy NER and dependency extractor',
        'usage': {'entities': '%s -d@input.json %s' % (command, ner_url),
                  'dependencies': '%s -d@input.json %s' % (command, dep_url)}}
    if pretty:
        answer = prettify(answer)
    return answer


@app.post('/ner')
def entities(item: Item, pretty: bool = False):
    doc = ner.SpacyDocument(item.text)
    answer = {'input': item.text, 'output': doc.get_entities()}
    if pretty:
        answer = prettify(answer)
    return answer


@app.post('/dep')
def dependencies(item: Item, pretty: bool = False):
    doc = ner.SpacyDocument(item.text)
    answer = {'input': item.text, 'output': doc.get_dependencies()}
    if pretty:
        answer = prettify(answer)
    return answer


def prettify(result: dict):
    json_str = json.dumps(result, indent=2)
    return Response(content=json_str, media_type='application/json')
