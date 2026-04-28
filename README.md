# Progetto1FAS

Il progetto proposto consiste in un'analisi computazionale applicata a un dataset di tipologia linguistica.

## Tecnologie utilizzate

Le tecnologie impiegate nel workflow sono:

- Git
- Docker
- Ansible
- Python3
- Modulo venv di Python3
- Bash
- xan
- Modulo pandas di Python3
- Modulo matplotlib di Python3
- Modulo jupyterlab di Python3
- Modulo geopandas di Python3
- Modulo ipywidgets di Python3

Sebbene l'adozione di alcune di queste tecnologie possa apparire sovradimensionata rispetto alla scala del progetto,
si è scelto di integrarne il maggior numero tra quelle esaminate durante il corso.
Tale approccio permette di condensare in un unico output le competenze maturate nella prima metà dell'insegnamento,
pur consapevoli che alcune implementazioni possano risultare volutamente elaborate.

## Dipendenze del progetto

Per l'inizializzazione del progetto è necessaria l'installazione preventiva di Git e Docker.

## Avvio

- Clonazione della repository:

```bash
git clone [https://github.com/FedeBrus/Progetto1FAS](https://github.com/FedeBrus/Progetto1FAS)
```

- Build dell'immagine di progetto:

```bash
docker build --network=host -t wals .
```

- Esecuzione del container:

```bash
docker run --rm -p 8888:8888 wals
```

Una volta avviato, il container eseguirà JupyterLab e genererà un token di autenticazione;
sarà sufficiente copiare il link prodotto all'interno di un browser per accedere all'ambiente di lavoro e ai notebook.

### Sviluppo

Il progetto è stato sviluppato mediante l'ausilio di Git e VSCode. Durante le fasi di implementazione si è fatto ricorso a risorse online,
tra cui documentazione ufficiale, forum tecnici (nello specifico StackOverflow) e strumenti basati su LLM (in particolare Gemini).
Ogni riferimento esterno è stato oggetto di cross-referencing con la documentazione ufficiale per garantirne l'accuratezza.

// Storia dei branch

\newpage

### Struttura del progetto

```  
.
├── ansible
│   ├── hosts
│   ├── jupyter.yml
│   └── roles
│       └── setup_wals_analysis
│           ├── tasks
│           │   ├── main.yml
│           │   ├── python_setup.yml
│           │   ├── system_packages.yml
│           │   └── xan_install.yml
│           └── vars
│               └── main.yml
├── dataset
│   ├── processed
│   │   └── features.csv
│   └── raw
│       ├── codes.csv
│       ├── countries.csv
│       ├── languages.csv
│       ├── parameters.csv
│       └── values.csv
├── Dockerfile
├── notebooks
│   ├── Part0.ipynb
│   ├── Part1.ipynb
│   ├── Part2.ipynb
│   ├── Part3.ipynb
│   └── Part4.ipynb
├── output.pdf
├── README.md
├── requirements.txt
├── scripts
│   ├── fetch.sh
│   ├── join.sh
│   ├── prune.sh
│   └── utils.sh
└── src
    ├── __init__.py
    ├── __pycache__
    │   ├── info.cpython-314.pyc
    │   ├── loader.cpython-314.pyc
    │   ├── plotter.cpython-314.pyc
    │   └── stats.cpython-314.pyc
    ├── info.py
    ├── loader.py
    ├── plotter.py
    └── stats.py
```

### Script Bash

Sono stati predisposti tre script Bash deputati alle operazioni di recupero del dataset da GitHub (fetch.sh),
alla potatura (pruning) dei dati non funzionali all'analisi (prune.sh) e, infine, alla denormalizzazione del dataset (join.sh)
per consentire l'operatività su un file unico. Si è preferito l'utilizzo di xan rispetto a csvkit per inclinazione metodologica,
pur essendo i due strumenti intercambiabili nel contesto specifico.

### Dockerfile

Si è optato per l'impiego di Docker al fine di garantire la piena riproducibilità dell'ambiente di runtime e consentire l'avvio del progetto
tramite un singolo comando. È stato redatto un Dockerfile per la generazione di un'immagine personalizzata basata su Ubuntu 24.04;
tale distribuzione è stata scelta per semplificare la gestione delle dipendenze, nonostante l'alternativa Alpine avrebbe garantito una maggiore leggerezza.
La versione della distribuzione è stata fissata per prevenire eventuali criticità di compatibilità future.
Il Dockerfile orchestra l'installazione e l'esecuzione di Ansible per la gestione delle dipendenze, gestisce la persistenza dei file,
i permessi di esecuzione degli script shell e la loro invocazione. All'avvio del container, viene inizializzato il servizio JupyterLab.

### Ansible
Ansible presiede all'installazione delle dipendenze di progetto. Il file hosts assolve alla funzione di definire il target sul localhost del container.
La configurazione segue una struttura standard, basata su un ruolo composto dai seguenti task:
  - Installazione dei pacchetti di sistema
  - Installazione di xan (strumento non presente nei principali package manager, incluso APT)
  - Installazione dei moduli Python necessari, definiti nel file requirements.txt

Il ruolo di setup si occupa di coordinare ed eseguire tali operazioni.
File Python

I sorgenti Python sono organizzati in un modulo dedicato, successivamente importato dai notebook.
Questi espongono diverse funzioni di utilità per il caricamento del dataset e la generazione di visualizzazioni grafiche mediante le librerie Geopandas e Matplotlib.

### Jupyter
L'attività di analisi è ripartita in cinque notebook:
  - Part0: disamina del contenuto del dataset.
  - Part1: elaborazioni statistiche sulle lingue, categorizzate per regioni geografiche e affiliazioni genealogiche.
  - Part2: analisi dei valori assunti da determinati parametri in relazione alle regioni geografiche e alle diramazioni genealogiche.
  - Part3: visualizzazione della distribuzione geospaziale delle lingue e dei relativi valori parametrici.
  - Part4: analisi delle correlazioni incrociate tra i valori dei parametri presi in esame.
