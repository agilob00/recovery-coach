import os
from fastapi import FastAPI
from pydantic import BaseModel
from neo4j import GraphDatabase

app = FastAPI(title="RecoveryCoach API")

# Configuración Neo4j desde variables de entorno
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "test")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

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
    with driver.session() as session:
        q = """
        MATCH (e:Exercise {name:$type})-[:TARGETS]->(m:Muscle)-[:SUGGESTS]->(r:Routine)
        WHERE r.duration <= $max_time
        RETURN r {.*} AS routine, collect(m.name) AS muscles
        LIMIT 6
        """
        res = session.run(q, {"type": payload.training_type, "max_time": payload.available_minutes})
        recs = []
        for row in res:
            recs.append({"routine": row["routine"], "muscles": row["muscles"]})
    return {"recommendations": recs}
