import { Node, Edge } from 'reactflow';

export const layoutElements = (nodes: Node[], edges: Edge[]) => {
  // Простой алгоритм размещения в виде сетки
  const GRID_COLS = 4;
  const NODE_WIDTH = 250;
  const NODE_HEIGHT = 150;
  const HORIZONTAL_SPACING = 100;
  const VERTICAL_SPACING = 80;
  
  const positionedNodes = nodes.map((node, index) => {
    const row = Math.floor(index / GRID_COLS);
    const col = index % GRID_COLS;
    
    return {
      ...node,
      position: { 
        x: col * (NODE_WIDTH + HORIZONTAL_SPACING) + 50, 
        y: row * (NODE_HEIGHT + VERTICAL_SPACING) + 50 
      },
      style: {
        width: NODE_WIDTH,
        height: NODE_HEIGHT
      }
    };
  });
  
  return { 
    nodes: positionedNodes, 
    edges: edges.map(edge => ({
      ...edge,
      animated: true
    })) 
  };
};