# Progetto1FAS

Il progetto proposto consiste in un'analisi dati applicata a un dataset di tipologia linguistica.
Il dataset utilizzato è il [WALS](https://wals.info/), una dei più grandi dataset di tipologia linguistica,
che raccoglie informazioni riguardanti le proprietà strutturali di un ampio campione di lingue mondiali.

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
Tale approccio permette di condensare nel progetto gli argomenti trattati a lezione nonostante
alcune implementazioni possano risultare artificialmente elaborate.

## Dipendenze del progetto

Per avviare il progetto è necessaria l'installazione di Git e Docker.

## Avvio

- Clonazione della repository:

```bash
git clone https://github.com/FedeBrus/Progetto1FAS
```

- Build dell'immagine di progetto:

```bash
docker build -t wals-analysis .
```

- Esecuzione del container:

```bash
docker run -p 8888:8888 wals-analysis
```

Una volta avviato, il container eseguirà JupyterLab e genererà un token di autenticazione;
sarà sufficiente copiare il link prodotto all'interno di un browser per accedere ai notebook.

### Sviluppo

Il progetto è stato sviluppato con l'utilizzo di Git e VSCode. Durante le fasi di implementazione si è fatto ricorso a risorse online,
tra cui documentazione ufficiale, forum (nello specifico StackOverflow) e LLM (in particolare Gemini).
Ogni risposta trovata su forum o generata da LLM è stato oggetto di verifica e comparazione con la documentazione ufficiale.
Strumenti basati su LLM sono stati utilizzati principalmente per esplorare le funzionalità delle librerie di python precedentemente non note, facilitandone l'apprendimento.

Per il progetto è stata creata una repository Github a questo [link](https://github.com/FedeBrus/Progetto1FAS).
La git history, sebbene contenga qualche branch, è molto lineare, dato che questo progetto non ha visto
la collaborazione di più membri.

### Script Bash

Sono stati creati tre script Bash responsabili delle operazioni di recupero del dataset da GitHub (fetch.sh),
al pruning dei dati non utilizzati dall'analisi (prune.sh) e, infine, alla denormalizzazione del dataset (join.sh)
per consentire di lavorare su un file unico.
Si è preferito l'utilizzo di xan rispetto al tool csvkit visto a lezione per mera preferenza,
pur essendo intercambiabili in questo contesto.

### Dockerfile

Si è optato per l'impiego di Docker al fine di garantire la piena riproducibilità dell'ambiente di runtime e consentire l'avvio del progetto
tramite un singolo comando.
È stato creato un Dockerfile per la generazione di un'immagine personalizzata basata su Ubuntu 24.04;
tale distribuzione è stata scelta per semplificare la gestione delle dipendenze, nonostante l'alternativa Alpine avrebbe garantito una maggiore leggerezza.
Una delle auto-criticità più grandi è infatti la dimensione spropositata dell'immagine Docker, causata appunto dall'immagine di partenze Ubuntu e
dal volume dei moduli python installati.
La versione della distribuzione è stata fissata per prevenire eventuali problemi di compatibilità future.
Il Dockerfile si occupa dell'installazione e dell'esecuzione di Ansible per la gestione delle dipendenze,
i permessi di esecuzione degli script shell e la loro invocazione.
All'avvio del container, viene inizializzato il servizio JupyterLab.

### Ansible

Ansible si occupa dell'installazione delle dipendenze del progetto. Il file hosts definisce il target sul localhost del container ed è più una formalità che altro.
E' presente un solo ruolo composto dai seguenti task:

  - Installazione dei pacchetti di sistema.
  - Installazione di xan (strumento non presente nei principali package manager, incluso APT).
  - Installazione in un ambienete virtuale dei moduli Python necessari, definiti nel file requirements.txt.

### File Python

I sorgenti Python sono organizzati in un modulo, che viene importato dai notebook.
Questi espongono diverse funzioni di utility per il caricamento del dataset e la generazione grafici.

### Jupyter

L'attività di analisi è distribuita in cinque notebook:

  - Part0: esposizione della struttura del dataset.
  - Part1: elaborazioni statistiche sulle lingue, categorizzate per regioni geografiche e rapporti genealogiche.
  - Part2: analisi dei valori assunti da determinati parametri in relazione alle regioni geografiche e alle diramazioni genealogiche.
  - Part3: visualizzazione della distribuzione geografica delle lingue e dei relativi valori parametrici.
  - Part4: analisi della distribuzione incrociata tra i valori dei parametri.
