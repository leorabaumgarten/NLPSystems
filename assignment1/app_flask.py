"""Simple Web interface to spaCy NER and dependency parser

To see the pages point your browser at http://127.0.0.1:5000.
"""


from flask import Flask, request, render_template

import nlp

app = Flask(__name__)


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
        deps = doc.get_dependencies_by_sent()
        return render_template('result.html', markup=ner_formatted, deps=deps)


if __name__ == '__main__':

    app.run(debug=True)
