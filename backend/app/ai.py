import anthropic
import json
from flask import Blueprint, jsonify, request, current_app
from .auth import token_required

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ai-assistant', methods=['POST'])
@token_required
def ai_assistant(current_user):
    data = request.json
    action = data.get('action', '')
    current_diagram = data.get('currentDiagram', {})
    current_code = data.get('currentCode', '')
    
    # Формирование описания диаграммы
    diagram_description = generate_diagram_description(current_diagram)
    
    try:
        # Инициализация клиента Anthropic (новый стиль)
        client = anthropic.Anthropic(
            api_key=current_app.config['ANTHROPIC_API_KEY']
        )
        
        # Системный промпт
        system_prompt = """
        You are an AI assistant for software architecture design using C4 model. Your tasks:
        1. Understand user requests in context of current diagram
        2. Propose modifications to the architecture
        3. Output changes in strict JSON format:
        {
            "response": "Text response to user",
            "changes": {
                "add_nodes": [{"id": "...", "type": "...", ...}],
                "remove_node_ids": ["id1", "id2"],
                "add_edges": [{"id": "...", "source": "...", "target": "...", ...}],
                "remove_edge_ids": ["id1", "id2"]
            }
        }
        Current diagram state:
        """ + diagram_description

        # Запрос к Anthropic API
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"User request: {action}"}
            ]
        )
        
        # Парсинг ответа
        ai_response = json.loads(response.content[0].text)
        return apply_ai_changes(current_diagram, ai_response)
    
    except Exception as e:
        current_app.logger.error(f"AI processing error: {str(e)}")
        return jsonify({
            "error": "AI processing failed",
            "details": str(e)
        }), 500

def generate_diagram_description(diagram):
    """Генерация текстового описания диаграммы"""
    description = "Current diagram elements:\n"
    
    # Описание узлов
    for node in diagram.get('nodes', []):
        description += f"Node {node['id']}: {node['data']['label']} ({node['data']['entityType']})\n"
    
    # Описание связей
    for edge in diagram.get('edges', []):
        description += f"Edge {edge['id']}: {edge['source']} -> {edge['target']} ({edge.get('label', '')})\n"
    
    return description

def apply_ai_changes(current_diagram, ai_response):
    """Применение изменений от AI к диаграмме"""
    nodes = current_diagram.get('nodes', [])[:]
    edges = current_diagram.get('edges', [])[:]
    
    # Применение изменений
    changes = ai_response.get("changes", {})
    
    # Удаление узлов
    for node_id in changes.get("remove_node_ids", []):
        nodes = [n for n in nodes if n['id'] != node_id]
        edges = [e for e in edges if e['source'] != node_id and e['target'] != node_id]
    
    # Удаление связей
    for edge_id in changes.get("remove_edge_ids", []):
        edges = [e for e in edges if e['id'] != edge_id]
    
    # Добавление узлов
    for node in changes.get("add_nodes", []):
        # Генерация уникального ID если необходимо
        if 'id' not in node or not node['id']:
            node['id'] = f"node-{len(nodes)}"
        nodes.append(node)
    
    # Добавление связей
    for edge in changes.get("add_edges", []):
        # Генерация уникального ID если необходимо
        if 'id' not in edge or not edge['id']:
            edge['id'] = f"edge-{len(edges)}"
        edges.append(edge)
    
    return jsonify({
        "response": ai_response.get("response", "Changes applied"),
        "nodes": nodes,
        "edges": edges,
        "code": current_code
    })