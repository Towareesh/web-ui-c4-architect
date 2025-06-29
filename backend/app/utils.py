from .constants import ENTITY_TYPES, RELATION_TYPES, C4_LEVELS

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