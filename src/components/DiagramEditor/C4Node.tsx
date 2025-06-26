import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { motion } from 'framer-motion';
import EditIcon from '@mui/icons-material/Edit';

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

// Функция для получения цвета по типу сущности
const getEntityColor = (entityType: string) => {
  switch (entityType) {
    case 'SYSTEM': return '#4caf50';
    case 'CONTAINER': return '#2196f3';
    case 'COMPONENT': return '#ff9800';
    case 'ACTOR': return '#9c27b0';
    case 'EXTERNAL_SYSTEM': return '#f44336';
    case 'DATABASE': return '#795548';
    case 'QUEUE': return '#607d8b';
    case 'VERB': return '#00bcd4';
    default: return '#9e9e9e';
  }
};

const C4Node: React.FC<NodeProps> = ({ data }) => {
  const icon = getEntityIcon(data.entityType);
  const color = getEntityColor(data.entityType);
  
  return (
    <motion.div 
      className="c4-node"
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
      whileHover={{ boxShadow: `0 0 15px ${color}80` }}
      style={{ borderColor: color }}
    >
      <div className="node-header" style={{ backgroundColor: `${color}20` }}>
        <div className="node-icon">{icon}</div>
        <div className="node-title">{data.label}</div>
        <EditIcon className="edit-icon" fontSize="small" />
      </div>
      <div className="node-body">
        <div className="node-type" style={{ color }}>
          {data.entityType}
        </div>
      </div>
      <Handle type="source" position={Position.Right} style={{ background: color }} />
      <Handle type="target" position={Position.Left} style={{ background: color }} />
    </motion.div>
  );
};

export default C4Node;