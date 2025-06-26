from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from transformers import AutoModelForSequenceClassification
import torch
import re
import os
import json
import uuid
import traceback

app = Flask(__name__)
CORS(app)

# Загрузка NER модели
ner_model_path = "ner_model-20250625T131736Z-1-001/ner_model"
ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_path)
ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_path)

# Загрузка RE модели
re_model_path = "re_model_v2-20250625T151402Z-1-001/re_model_v2"
re_tokenizer = AutoTokenizer.from_pretrained(re_model_path)
re_model = AutoModelForSequenceClassification.from_pretrained(re_model_path)

# Списки сущностей и отношений
ENTITY_TYPES = ["SYSTEM", "CONTAINER", "COMPONENT", "ACTOR", "EXTERNAL_SYSTEM", "DATABASE", "QUEUE", "VERB"]
RELATION_TYPES = ["uses", "contains", "stores_in", "produces", "retrieves_from", 
                 "triggers", "monitors", "delivers_to", "depends_on", "communicates_with", "interacts_with"]

# Иерархия C4
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

# Создаем пайплайны
ner_pipeline = pipeline(
    "token-classification", 
    model=ner_model, 
    tokenizer=ner_tokenizer,
    aggregation_strategy="simple"
)

def predict_entities(text):
    """Предсказание сущностей с помощью NER модели"""
    results = ner_pipeline(text)
    
    entities = []
    for entity in results:
        # Фильтрация и нормализация сущностей
        if entity['entity_group'] in ENTITY_TYPES and entity['word'].strip():
            # Объединение разделенных токенов
            if entities and entities[-1]['end'] == entity['start'] and entities[-1]['type'] == entity['entity_group']:
                entities[-1]['text'] += " " + entity['word'].strip()
                entities[-1]['end'] = entity['end']
            else:
                entity_id = f"ent-{len(entities)}"
                entity_level = C4_LEVELS.get(entity['entity_group'], 1)
                entities.append({
                    "text": entity['word'].strip(),
                    "type": entity['entity_group'],
                    "start": entity['start'],
                    "end": entity['end'],
                    "id": entity_id,
                    "level": entity_level
                })
    
    return entities

def predict_relations(entities, text):
    """Предсказание отношений с помощью RE модели"""
    relations = []
    
    if len(entities) < 2:
        return relations
    
    # Создаем все возможные пары сущностей
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            head = entities[i]
            tail = entities[j]
            
            # Только если сущности на одном уровне или соседних уровнях
            if abs(head['level'] - tail['level']) > 1:
                continue
                
            # Создаем контекст для классификации отношений
            context = f"{head['text']} {tail['text']} in: {text}"
            inputs = re_tokenizer(
                context, 
                return_tensors="pt", 
                padding=True,
                truncation=True, 
                max_length=128
            )
            
            # Предсказание
            outputs = re_model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            confidence, predicted_class = torch.max(probabilities, dim=1)
            
            # Принимаем только предсказания с достаточной уверенностью
            if confidence.item() > 0.7 and predicted_class.item() < len(RELATION_TYPES):
                relation_type = RELATION_TYPES[predicted_class.item()]
                relations.append({
                    "source": head['id'],
                    "target": tail['id'],
                    "type": relation_type,
                    "confidence": confidence.item(),
                    "level": min(head['level'], tail['level'])
                })
    
    return relations

