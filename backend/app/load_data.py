from neo4j import GraphDatabase
import csv
import os

# Config
URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASS = os.getenv("NEO4J_PASS", "recovery123")
CSV_PATH = "/app/datasets/exercises_merged.csv"

driver = GraphDatabase.driver(URI, auth=(USER, PASS))

# --- Función de normalización ---
def norm(s):
    if not s:
        return ""
    return s.strip().title()

# --- Crear constraints ---
def create_constraints(session):
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (e:Exercise) REQUIRE e.name IS UNIQUE;")
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:Muscle) REQUIRE m.name IS UNIQUE;")
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (r:Routine) REQUIRE r.name IS UNIQUE;")
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:TrainingType) REQUIRE t.name IS UNIQUE;")

# --- Cargar ejercicios y músculos ---
def load_exercises(session, csv_path):
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        total, skipped = 0, 0
        for row in reader:
            exercise_name = norm(row.get("exercise_name"))
            primary_muscle = norm(row.get("primary_muscle"))
            secondary_muscle = norm(row.get("secondary_muscle"))
            body_part = norm(row.get("body_part"))
            exercise_type = norm(row.get("type"))  # NO usar palabra reservada
            equipment = norm(row.get("equipment"))
            difficulty = norm(row.get("difficulty"))

            if not exercise_name or not primary_muscle:
                skipped += 1
                continue

            session.run(
                """
                MERGE (e:Exercise {name: $exercise_name})
                ON CREATE SET 
                    e.body_part = $body_part,
                    e.type = $exercise_type,
                    e.equipment = $equipment,
                    e.difficulty = $difficulty
                ON MATCH SET 
                    e.body_part = coalesce(e.body_part, $body_part),
                    e.type = coalesce(e.type, $exercise_type),
                    e.equipment = coalesce(e.equipment, $equipment),
                    e.difficulty = coalesce(e.difficulty, $difficulty)
                MERGE (m:Muscle {name: $primary_muscle})
                MERGE (e)-[:TARGETS]->(m)
                """,
                exercise_name=exercise_name,
                body_part=body_part,
                exercise_type=exercise_type,  # <-- ahora se pasa correctamente
                equipment=equipment,
                difficulty=difficulty,
                primary_muscle=primary_muscle,
            )

            if secondary_muscle:
                session.run(
                    """
                    MERGE (sm:Muscle {name: $secondary_muscle})
                    WITH sm
                    MATCH (e:Exercise {name: $exercise_name})
                    MERGE (e)-[:TARGETS]->(sm)
                    """,
                    secondary_muscle=secondary_muscle,
                    exercise_name=exercise_name,
                )

            total += 1

        print(f"✔ Ejercicios procesados: {total}, saltados: {skipped}")

# --- Crear rutinas ---
def create_routines_for_muscles(session):
    templates = {
        "Quadriceps": ["Quad Stretch", "Foam Roller Quads"],
        "Hamstrings": ["Hamstring Stretch", "Foam Roller Hamstrings"],
        "Calves": ["Calf Stretch", "Foam Roller Calves"],
        "Glutes": ["Figure-4 Stretch", "Foam Roller Glutes"],
        "Core": ["Child's Pose", "Deep Core Reset"],
    }
    total = 0
    for muscle, routines in templates.items():
        for r in routines:
            session.run(
                """
                MERGE (m:Muscle {name: $muscle})
                MERGE (r:Routine {name: $rname})
                SET r.duration = 8, r.type = 'stretch', r.level = 'easy'
                MERGE (m)-[:SUGGESTS]->(r)
                """,
                muscle=muscle,
                rname=r,
            )
            total += 1
    print(f"✔ Rutinas creadas/vinculadas: {total}")

# --- Crear tipos de entrenamiento ---
def create_training_types(session):
    training_types = {
        "Running": ["Quadriceps", "Hamstrings", "Calves", "Core"],
        "Football": ["Quadriceps", "Hamstrings", "Calves", "Glutes"],
        "Gym": ["Chest", "Back", "Biceps", "Triceps", "Shoulders"],
    }
    total = 0
    for tt, muscles in training_types.items():
        session.run("MERGE (t:TrainingType {name: $name})", name=tt)
        for m in muscles:
            session.run(
                """
                MATCH (t:TrainingType {name: $tt})
                MERGE (mu:Muscle {name: $m})
                MERGE (t)-[:FOCUSES_ON]->(mu)
                """,
                tt=tt,
                m=m,
            )
            total += 1
    print(f"✔ TrainingTypes creados y vinculados: {total}")

# --- Main ---
def main():
    with driver.session() as session:
        create_constraints(session)
        load_exercises(session, CSV_PATH)
        create_routines_for_muscles(session)
        create_training_types(session)
    print("✅ Carga completa: ejercicios, músculos, rutinas y tipos de entrenamiento.")

if __name__ == "__main__":
    main()
