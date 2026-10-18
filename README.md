# E-Commerce & Order Management Web API

Una potente Web API RESTful pronta per la produzione per una piattaforma di e-commerce, sviluppata con **FastAPI**, **SQLAlchemy ORM** e **Pydantic v2**. 

Il progetto applica i sani principi di ingegneria del software come la **Separation of Concerns (SoC)** e il **Data Transfer Object (DTO) pattern**, gestendo transazioni di database complesse, autenticazione sicura e controllo degli accessi.

---

## 🚀 Key Features

*   **Autenticazione Sicura con JWT:** Sistema di login e registrazione basato su JSON Web Tokens (JWT) con hashing delle password in totale sicurezza.
*   **Pannello Admin e RBAC:** Controllo degli accessi basato sui ruoli (**Role-Based Access Control**). Protezione avanzata delle rotte tramite la Dependency Injection di FastAPI per consentire le operazioni di gestione catalogo, utenti e ordini solo ad utenti con privilegi Admin.
*   **Gestione Atomica dello Stock (Warehouse Logic):** Verifica automatica della disponibilità degli articoli nel magazzino durante il checkout. Riduzione delle quantità in tempo reale con gestione delle transazioni (commit/rollback) per garantire la coerenza dei dati ed evitare l'overbooking.
*   **Separazione dei Payload (DTO Pattern):** Utilizzo rigoroso degli schemi di **Pydantic v2** per separare i dati di richiesta e risposta, nascondendo le colonne sensibili del database (come gli hash delle password).
*   **Architettura Documentata:** Integrazione nativa con **Swagger UI** (`/docs`) e **ReDoc** (`/redoc`) per il test e l'ispezione immediata degli endpoint in runtime.

---

## 🛠️ Architettura del Progetto

L'applicazione segue una struttura modulare e pulita per garantire scalabilità e manutenibilità del codice:

*   `main.py` (Controller/API Layer): Gestisce l'inizializzazione dell'app, la configurazione dei router, dei tag e la cattura delle eccezioni HTTP.
*   `App/crud.py` (Persistence Layer): Isola la business logic e le query dirette al database (inserimenti, update, logica di magazzino, estrazione utenti correnti).
*   `App/models.py` (Entity Layer): Mappa lo schema Object-Relational (ORM) tramite SQLAlchemy ereditando da una Base dichiarativa comune.
*   `App/schemas.py` (Validation Layer): Contiene i modelli Pydantic v2 per la validazione rigorosa dei tipi di dato in ingresso e in uscita.
*   `App/db.py` (Infrastructure Layer): Gestisce il ciclo di vita dell'engine del database e fornisce la sessione transazionale per ogni singola richiesta HTTP (`Depends(get_db)`).

---

## 💻 Tech Stack

*   **Framework:** FastAPI
*   **Data Validation:** Pydantic v2
*   **ORM Framework:** SQLAlchemy
*   **Database Migrations:** Alembic
*   **Database Engine:** SQLite / PostgreSQL Ready

---
