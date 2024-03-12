"""
Run spaCy NER over an input string and insert XML tags for each entity.
"""


import io
import spacy


nlp = spacy.load('en_core_web_sm')


class SpacyDocument:

    def __init__(self, text: str):
        self.text = text
        self.doc = nlp(text)

    def get_tokens(self) -> list:
        return [token.lemma_ for token in self.doc]

    def get_entities(self) -> str:
        entities = []
        for e in self.doc.ents:
            entities.append((e.start_char, e.end_char, e.label_, e.text))
        return entities

    def get_entities_with_markup(self) -> str:
        entities = self.doc.ents
        starts = {e.start_char: e.label_ for e in entities}
        ends = {e.end_char: True for e in entities}
        buffer = io.StringIO()
        for p, char in enumerate(self.text):
            if p in ends:
                buffer.write('</entity>')
            if p in starts:
                buffer.write('<entity class="%s">' % starts[p])
            buffer.write(char)
        markup = buffer.getvalue()
        return '<markup>%s</markup>' % markup

    def get_dependencies(self) -> str:
        dependencies = []
        for token in self.doc:
            dependencies.append((token.head.text, token.dep_, token.text))
        return dependencies

    def get_dependencies_by_sent(self):
        dependencies = []
        for sent in self.doc.sents:
            dep = {'sent': str(sent)}
            dep['tokens'] = []
            for token in sent:
                head = token.head.text
                arc = token.dep_
                text = token.text
                dep['tokens'].append({'head': head, 'arc': arc, 'text': text})
            dependencies.append(dep)
        return dependencies
    
    def get_entity_dependencies(self):
        dependencies = {}
        entities = self.doc.ents
        for entity in entities:
            if entity in dependencies:
                dependencies[entity].append([{'head': self.doc[i].head.text, 'arc': self.doc[i].dep_, 'text': self.doc[i].text} for i in range(entity.start, entity.end)])
            else:
                dependencies[entity] = [{'head': self.doc[i].head.text, 'arc': self.doc[i].dep_, 'text': self.doc[i].text} for i in range(entity.start, entity.end)]
        return dependencies

if __name__ == '__main__':

    example = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")

    doc = SpacyDocument(example)
    print(doc.get_tokens())
    for entity in doc.get_entities():
        print(entity)
    print(doc.get_entities_with_markup())
