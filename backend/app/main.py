import os
from fastapi import FastAPI
from pydantic import BaseModel
from neo4j import GraphDatabase

app = FastAPI(title="RecoveryCoach API")

# Configuración Neo4j desde variables de entorno
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://recovery-coach-neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "recovery123")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

# Modelo de entrada
class TrainingInput(BaseModel):
    training_type: str
    available_minutes: int
    intensity: str | None = None
    user_context: dict | None = None


@app.get("/")
def root():
    return {"message": "RecoveryCoach API is running 🚀"}


@app.post("/api/recommend")
def recommend(payload: TrainingInput):
    print("👉 Recibido:", payload.training_type, payload.available_minutes)
    with driver.session() as session:
        query = """
        MATCH (t:TrainingType)
        WHERE toLower(t.name) = toLower($training_type)
        MATCH (t)-[:FOCUSES_ON]->(m:Muscle)-[:SUGGESTS]->(r:Routine)
        WITH r, m, 
             CASE 
                WHEN r.duration IS NOT NULL THEN toFloat(r.duration) 
                ELSE 0 
             END AS dur
        WHERE dur <= toFloat($available_minutes)
        RETURN DISTINCT 
            r.name AS routine, 
            dur AS duration, 
            r.type AS type, 
            r.level AS level, 
            m.name AS muscle
        ORDER BY duration ASC
        LIMIT 10
        """
        result = session.run(
            query,
            training_type=payload.training_type.strip(),
            available_minutes=payload.available_minutes
        )
        recs = [record.data() for record in result]

    print("👉 Recomendaciones encontradas:", len(recs))
    return {
        "training_type": payload.training_type,
        "available_minutes": payload.available_minutes,
        "recommendations": recs
    }

