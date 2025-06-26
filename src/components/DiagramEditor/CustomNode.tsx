// import React from 'react';
// import { Handle, Position } from 'reactflow';
// import type { NodeProps } from 'reactflow';
// import { motion } from 'framer-motion';

// const CustomNode: React.FC<NodeProps> = ({ data }) => {
//   return (
//     <motion.div 
//       className="custom-node"
//       initial={{ scale: 0.8, opacity: 0 }}
//       animate={{ scale: 1, opacity: 1 }}
//       transition={{ duration: 0.3 }}
//       whileHover={{ boxShadow: '0 0 15px rgba(25, 118, 210, 0.5)' }}
//     >
//       <div className="node-header">
//         <div className="node-icon">📱</div>
//         <div className="node-title">{data.label}</div>
//       </div>
//       <div className="node-body">
//         <div className="node-info">Type: System Component</div>
//         <div className="node-status">Status: Active</div>
//       </div>
//       <Handle type="source" position={Position.Right} />
//       <Handle type="target" position={Position.Left} />
//     </motion.div>
//   )
// }

// export default CustomNode

import React from 'react';
import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import { motion } from 'framer-motion';

// Функция для получения иконки по типу сущности
const getEntityIcon = (entityType: string) => {
  switch (entityType) {
    case 'SYSTEM': return '🖥️';
    case 'CONTAINER': return '📦';
    case 'COMPONENT': return '⚙️';
    case 'ACTOR': return '👤';
    case 'EXTERNAL_SYSTEM': return '🌐';
    case 'DATABASE': return '💾';
    case 'QUEUE': return '📫';
    case 'VERB': return '🏃';
    default: return '❓';
  }
};

const CustomNode: React.FC<NodeProps> = ({ data }) => {
  return (
    <motion.div 
      className="custom-node"
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
      whileHover={{ boxShadow: '0 0 15px rgba(25, 118, 210, 0.5)' }}
    >
      <div className="node-header">
        <div className="node-icon">{getEntityIcon(data.entityType)}</div>
        <div className="node-title">{data.label}</div>
      </div>
      <div className="node-body">
        <div className="node-info">Type: {data.entityType}</div>
      </div>
      <Handle type="source" position={Position.Right} />
      <Handle type="target" position={Position.Left} />
    </motion.div>
  );
};

export default CustomNode;