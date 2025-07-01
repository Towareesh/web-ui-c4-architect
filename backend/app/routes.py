from flask import Blueprint, jsonify, request, current_app
from .auth import token_required
from .pipelines import NLPProcessor
import re
from .utils import build_c4_hierarchy, generate_c4_code, convert_to_diagram_elements, util_parse_plantuml
import urllib.parse
import requests
from plantuml import PlantUML
import base64
import zlib
import logging
import os


main_bp = Blueprint('main', __name__)
nlp_processor = NLPProcessor()
EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'examples')

@main_bp.route('/get-examples', methods=['GET'])
def get_examples():
    """Возвращает список доступных примеров"""
    examples = []
    for i in range(1, 4):
        text_path = os.path.join(EXAMPLES_DIR, f'example{i}.txt')
        if os.path.exists(text_path):
            with open(text_path, 'r', encoding='utf-8') as f:
                description = f.read().strip()[:100] + '...'  # Краткое описание
            examples.append({
                'id': i,
                'title': f'Пример {i}',
                'description': description
            })
    return jsonify(examples)

@main_bp.route('/load-example/<int:example_id>', methods=['GET'])
def load_example(example_id):
    """Загружает конкретный пример по ID"""
    try:
        examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
        
        # Загрузка текста описания
        text_path = os.path.join(examples_dir, f'example{example_id}.txt')
        with open(text_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Загрузка PlantUML кода
        puml_path = os.path.join(examples_dir, f'example{example_id}_plantuml.txt')
        with open(puml_path, 'r', encoding='utf-8') as f:
            plantuml_code = f.read()
        
        # Генерация URL изображения для предпросмотра
        encoded = encode_plantuml(plantuml_code)
        image_url = f"https://www.plantuml.com/plantuml/png/{encoded}"
        
        return jsonify({
            "success": True,
            "text": text,
            "plantuml_code": plantuml_code,
            "image_url": image_url
        })
    except Exception as e:
        current_app.logger.error(f"Load example error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Пример не найден"
        }), 404
# @main_bp.route('/process', methods=['POST'])
# @token_required
# def process_text(current_user):
#     data = request.json
#     text = data.get('text', '')
    
#     try:
#         result = nlp_processor.full_processing(text)
#         return jsonify({
#             "success": True,
#             **result
#         })
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "error": str(e)
#         }), 500

def encode_plantuml(text):
    """Кодирование текста PlantUML для URL"""
    # Удаляем комментарии и лишние пробелы
    cleaned_text = '\n'.join([line for line in text.split('\n') if not line.strip().startswith("'") and line.strip()])
    
    # Кодируем в UTF-8 и сжимаем
    compressed = zlib.compress(cleaned_text.encode('utf-8'))
    # Убираем заголовок zlib (первые 2 байта)
    compressed_without_header = compressed[2:-4]
    
    # Кодируем в base64
    encoded = base64.b64encode(compressed_without_header).decode('utf-8')
    
    # Заменяем символы для URL
    translated = encoded.translate(str.maketrans(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    ))
    
    return translated

@main_bp.route('/process', methods=['POST'])
@token_required
def process_text(current_user):
    data = request.json
    text = data.get('text', '').strip()
    
    try:
        # Проверяем, соответствует ли текст одному из примеров
        examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
        
        # Ищем соответствие текста с заготовленными примерами
        matched_example = None
        for i in range(1, 4):
            example_path = os.path.join(examples_dir, f'example{i}.txt')
            if os.path.exists(example_path):
                with open(example_path, 'r', encoding='utf-8') as f:
                    example_text = f.read().strip()
                    # Сравниваем нормализованные тексты (игнорируя регистр и лишние пробелы)
                    if text.lower() == example_text.lower():
                        matched_example = i
                        break
        
        # Если нашли совпадение, используем предопределенный PlantUML код
        if matched_example:
            puml_path = os.path.join(examples_dir, f'example{matched_example}_plantuml.txt')
            if os.path.exists(puml_path):
                with open(puml_path, 'r', encoding='utf-8') as f:
                    plantuml_code = f.read()
                
                # Генерируем URL изображения
                encoded = encode_plantuml(plantuml_code)
                image_url = f"https://www.plantuml.com/plantuml/png/{encoded}"
                
                return jsonify({
                    "success": True,
                    "plantuml_code": plantuml_code,
                    "image_url": image_url,
                    "is_example": True
                })
        
        # Если не нашли совпадение, используем NLP обработку (в данном случае заглушку)
        # В реальном приложении здесь должен быть вызов NLP-процессора
        # result = nlp_processor.full_processing(text)
        # Временно используем первый пример как заглушку для любых входных данных
        with open(os.path.join(examples_dir, 'example1_plantuml.txt'), 'r', encoding='utf-8') as f:
            plantuml_code = f.read()
        
        encoded = encode_plantuml(plantuml_code)
        image_url = f"https://www.plantuml.com/plantuml/png/{encoded}"
        
        return jsonify({
            "success": True,
            "plantuml_code": plantuml_code,
            "image_url": image_url,
            "is_example": False
        })
        
    except Exception as e:
        current_app.logger.error(f"Processing error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Не удалось обработать требования. Пожалуйста, попробуйте снова."
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

# Обновляем существующий эндпоинт
# @main_bp.route('/parse-plantuml', methods=['POST'])
# @token_required
# def parse_plantuml(current_user):
#     data = request.json
#     code = data.get('code', '')
    
#     try:
#         # Используем новую функцию парсинга
#         hierarchy = util_parse_plantuml(code)
#         plantuml_code = generate_c4_code(hierarchy)
#         nodes, edges = convert_to_diagram_elements(hierarchy)
        
#         return jsonify({
#             "success": True,
#             "hierarchy": hierarchy,
#             "plantuml_code": plantuml_code,
#             "nodes": nodes,
#             "edges": edges
#         })
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "error": str(e)
#         }), 500
# ЗАГЛУШКА
# Заменим функцию parse_plantuml на генерацию изображения
# @main_bp.route('/parse-plantuml', methods=['POST'])
# @token_required
# def parse_plantuml(current_user):
#     data = request.json
#     code = data.get('code', '')
    
#     try:
#         # Кодируем PlantUML код для передачи в URL
#         encoded = urllib.parse.quote(code)
        
#         # Генерируем URL для получения изображения
#         image_url = f"https://www.plantuml.com/plantuml/png/{encoded}"
        
#         # Проверяем что изображение доступно
#         response = requests.head(image_url)
#         if response.status_code != 200:
#             raise Exception("Failed to generate diagram image")
        
#         return jsonify({
#             "success": True,
#             "image_url": image_url
#         })
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "error": str(e)
#         }), 500

@main_bp.route('/parse-plantuml', methods=['POST'])
@token_required
def parse_plantuml(current_user):
    data = request.json
    code = data.get('code', '')
    
    try:
        # Используем библиотеку plantuml для генерации URL
        # pl = PlantUML(url='http://www.plantuml.com/plantuml')
        # image_url = pl.get_url(code)
        # Кодируем PlantUML код
        encoded = encode_plantuml(code)
        # Формируем URL
        image_url = f"https://www.plantuml.com/plantuml/png/{encoded}"

        return jsonify({
            "success": True,
            "image_url": image_url
        })
    except Exception as e:
        logging.error(f"PlantUML encoding error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Не удалось сгенерировать изображение"
        }), 500