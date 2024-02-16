from collections import Counter
from operator import itemgetter

import streamlit as st
import pandas as pd
import altair as alt
import graphviz

import ner


example = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")


# st.set_page_config(layout='wide')
st.markdown('## spaCy Visualization')

text = st.text_area('Text to process', value=example, height=100)

doc = ner.SpacyDocument(text)

with st.sidebar:
    add_radio = st.radio("Select view", ("entities", "dependencies"))

if add_radio == "entities":

    entities = doc.get_entities()
    tokens = doc.get_tokens()
    counter = Counter(tokens)
    words = list(sorted(counter.most_common(30)))

    # https://pandas.pydata.org
    chart = pd.DataFrame({
        'frequency': [w[1] for w in words],
        'word': [w[0] for w in words]})

    # https://pypi.org/project/altair/
    bar_chart = alt.Chart(chart).mark_bar().encode(x='word', y='frequency')

    num_tokens = len(tokens)
    num_types = len(counter)

    st.markdown(f'Total number of tokens: {num_tokens}<br/>'
                f'Total number of types: {num_types}', unsafe_allow_html=True)

    # https://docs.streamlit.io/library/api-reference/data/st.table
    st.table(entities)

    # https://docs.streamlit.io/library/api-reference/charts/st.altair_chart
    st.altair_chart(bar_chart)

else:
    table_tab, graph_tab = st.tabs(['table', 'graph'])
    dependencies = doc.get_dependencies_by_sent()
    with table_tab:
        charts = []
        for d in dependencies:
            heads = [token['head'] for token in d['tokens']]
            arcs = [token['arc'] for token in d['tokens']]
            tokens = [token['text'] for token in d['tokens']]
            chart = pd.DataFrame({'head': heads, 'arc': arcs, 'token': tokens})
            charts.append(chart)
        for sent, chart in zip([d['sent'] for d in dependencies], charts):
            st.info(sent)
            st.table(chart)
    with graph_tab:
        graphs = []
        for d in dependencies:
            graph = graphviz.Digraph()
            for token in d['tokens']:
                graph.edge(token['head'], token['text'], label=token['arc'])
            graphs.append(graph)
        for sent, graph in zip([d['sent'] for d in dependencies], graphs):
            st.info(sent)
            st.graphviz_chart(graph)