def build_c4_hierarchy(entities, relations):
    """Построение иерархии C4 из сущностей и отношений"""
    # Группируем сущности по уровням
    levels = {1: [], 2: [], 3: [], 4: []}
    for entity in entities:
        if entity['level'] in levels:
            levels[entity['level']].append(entity)
    
    # Строим связи между уровнями
    hierarchy = {
        "systems": [],
        "containers": [],
        "components": [],
        "code_elements": []
    }
    
    # Уровень 1: Системы и акторы
    for entity in levels[1]:
        if entity['type'] == 'SYSTEM':
            system = {
                "id": entity['id'],
                "name": entity['text'],
                "description": "",
                "containers": []
            }
            hierarchy["systems"].append(system)
        elif entity['type'] == 'ACTOR':
            hierarchy["systems"].append({
                "id": entity['id'],
                "name": entity['text'],
                "type": "actor",
                "description": ""
            })
        elif entity['type'] == 'EXTERNAL_SYSTEM':
            hierarchy["systems"].append({
                "id": entity['id'],
                "name": entity['text'],
                "type": "external",
                "description": ""
            })
    
    # Уровень 2: Контейнеры и БД
    for entity in levels[2]:
        container = {
            "id": entity['id'],
            "name": entity['text'],
            "type": entity['type'].lower(),
            "components": []
        }
        
        # Находим родительскую систему
        for rel in relations:
            if rel['source'] == entity['id'] and rel['level'] == 1:
                for system in hierarchy["systems"]:
                    if system["id"] == rel['target']:
                        if "containers" not in system:
                            system["containers"] = []
                        system["containers"].append(container)
                        break
            elif rel['target'] == entity['id'] and rel['level'] == 1:
                for system in hierarchy["systems"]:
                    if system["id"] == rel['source']:
                        if "containers" not in system:
                            system["containers"] = []
                        system["containers"].append(container)
                        break
        
        hierarchy["containers"].append(container)
    
    # Уровень 3: Компоненты
    for entity in levels[3]:
        component = {
            "id": entity['id'],
            "name": entity['text'],
            "code_elements": []
        }
        
        # Находим родительский контейнер
        for rel in relations:
            if rel['source'] == entity['id'] and rel['level'] == 2:
                for container in hierarchy["containers"]:
                    if container["id"] == rel['target']:
                        if "components" not in container:
                            container["components"] = []
                        container["components"].append(component)
                        break
            elif rel['target'] == entity['id'] and rel['level'] == 2:
                for container in hierarchy["containers"]:
                    if container["id"] == rel['source']:
                        if "components" not in container:
                            container["components"] = []
                        container["components"].append(component)
                        break
        
        hierarchy["components"].append(component)
    
    # Уровень 4: Элементы кода (классы, функции)
    for entity in levels[4]:
        code_element = {
            "id": entity['id'],
            "name": entity['text'],
            "type": "function" if "function" in entity['text'].lower() else "class"
        }
        
        # Находим родительский компонент
        for rel in relations:
            if rel['source'] == entity['id'] and rel['level'] == 3:
                for component in hierarchy["components"]:
                    if component["id"] == rel['target']:
                        if "code_elements" not in component:
                            component["code_elements"] = []
                        component["code_elements"].append(code_element)
                        break
            elif rel['target'] == entity['id'] and rel['level'] == 3:
                for component in hierarchy["components"]:
                    if component["id"] == rel['source']:
                        if "code_elements" not in component:
                            component["code_elements"] = []
                        component["code_elements"].append(code_element)
                        break
        
        hierarchy["code_elements"].append(code_element)
    
    return hierarchy

