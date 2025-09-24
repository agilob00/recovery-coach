// Constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (e:Exercise) REQUIRE e.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Muscle) REQUIRE m.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (r:Routine) REQUIRE r.name IS UNIQUE;

// Example nodes
CREATE (ex1:Exercise {name:'Running', type:'cardio'});
CREATE (ex2:Exercise {name:'Gym', type:'strength'});

CREATE (m1:Muscle {name:'Quadriceps'});
CREATE (m2:Muscle {name:'Hamstrings'});

CREATE (r1:Routine {name:'Quad Stretch', duration:8, type:'stretch', level:'easy'});
CREATE (r2:Routine {name:'Foam Roller Quads', duration:10, type:'foamroller', level:'easy'});

// Relationships
CREATE (ex1)-[:TARGETS]->(m1);
CREATE (ex1)-[:TARGETS]->(m2);
CREATE (m1)-[:SUGGESTS]->(r1);
CREATE (m1)-[:SUGGESTS]->(r2);
