import React, { useState, useEffect, useCallback } from 'react';
import ReactFlow, { 
  Controls, 
  Background, 
  MiniMap,
  ReactFlowProvider,
  Node,
  NodeTypes,
  applyNodeChanges,
  applyEdgeChanges,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
  NodeChange,
  EdgeChange,
  Connection,
  Edge,
  ConnectionLineType // Добавляем импорт
} from 'reactflow';
import 'reactflow/dist/style.css';
import './DiagramEditor.css';
import { motion } from 'framer-motion';
import C4Node from './C4Node';
import { Typography } from '@mui/material';

const nodeTypes: NodeTypes = {
  c4: C4Node,
};

// interface DiagramEditorProps {
//   data: { nodes: Node[]; edges: Edge[]; hierarchy?: any } | null;
//   onNodeClick?: (node: Node) => void;
//   onChange?: (nodes: Node[], edges: Edge[]) => void;
// }

// Добавим отображение изображения вместо интерактивной диаграммы
interface DiagramEditorProps {
  data: { nodes: Node[]; edges: Edge[]; hierarchy?: any } | null;
  imageUrl?: string | null; // Добавляем пропс для URL изображения
  onNodeClick?: (node: Node) => void;
  onChange?: (nodes: Node[], edges: Edge[]) => void;
}

const DiagramEditor: React.FC<DiagramEditorProps> = ({ 
  data,
  imageUrl,
  onNodeClick,
  onChange
}) => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);

  useEffect(() => {
    if (data) {
      setNodes(data.nodes);
      setEdges(data.edges);
    }
  }, [data]);

  const handleNodeClick = (_event: React.MouseEvent, node: Node) => {
    if (onNodeClick) {
      onNodeClick(node);
    }
  };

  const onNodesChange: OnNodesChange = useCallback(
    (changes: NodeChange[]) => {
      const updatedNodes = applyNodeChanges(changes, nodes);
      setNodes(updatedNodes);
      if (onChange) {
        onChange(updatedNodes, edges);
      }
    },
    [nodes, edges, onChange]
  );

  const onEdgesChange: OnEdgesChange = useCallback(
    (changes: EdgeChange[]) => {
      const updatedEdges = applyEdgeChanges(changes, edges);
      setEdges(updatedEdges);
      if (onChange) {
        onChange(nodes, updatedEdges);
      }
    },
    [nodes, edges, onChange]
  );

  const onConnect: OnConnect = useCallback(
    (connection: Connection) => {
      // Проверяем что source и target не null
      if (!connection.source || !connection.target) return;
      
      const newEdge: Edge = {
        ...connection,
        id: `edge-${connection.source}-${connection.target}-${Date.now()}`,
        animated: true,
        type: 'smoothstep',
        // Добавляем label со значением по умолчанию
        label: 'uses'
      } as Edge; // Явное приведение типа

      const updatedEdges = [...edges, newEdge];
      setEdges(updatedEdges);
      if (onChange) {
        onChange(nodes, updatedEdges);
      }
    },
    [nodes, edges, onChange]
  );
  const [imageError, setImageError] = useState(false);
  if (imageUrl) {
    return (
      <div className="diagram-image-container">
        {imageError ? (
          <div className="image-error">
            <Typography variant="h6">Не удалось загрузить изображение</Typography>
            <Typography>Проверьте синтаксис PlantUML</Typography>
          </div>
        ) : (
          <motion.img 
            src={imageUrl} 
            alt="C4 Diagram" 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            onError={() => setImageError(true)}
          />
        )}
      </div>
  // if (imageUrl) {
  //   return (
  //     <div className="diagram-image-container">
  //       <motion.img 
  //         src={imageUrl} 
  //         alt="C4 Diagram" 
  //         initial={{ opacity: 0 }}
  //         animate={{ opacity: 1 }}
  //         transition={{ duration: 0.5 }}
  //       />
  //     </div>

  // if (!data || data.nodes.length === 0) {
  //   return (
  //     <div className="diagram-placeholder">
  //       <motion.div
  //         initial={{ opacity: 0 }}
  //         animate={{ opacity: 1 }}
  //         className="placeholder-content"
  //       >
  //         <div className="animation-container">
  //           <div className="circle circle-1"></div>
  //           <div className="circle circle-2"></div>
  //           <div className="circle circle-3"></div>
  //         </div>
  //         <h3>Enter requirements to generate C4 diagram</h3>
  //         <p>Start by describing your system in the input panel below</p>
  //       </motion.div>
  //     </div>
    );
  }

  return (
    <ReactFlowProvider>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={handleNodeClick}
        nodeTypes={nodeTypes}
        fitView
        connectionLineType={ConnectionLineType.SmoothStep} // Исправляем здесь
      >
        <Background color="#5f5f5f" gap={16} />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </ReactFlowProvider>
  );
};

export default DiagramEditor;