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



main_bp = Blueprint('main', __name__)
nlp_processor = NLPProcessor()

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
    text = data.get('text', '')
    
    try:
        # Временное решение - генерируем фиктивный PlantUML код
        plantuml_code = """
        @startuml
        !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
        !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
        !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

        ' ==== Контекстная диаграмма (Level 1) ====
        title Системный контекст: Кластер СУБД

        Person(admin, "Администратор БД", "Управляет кластером, безопасностью, резервными копиями")
        Person(dev, "Разработчик", "Создает схемы данных, пишет запросы")
        Person(analyst, "Аналитик данных", "Выполняет сложные аналитические запросы")
        System_Boundary(db_cluster, "Высокодоступный кластер СУБД") {
            System(db_system, "Система управления базами данных", "Обработка SQL-запросов, транзакции, хранение данных")
        }

        System_Ext(app1, "Веб-приложение", "Основной потребитель данных")
        System_Ext(app2, "Мобильное приложение", "Вторичный потребитель данных")
        System_Ext(bi_tool, "BI-система", "Аналитика и отчетность")

        Rel(admin, db_system, "Администрирует", "CLI/GUI")
        Rel(dev, db_system, "Разрабатывает", "SQL/API")
        Rel(analyst, db_system, "Анализирует данные", "OLAP-запросы")
        Rel(app1, db_system, "CRUD операции", "JDBC/ODBC")
        Rel(app2, db_system, "Чтение данных", "REST API")
        Rel(bi_tool, db_system, "Сложные запросы", "SQL Connector")

        ' ==== Диаграмма контейнеров (Level 2) ====
        title Диаграмма контейнеров: Архитектура кластера

        Container_Boundary(db_cluster_boundary, "Кластер СУБД") {
            Container(query_node1, "Узел обработки запросов 1", "SQL Processor", "Обработка SELECT/INSERT/UPDATE/DELETE")
            Container(query_node2, "Узел обработки запросов 2", "SQL Processor", "Балансировка нагрузки")
            Container(storage_node1, "Узел хранения 1", "Storage Engine", "Шард A (Rows 1-10M)")
            Container(storage_node2, "Узел хранения 2", "Storage Engine", "Шард B (Rows 10M-20M)")
            Container(storage_node3, "Узел хранения 3", "Storage Engine", "Шард C (Rows 20M-30M)")
            Container(backup_service, "Сервис резервного копирования", "Backup Manager", "Ежедневные бэкапы, PITR")
            Container(monitoring, "Система мониторинга", "Prometheus Exporter", "Сбор метрик производительности")
            Container(auth_service, "Сервис аутентификации", "RBAC Engine", "Управление пользователями и правами")
        }

        ContainerDb(shared_storage, "Общее хранилище", "Distributed FS", "Холодные данные, бэкапы")
        System_Ext(cloud_storage, "Облачное хранилище", "AWS S3/Azure Blob", "Геораспределенные бэкапы")

        Rel(admin, auth_service, "Управление пользователями", "Admin API")
        Rel(admin, backup_service, "Инициирование бэкапов", "Control API")
        Rel(dev, query_node1, "Выполнение запросов", "SQL Protocol")
        Rel(analyst, query_node1, "Аналитические запросы", "SQL Protocol")

        Rel_R(query_node1, storage_node1, "Чтение/запись данных", "Internal RPC")
        Rel_R(query_node1, storage_node2, "Чтение/запись данных", "Internal RPC")
        Rel_R(query_node2, storage_node2, "Чтение/запись данных", "Internal RPC")
        Rel_R(query_node2, storage_node3, "Чтение/запись данных", "Internal RPC")

        Rel(storage_node1, storage_node2, "Синхронная репликация", "RAFT")
        Rel(storage_node2, storage_node3, "Синхронная репликация", "RAFT")

        Rel(backup_service, storage_node1, "Создание снепшотов", "Snapshot API")
        Rel(backup_service, storage_node2, "Создание снепшотов", "Snapshot API")
        Rel(backup_service, storage_node3, "Создание снепшотов", "Snapshot API")
        Rel(backup_service, shared_storage, "Хранение бэкапов", "NFS")
        Rel(backup_service, cloud_storage, "Гео-репликация бэкапов", "HTTPS")

        Rel(monitoring, query_node1, "Сбор метрик", "Metrics API")
        Rel(monitoring, storage_node1, "Сбор метрик", "Metrics API")
        Rel(admin, monitoring, "Просмотр дашбордов", "Grafana UI")

        Rel(auth_service, query_node1, "Проверка прав доступа", "Auth API")
        Rel(auth_service, storage_node1, "Проверка шифрования", "Security API")

        ' ==== Диаграмма компонентов узла хранения (Level 3) ====
        title Компоненты узла хранения

        Container_Boundary(storage_node, "Узел хранения данных") {
            Component(transaction_mgr, "Менеджер транзакций", "ACID", "Управление BEGIN/COMMIT/ROLLBACK")
            Component(storage_engine, "Движок хранения", "Storage", "Row/Columnar/JSON/BLOB")
            Component(index_mgr, "Менеджер индексов", "Indexing", "B-Tree, Hash, GIN/GIST")
            Component(replication, "Модуль репликации", "RAFT", "Синхронная/асинхронная репликация")
            Component(encryption, "Шифрование данных", "AES-256", "TDE (шифрование на лету)")
            Component(wal, "Журнал транзакций", "WAL Manager", "Write-Ahead Logging")
            Component(query_exec, "Исполнитель запросов", "Executor", "Локальное выполнение части запросов")
            Component(cache, "Кэширующий слой", "Buffer Pool", "In-Memory кэширование данных")
            
            ComponentDb(data_files, "Файлы данных", "Columnar/Row", "Постоянное хранение")
            ComponentDb(wal_files, "WAL файлы", "Append-only", "Журнал предзаписи")
        }

        Rel(transaction_mgr, wal, "Запись операций", "WAL Protocol")
        Rel(transaction_mgr, replication, "Распространение изменений")
        Rel(query_exec, storage_engine, "Чтение/запись данных")
        Rel(query_exec, index_mgr, "Использование индексов")
        Rel(query_exec, cache, "Кэширование результатов")
        Rel(storage_engine, data_files, "Сохранение на диск")
        Rel(storage_engine, encryption, "Шифрование/дешифровка")
        Rel(cache, data_files, "Загрузка/выгрузка страниц")
        Rel(wal, wal_files, "Запись журнала")
        Rel(index_mgr, data_files, "Построение индексов")
        Rel(replication, wal, "Чтение журнала для репликации")

        @enduml
        """
        
        # Генерируем URL изображения
        pl = PlantUML(url='http://www.plantuml.com/plantuml')
        image_url = pl.get_url(plantuml_code)
        
        return jsonify({
            "success": True,
            "plantuml_code": plantuml_code,
            "image_url": image_url
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