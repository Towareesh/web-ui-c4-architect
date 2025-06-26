// interface Entity {
//   id: string;
//   label: string;
//   type: string;
// }

// interface Relation {
//   source: string;
//   target: string;
//   label: string;
// }

// export const generateC4Code = (nodes: Entity[], edges: Relation[]): string => {
//   // Сопоставление типов сущностей с PlantUML-макросами
//   const typeMap: Record<string, string> = {
//     SYSTEM: 'System',
//     CONTAINER: 'Container',
//     COMPONENT: 'Component',
//     ACTOR: 'Person',
//     EXTERNAL_SYSTEM: 'System_Ext',
//     DATABASE: 'Database',
//     QUEUE: 'Queue',
//     VERB: 'Component'
//   };

//   // Генерация уникальных идентификаторов
//   const idMap: Record<string, string> = {};
//   let code = "@startuml\n";
//   code += "!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml\n\n";
  
//   // Добавление участников
//   code += "LAYOUT_WITH_LEGEND()\n\n";
  
//   // Создание сущностей
//   nodes.forEach((node, index) => {
//     const cleanId = node.id.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '');
//     idMap[node.id] = cleanId;
    
//     const plantUmlType = typeMap[node.type] || 'Component';
//     const description = node.type === 'ACTOR' ? 'Person' : '';
    
//     code += `${plantUmlType}(${cleanId}, "${node.label}", "${description}")\n`;
//   });
  
//   // Создание связей
//   edges.forEach((edge, index) => {
//     const sourceId = idMap[edge.source] || edge.source;
//     const targetId = idMap[edge.target] || edge.target;
    
//     code += `Rel(${sourceId}, ${targetId}, "${edge.label}")\n`;
//   });
  
//   code += "@enduml";
//   return code;
// };

// // Функция для парсинга PlantUML обратно в элементы диаграммы
// export const parseC4Code = (code: string) => {
//   const nodes: Entity[] = [];
//   const edges: Relation[] = [];
  
//   const entityRegex = /(\w+)\((\w+),\s*"([^"]+)",\s*"([^"]*)"\)/g;
//   const relationRegex = /Rel\((\w+),\s*(\w+),\s*"([^"]+)"\)/g;
  
//   let match;
//   while ((match = entityRegex.exec(code)) !== null) {
//     nodes.push({
//       id: match[2],
//       label: match[3],
//       type: match[1].toUpperCase()
//     });
//   }
  
//   while ((match = relationRegex.exec(code)) !== null) {
//     edges.push({
//       source: match[1],
//       target: match[2],
//       label: match[3]
//     });
//   }
  
//   return { nodes, edges };
// };