# E-Commerce & Order Management Web API

Una moderna Web API RESTful completamente **asincrona** progettata per la gestione ad alte prestazioni di piattaforme di e-commerce e sistemi d'ordine. L'applicazione sfrutta **FastAPI**, **SQLAlchemy ORM** con supporto nativo asincrono e **Pydantic v2**.

---

## 🚀 Key Features

*   **Architettura Asincrona:** Sfrutta l'I/O non bloccante per gestire un elevato volume di richieste concorrenti e ottimizzare la comunicazione con il database.
*   **Sicurezza e Autenticazione JWT:** Gestione asincrona di autenticazione e autorizzazione tramite JSON Web Tokens.
*   **Gestione Atomica dello Stock:** Controllo in tempo reale della disponibilità in magazzino all'interno di transazioni protette.
*   **Separazione dei Payload (DTO Pattern):** Validazione rigorosa tramite Pydantic v2 per isolare i modelli di input/output.
*   **Documentazione Interattiva:** Supporto nativo integrato per Swagger UI e ReDoc.

---

## 🛠 Architettura del Progetto e Stack Tecnologico

L'applicazione adotta una struttura modulare suddivisa nei seguenti componenti asincroni: strato API/Controller, logica di business, persistenza ORM, validazione dei dati e gestione delle connessioni al database.