def generate_c4_code(hierarchy, current_level=1):
    """Рекурсивная генерация кода PlantUML для C4 уровней"""
    code = ""
    
    if current_level == 1:
        code += "@startuml\n"
        code += "!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml\n"
        code += "!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml\n"
        code += "!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml\n\n"
        
        # Системы и акторы
        for system in hierarchy["systems"]:
            if system.get("type") == "actor":
                code += f'Person({system["id"]}, "{system["name"]}", "")\n'
            elif system.get("type") == "external":
                code += f'System_Ext({system["id"]}, "{system["name"]}", "")\n'
            else:
                code += f'System({system["id"]}, "{system["name"]}", "")\n'
        
        code += "\n"
    
    # Контейнеры (уровень 2)
    if current_level == 2:
        for system in hierarchy["systems"]:
            if "containers" in system and system["containers"]:
                code += f'System_Boundary({system["id"]}_boundary, "{system["name"]} Boundary") {{\n'
                
                for container in system["containers"]:
                    if container["type"] == "database":
                        code += f'  ContainerDb({container["id"]}, "{container["name"]}", "")\n'
                    elif container["type"] == "queue":
                        code += f'  Queue({container["id"]}, "{container["name"]}", "")\n'
                    else:
                        code += f'  Container({container["id"]}, "{container["name"]}", "")\n'
                
                code += "}\n\n"
    
    # Компоненты (уровень 3)
    if current_level == 3:
        for container in hierarchy["containers"]:
            if "components" in container and container["components"]:
                code += f'Container_Boundary({container["id"]}_boundary, "{container["name"]} Components") {{\n'
                
                for component in container["components"]:
                    code += f'  Component({component["id"]}, "{component["name"]}", "")\n'
                
                code += "}\n\n"
    
    # Элементы кода (уровень 4)
    if current_level == 4:
        for component in hierarchy["components"]:
            if "code_elements" in component and component["code_elements"]:
                code += f'Component_Boundary({component["id"]}_boundary, "{component["name"]} Code") {{\n'
                
                for code_elem in component["code_elements"]:
                    code += f'  Component({code_elem["id"]}, "{code_elem["name"]}", "{code_elem["type"]}")\n'
                
                code += "}\n\n"
    
    # Генерируем связи
    if current_level == 1:
        # Только для верхнего уровня
        code += "\n' Relations\n"
        for system in hierarchy["systems"]:
            if "containers" in system:
                for container in system["containers"]:
                    code += f'Rel({system["id"]}, {container["id"]}, "Uses")\n'
        
        for container in hierarchy["containers"]:
            if "components" in container:
                for component in container["components"]:
                    code += f'Rel({container["id"]}, {component["id"]}, "Uses")\n'
        
        for component in hierarchy["components"]:
            if "code_elements" in component:
                for code_elem in component["code_elements"]:
                    code += f'Rel({component["id"]}, {code_elem["id"]}, "Uses")\n'
    
    # Рекурсивно генерируем следующий уровень
    if current_level < 4:
        next_level_code = generate_c4_code(hierarchy, current_level + 1)
        code += next_level_code
    
    if current_level == 1:
        code += "@enduml"
    
    return code

def convert_to_diagram_elements(hierarchy):
    """Преобразование иерархии в элементы диаграммы для ReactFlow"""
    nodes = []
    edges = []
    
    # Системы (уровень 1)
    for i, system in enumerate(hierarchy["systems"]):
        nodes.append({
            "id": system["id"],
            "type": "c4",
            "position": {"x": 100 + i * 300, "y": 100},
            "data": {
                "label": system["name"],
                "entityType": system.get("type", "SYSTEM").upper(),
                "level": 1
            }
        })
    
    # Контейнеры (уровень 2)
    container_idx = 0
    for system in hierarchy["systems"]:
        if "containers" in system:
            for i, container in enumerate(system["containers"]):
                nodes.append({
                    "id": container["id"],
                    "type": "c4",
                    "position": {"x": 200 + container_idx * 200, "y": 200},
                    "data": {
                        "label": container["name"],
                        "entityType": container["type"].upper(),
                        "level": 2,
                        "parent": system["id"]
                    }
                })
                edges.append({
                    "id": f"edge-{system['id']}-{container['id']}",
                    "source": system["id"],
                    "target": container["id"],
                    "label": "Contains",
                    "level": 1
                })
                container_idx += 1
    
    # Компоненты (уровень 3)
    component_idx = 0
    for container in hierarchy["containers"]:
        if "components" in container:
            for i, component in enumerate(container["components"]):
                nodes.append({
                    "id": component["id"],
                    "type": "c4",
                    "position": {"x": 300 + component_idx * 150, "y": 300},
                    "data": {
                        "label": component["name"],
                        "entityType": "COMPONENT",
                        "level": 3,
                        "parent": container["id"]
                    }
                })
                edges.append({
                    "id": f"edge-{container['id']}-{component['id']}",
                    "source": container["id"],
                    "target": component["id"],
                    "label": "Contains",
                    "level": 2
                })
                component_idx += 1
    
    # Элементы кода (уровень 4)
    code_idx = 0
    for component in hierarchy["components"]:
        if "code_elements" in component:
            for i, code_elem in enumerate(component["code_elements"]):
                nodes.append({
                    "id": code_elem["id"],
                    "type": "c4",
                    "position": {"x": 400 + code_idx * 120, "y": 400},
                    "data": {
                        "label": code_elem["name"],
                        "entityType": "CODE",
                        "level": 4,
                        "parent": component["id"]
                    }
                })
                edges.append({
                    "id": f"edge-{component['id']}-{code_elem['id']}",
                    "source": component["id"],
                    "target": code_elem["id"],
                    "label": "Implements",
                    "level": 3
                })
                code_idx += 1
    
    return nodes, edges

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    text = data.get('text', '')
    
    try:
        # Предсказываем сущности
        entities = predict_entities(text)
        print("Predicted entities:", json.dumps(entities, indent=2, ensure_ascii=False))
        
        # Предсказываем отношения
        relations = predict_relations(entities, text)
        print("Predicted relations:", json.dumps(relations, indent=2, ensure_ascii=False))
        
        # Строим иерархию C4
        hierarchy = build_c4_hierarchy(entities, relations)
        print("C4 Hierarchy:", json.dumps(hierarchy, indent=2, ensure_ascii=False))
        
        # Генерируем PlantUML код
        plantuml_code = generate_c4_code(hierarchy)
        print("Generated PlantUML code:\n", plantuml_code)
        
        # Преобразуем в элементы диаграммы
        nodes, edges = convert_to_diagram_elements(hierarchy)
        
        return jsonify({
            "success": True,
            "hierarchy": hierarchy,
            "plantuml_code": plantuml_code,
            "nodes": nodes,
            "edges": edges
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        })

