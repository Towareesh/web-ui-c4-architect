ENTITY_TYPES = ["SYSTEM", "CONTAINER", "COMPONENT", "ACTOR", "EXTERNAL_SYSTEM", "DATABASE", "QUEUE", "VERB"]
RELATION_TYPES = ["uses", "contains", "stores_in", "produces", "retrieves_from", 
                 "triggers", "monitors", "delivers_to", "depends_on", "communicates_with", "interacts_with"]

C4_LEVELS = {
    "SYSTEM": 1,
    "CONTAINER": 2,
    "COMPONENT": 3,
    "DATABASE": 2,
    "QUEUE": 2,
    "EXTERNAL_SYSTEM": 1,
    "ACTOR": 1,
    "VERB": 4
}