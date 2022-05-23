## Avvertenze

Usare le cartella "backend" come root del componente da sviluppare.

L'applicato Backend dovrà girare sulla porta 8000 su localhost.
Per lanciare lo stack è necessario usare docker-compose.

Per lanciare l'applicativo usare il comando 'bin/start.sh'.
Per fermale lo stack applicativo usare il comando 'bin/stop.sh'.

## Root Del Progetto

Progetto per il test pratico per backend Marco Vannoli

## Installation

Per inizializzare il progetto seguire i seguenti comandi:

Stare nella root rpincipale del progetto:

```bash
pip install -r requirements.txt
```

Cambiare path del progetto nella variabile del file config.py:

```python
pathProject = <local path of the project>
```

## Usage of API (start API)

Andare sotto cartella backend:
```bash
uvicorn main:app –reload
```

Andare nel l'url: http://127.0.0.1:8000/docs (FastApi)



## MongoDB

Usare MongoDB Compass:

Stringa di connessione : "mongodb+srv://vannoli:PassWord95@clusterbigprofile.cqrw1.mongodb.net/test"

Database : "BigProfilesDB"

Collection :  "BigProfilesData"

## Test Api Client

usare i metodi per richiamanre l'api el file test.py
