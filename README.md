# Lab 09

#### Argomenti

- Utilizzo Pattern MVC e DAO
- Utilizzo dell'Object Relational Mapping (ORM)
- Algoritmi di Ricorsione

---
> **❗ ATTENZIONE:** 
>  Ricordare di effettuare il **fork** del repository principale, quindi clonare su PyCharm il **repository personale** 
> (https://github.com/my-github-username/Lab09) e non quello principale.
> 
> In caso di dubbi consultare la guida caricata nel lab02: 
> https://github.com/Programmazione-Avanzata-2025-26/Lab02/blob/main/Guida.pdf

---

##  Analisi Ottimale dei Pacchetti Turistici
Una **compagnia di viaggi italiana** vuole usare i dati storici di tour già svolti per proporre pacchetti turistici 
ottimali ai nuovi clienti. Per ogni tour sono note la regione, la durata in giorni, le attrazioni incluse e il valore 
culturale di ciascuna attrazione (da 1 a 10). 

Realizzare un programma che consenta all’utente di scegliere una regione italiana, di indicare la durata desiderata 
del pacchetto turistico (in giorni, `G`) e un budget massimo (`B`). A partire dai tour storicamente realizzati nella 
regione selezionata, il programma dovrà generare un pacchetto turistico che consista in una combinazione di tour che 
massimizzi il valore culturale complessivo delle attrazioni presenti nei tour selezionati e che rispetti i 
seguenti vincoli: 
- I tour inclusi nel pacchetto devono essere **tutti diversi tra loro**.
- Non devono esserci **attrazioni duplicate** all’interno del pacchetto. 
- La durata complessiva del pacchetto non deve superare il **numero massimo di giorni** indicato (`G`). 
- Il costo totale del pacchetto non deve eccedere il **budget massimo** previsto (`B`). 

Il programma utilizza il database fornito, denominato `archivio_tour.sql`, che contiene due tabelle principali: 
- `regione`: contiene le informazioni delle 20 regioni italiane:
  - id
  - nome 

- `attrazione`: contiene le informazioni inerenti alle attrazioni:
  - id 
  - nome
  - valore_culturale

- `tour`: contiene le informazioni inerenti a ciascun tour:
  - id 
  - id_regione
  - nome
  - durata_giorni
  - costo

- `tour_attrazione`: la tabella che gestisce la relazione **molti-a-molti (N:N)** tra tour e attrazioni. 
Permette di trovare tutte le attrazioni incluse in un tour e tutti i tour a cui ciascuna attrazione appartiene:
  - id_tour 
  - id_regione

![relazione_db.png](img/relazione_db.png)

L’applicazione, sviluppata in Python, deve permettere di 
- Gestire **la relazione N:N** tra attrazioni e tour tramite l'**ORM** e opportune strutture dati in Python.
- Calcolare la sequenza di tour che massimizzi il valore culturale complessivo delle attrazioni presenti nei tour 
selezionati (e che rispetti i vari vincoli indicati) attraverso un **algoritmo di ottimizzazione ricorsiva**. 


##  Funzionalità Richieste
Nel progetto di base, l'interfaccia grafica (file `view.py` e `controller.py`) è già implementata con il seguente layout:
![layout.png](img/layout.png)

### **Problema di Ottimizzazione (algoritmo ricorsivo + ORM)**
A partire dal layout proposto, l’applicazione deve permettere all’utente di: 
- Selezionare una regione (un codice alfanumerico univoco, l’id della regione), tramite un Dropdown; 
- Inserire un budget massimo tramite un TextField;
- Inserire la durata massima desiderata in giorni tramite un TextField;
- Premendo un pulsante (“Genera Pacchetto”) visualizzare tramite una ListView la lista di tour che massimizzano 
il valore culturale.

>💡 **Esempio**: L’utente seleziona la regione “Abruzzo”, indica un numero di giorni pari a 5 e un costo massimo pari 
> a €500 → il programma mostra la lista di tour che massimizzano il valore culturale, rispettando i vincoli indicati. 
![esempio.png](img/esempio.png)

È inoltre importante considerare alcune condizioni particolari per il corretto funzionamento dell’applicazione:
- Se l’utente non specifica un budget massimo, il sistema interpreta la richiesta come la volontà di generare un 
pacchetto senza alcun limite di costo. 
- Se l’utente non indica un numero massimo di giorni, il sistema considera la ricerca libera da vincoli di durata.

##  Nota Bene
Per pensare come impostare la **ricorsione**, è consigliato utilizzare lo schema seguente. 
Può esser utile ragionare su carta per capire come impostare l’algoritmo.

```code
def recursion(..., level):
    # 🟤 A - Istruzioni che dovrebbero essere sempre eseguite
    do_always(...)
    
    # 🟢 B - Potrebbe non essere necessaria per questo problema
    if terminal_condition:
        do_something(...)
    
    for ...: # un loop, se necessario     
    
        # 🟡 C - Considerare dei vincoli prima di procedere con la ricorsione
        if filter: 
        
            # 🔵 D
            compute_partial()
            
            # 🔴 E
            recursion(..., level + 1)
        
            # 🟣 F
            back_tracking()
```

**💡 Suggerimenti Pratici**
- Quando è necessario copiare liste di oggetti per evitare di modificare l’originale durante la ricorsione, 
è meglio usare il metodo `.copy()` (vedi anche [`.deepcopy()`](https://docs.python.org/3/library/copy.html)) che crea una copia superficiale della lista: la nuova lista contiene gli stessi 
oggetti della lista originale, ma modificando la lista copiata non si altera la lista originale.
    ```code
    lista_copia = lista_originale.copy()
    ```
- Per le strutture dati `set()`, ricordare che sono disponibili molti metodi utili, tra cui: `.add()`, `.update()`, 
`.intersection()`, `.difference()`, `.difference_update()`, ecc. (vedi
[Python Sets](https://www.w3schools.com/python/python_ref_set.asp)). Questi permettono di gestire in modo efficace 
insiemi di elementi senza duplicati. Inoltre, è importante ricordare che tutti gli elementi di un `set()` 
devono essere **hashable**, cioè immutabili e confrontabili.

## Materiale Fornito
Il repository del lab09 è organizzato con la struttura ad albero mostrata di seguito e contiene tutto il necessario per 
svolgere il laboratorio:

```code
Lab09/
├── database/
│   ├── __init__.py
|   ├── connector.cnf 
|   ├── DB_connect.py 
│   ├── regione_DAO.py (DA MODIFICARE) 
│   ├── attrazione_DAO.py (DA MODIFICARE) 
│   └── tour_DAO.py (DA MODIFICARE) 
│
├── model/
│   ├── __init__.py
│   ├── model.py (DA MODIFICARE) 
│   ├── attrazione.py 
│   ├── regione.py 
│   └── tour.py
│
├── UI/
│   ├── __init__.py
│   ├── alert.py
│   ├── controller.py
│   └── view.py
│
├── archivio_tour.sql (DA IMPORTARE)
└── main.py (DA ESEGUIRE)
 ```
