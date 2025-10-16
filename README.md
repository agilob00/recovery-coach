# 🧠 RecoveryCoach

**RecoveryCoach** es una aplicación que recomienda **rutinas de recuperación personalizadas** según el tipo de entrenamiento del usuario (running, fútbol, gym, etc.) y su contexto.  
El sistema utiliza un **grafo de conocimiento deportivo-médico (Neo4j)** para modelar relaciones entre *entrenamientos, músculos y rutinas de recuperación*, y un **backend FastAPI** que ofrece recomendaciones dinámicas a través de una API REST.

Además, el proyecto está diseñado para incorporar un **módulo RAG (LlamaIndex + Ollama)** que permitirá explicar y justificar las recomendaciones basándose en evidencia científica.

---

## 🚀 Objetivos del proyecto

- Mostrar cómo usar **Neo4j** para modelar conocimiento deportivo y médico.
- Integrar **FastAPI** para construir una API escalable y documentada.
- Incluir **RAG (LlamaIndex + Ollama)** para soporte conversacional con evidencia.
- Desplegar la aplicación con **Docker Compose** (Neo4j + Backend).
- Incorporar **gamificación** y adaptaciones según tiempo o nivel del usuario.

---

## ⚙️ Funcionalidades principales

✅ Ingreso del tipo de entrenamiento (Running, Football, Gym, etc.)  
✅ Recomendación automática de rutinas según músculos implicados  
✅ Adaptación según tiempo disponible del usuario  
✅ Visualización del grafo de conocimiento en Neo4j  
✅ API REST documentada con Swagger (`/docs`)  
🔜 Próximamente: Chatbot / Coach con evidencia médica y gamificación

---

## 🧩 Arquitectura general

```plaintext
📦 recovery-coach/
├── backend/
│   ├── main.py              # API FastAPI con conexión a Neo4j
│   ├── load_data.py         # Script para importar CSV al grafo
│   ├── requirements.txt     # Dependencias de backend
│
├── datasets/
│   ├── exercises_merged.csv # Dataset de ejercicios + músculos + rutinas
│
├── neo4j/
│   ├── init.cypher          # Script inicial para poblar el grafo
│
├── docker-compose.yml       # Infraestructura (Neo4j + FastAPI)
└── README.md
