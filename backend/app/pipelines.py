import re
import torch
import json
from razdel import sentenize
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
from flask import current_app
from .utils import build_c4_hierarchy, generate_c4_code, convert_to_diagram_elements
from .constants import ENTITY_TYPES, RELATION_TYPES, C4_LEVELS

class NLPProcessor:
    def __init__(self):
        self.ner_pipeline = None
        self.re_tokenizer = None
        self.re_model = None
    
    def load_models(self):
        ner_model_path = "ner_model-20250625T131736Z-1-001/ner_model"
        re_model_path = "re_model_v2-20250625T151402Z-1-001/re_model_v2"
        
        # Загрузка NER модели
        ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_path)
        ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_path)
        self.ner_pipeline = pipeline(
            "token-classification", 
            model=ner_model, 
            tokenizer=ner_tokenizer,
            aggregation_strategy="simple"
        )
        
        # Загрузка RE модели
        self.re_tokenizer = AutoTokenizer.from_pretrained(re_model_path)
        self.re_model = AutoModelForSequenceClassification.from_pretrained(re_model_path)
    
    def preprocess_text(self, text):
        """Разделение текста на предложения с сохранением позиций"""
        return list(sentenize(text))
    
    def predict_entities(self, text):
        """Предсказание сущностей с обработкой предложений"""
        sentences = self.preprocess_text(text)
        entities = []
        
        for sent in sentences:
            results = self.ner_pipeline(sent.text)
            for entity in results:
                if entity['entity_group'] in ENTITY_TYPES and entity['word'].strip():
                    # Корректировка позиций относительно исходного текста
                    entity['start'] += sent.start
                    entity['end'] += sent.start
                    
                    # Объединение смежных сущностей
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

    def predict_relations(self, entities, text):
        """Предсказание отношений с обработкой предложений"""
        sentences = self.preprocess_text(text)
        relations = []
        
        for sent in sentences:
            # Фильтрация сущностей в текущем предложении
            sent_entities = [
                ent for ent in entities 
                if ent['start'] >= sent.start and ent['end'] <= sent.stop
            ]
            
            # Предсказание отношений внутри предложения
            relations.extend(self._predict_relations_for_sentence(sent_entities, sent.text))
        
        return relations

    def _predict_relations_for_sentence(self, entities, sentence_text):
        """Предсказание отношений для одного предложения"""
        relations = []
        
        if len(entities) < 2:
            return relations
        
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                head = entities[i]
                tail = entities[j]
                
                if abs(head['level'] - tail['level']) > 1:
                    continue
                    
                context = f"{head['text']} {tail['text']} in: {sentence_text}"
                inputs = self.re_tokenizer(
                    context, 
                    return_tensors="pt", 
                    padding=True,
                    truncation=True, 
                    max_length=128
                )
                
                outputs = self.re_model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)
                confidence, predicted_class = torch.max(probabilities, dim=1)
                
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

    def full_processing(self, text):
        """Полный цикл обработки текста"""
        if not self.ner_pipeline:
            self.load_models()
        
        entities = self.predict_entities(text)
        relations = self.predict_relations(entities, text)
        hierarchy = build_c4_hierarchy(entities, relations)
        plantuml_code = generate_c4_code(hierarchy)
        nodes, edges = convert_to_diagram_elements(hierarchy)
        
        return {
            "entities": entities,
            "relations": relations,
            "hierarchy": hierarchy,
            "plantuml_code": plantuml_code,
            "nodes": nodes,
            "edges": edges
        }