from flask import Blueprint, jsonify, request, current_app
from .auth import token_required
from .pipelines import NLPProcessor

main_bp = Blueprint('main', __name__)
nlp_processor = NLPProcessor()

@main_bp.route('/process', methods=['POST'])
@token_required
def process_text(current_user):
    data = request.json
    text = data.get('text', '')
    
    try:
        result = nlp_processor.full_processing(text)
        return jsonify({
            "success": True,
            **result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_bp.route('/update-diagram', methods=['POST'])
@token_required
def update_diagram(current_user):
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

@main_bp.route('/parse-plantuml', methods=['POST'])
@token_required
def parse_plantuml(current_user):
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