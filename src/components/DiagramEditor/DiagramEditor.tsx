import React from 'react';
import ReactFlow, { 
  Controls, 
  Background, 
  MiniMap,
  ReactFlowProvider,
  Node,
  NodeTypes
} from 'reactflow';
import 'reactflow/dist/style.css';
import './DiagramEditor.css';
import { motion } from 'framer-motion';
import C4Node from './C4Node';

const nodeTypes: NodeTypes = {
  c4: C4Node,
};

interface DiagramEditorProps {
  data: { nodes: Node[]; edges: any[] } | null;
  onNodeClick?: (node: Node) => void;
}

const DiagramEditor: React.FC<DiagramEditorProps> = ({ data, onNodeClick }) => {
  const handleNodeClick = (_event: React.MouseEvent, node: Node) => {
    if (onNodeClick) {
      onNodeClick(node);
    }
  };

  if (!data || data.nodes.length === 0) {
    return (
      <div className="diagram-placeholder">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="placeholder-content"
        >
          <div className="animation-container">
            <div className="circle circle-1"></div>
            <div className="circle circle-2"></div>
            <div className="circle circle-3"></div>
          </div>
          <h3>Enter requirements to generate C4 diagram</h3>
          <p>Start by describing your system in the input panel below</p>
        </motion.div>
      </div>
    );
  }

  return (
    <ReactFlowProvider>
      <ReactFlow
        nodes={data.nodes}
        edges={data.edges}
        onNodeClick={handleNodeClick}
        nodeTypes={nodeTypes}
        fitView
      >
        <Background color="#5f5f5f" gap={16} />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </ReactFlowProvider>
  );
};

export default DiagramEditor;