@app.route('/update-diagram', methods=['POST'])
def update_diagram():
    data = request.json
    hierarchy = data.get('hierarchy', {})
    
    try:
        # Регенерация PlantUML кода
        plantuml_code = generate_c4_code(hierarchy)
        
        # Преобразование в элементы диаграммы
        nodes, edges = convert_to_diagram_elements(hierarchy)
        
        return jsonify({
            "success": True,
            "plantuml_code": plantuml_code,
            "nodes": nodes,
            "edges": edges
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/parse-plantuml', methods=['POST'])
def parse_plantuml():
    data = request.json
    code = data.get('code', '')
    
    # В реальной реализации здесь будет парсинг PlantUML
    # Для демонстрации вернем фиктивные данные
    return jsonify({
        "nodes": [
            {"id": "sys1", "type": "c4", "data": {"label": "System 1", "entityType": "SYSTEM"}},
            {"id": "db1", "type": "c4", "data": {"label": "Database", "entityType": "DATABASE"}}
        ],
        "edges": [
            {"id": "edge1", "source": "sys1", "target": "db1", "label": "uses"}
        ]
    })

@app.route('/ai-assistant', methods=['POST'])
def ai_assistant():
    data = request.json
    action = data.get('action', '')
    current_diagram = data.get('currentDiagram', {})
    current_code = data.get('currentCode', '')
    
    print(f"AI Assistant request: {action}")
    
    # Здесь будет реальная интеграция с ИИ
    # Пока вернем фиктивный ответ
    
    response_text = f"I've processed your request: '{action}'. The diagram has been updated accordingly."
    
    # Для демонстрации создадим фиктивные изменения
    new_nodes = current_diagram.get('nodes', [])
    new_edges = current_diagram.get('edges', [])
    
    if "add" in action.lower():
        new_node_id = f"node-{len(new_nodes)}"
        new_nodes.append({
            "id": new_node_id,
            "position": {"x": 500, "y": 300},
            "data": {
                "label": "New Component",
                "entityType": "COMPONENT"
            },
            "type": "custom"
        })
        
        if new_nodes:
            new_edges.append({
                "id": f"edge-{len(new_edges)}",
                "source": new_nodes[0]['id'],
                "target": new_node_id,
                "label": "uses",
                "animated": True
            })
    
    # Обновляем код (в реальном приложении нужно генерировать)
    new_code = current_code + f"\n// AI Action: {action}"
    
    return jsonify({
        "response": response_text,
        "nodes": new_nodes,
        "edges": new_edges,
        "code": new_code
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)