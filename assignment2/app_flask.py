"""Simple Web interface to spaCy NER and dependency parser

To see the pages point your browser at http://127.0.0.1:5000.
"""


from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import nlp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc17ef05b0e34d7a4d5ee9daff970079'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    dependencies = db.relationship('Dependency', backref='entity', lazy=True)

class Dependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String, nullable=False)
    arc = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        input = open('input.txt', encoding='utf8').read()
        return render_template('form.html', input=input)
    else:
        text = request.form['text']
        doc = nlp.SpacyDocument(text)

        markup = doc.get_entities_with_markup()
        ner_formatted = ''
        for line in markup.split('\n'):
            if line.strip() == '':
                ner_formatted += '<p/>\n'
            else:
                ner_formatted += line
        
        deps_by_sent = doc.get_dependencies_by_sent()
        
        deps_by_ent = doc.get_entity_dependencies()
        for ent in deps_by_ent:
            entity = db.session.query(Entity).filter_by(entity=str(ent)).first()
            if entity:
                entity.count = entity.count + 1
            else:
                entity = Entity(entity=str(ent), count=1)
                db.session.add(entity)
            db.session.commit()
            for dep in deps_by_ent[ent]:
                entity = Entity.query.filter_by(entity=str(ent)).first()
                head = dep['head']
                arc = dep['arc']
                text = dep['text']
                dependency = db.session.query(Dependency).filter_by(head=head, arc=arc, text=text, entity_id=entity.id).first()
                if dependency:
                    dependency.count = dependency.count + 1
                else:
                    dependency = Dependency(head=dep['head'], arc=dep['arc'], text=dep['text'], entity_id=entity.id, count=1)
                    db.session.add(dependency)
                db.session.commit()

        return render_template('result.html', markup=ner_formatted, deps=deps_by_sent)
    
@app.route('/database', methods=['GET'])
def database():
    entities = db.session.query(Entity.entity, Entity.count, Dependency.head, Dependency.arc, Dependency.text, Dependency.count).filter(Entity.id == Dependency.entity_id)
    ents = {}
    for ent in entities:
        entity = ent[0]
        entity_count = ent[1]
        dep = (ent[2], ent[3], ent[4])
        dep_count = ent[5]
        if entity in ents:
            ents[entity]['dependencies'][dep] = dep_count
        else:
            ents[entity] = {'count': entity_count, 'dependencies': {dep: dep_count}}
    return render_template('database.html', entities=ents)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
