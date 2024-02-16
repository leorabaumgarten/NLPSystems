## Python version

Run the apps with Python version 3.10.13.

## Required modules

- fastapi==0.109.2
- pydantic==2.6.0
- uvicorn==0.21.1
- Flask==3.0.2
- streamlit==1.31.0
- pandas==2.2.0
- altair==5.2.0
- graphviz==0.20.1
- spacy==3.7.2

## Running the apps

cd to the Project 1 directory. Then, for the RESTful API, run `uvicorn app_fastapi:app`, for the Flask webserver, run `flask --app app_flask run`, and for the Streamlit application run `streamlit run app_streamlit.py`.

## Using the apps

### RESTful API

Run `curl http://127.0.0.1:8000`to see a description of the API.  
For NER, run

```
curl -X POST -H "Content-Type: application/json" -d@input.json http://127.0.0.1:8000/ner
```

and for dependency parsing, run

```
curl -X POST -H \"Content-Type: application/json\" -d@input.json http://127.0.0.1:8000/dep
```

For nicely formatted results, add `?pretty=true` to the end of the urls in any of the previous commands.

### Flask webserver

Load `http://127.0.0.1:5000/` in your browser to access the Flask webserver.

### Streamlit application

Load `http://localhost:8501/` in your browser to access the Streamlit application.
