import React, { useState, useCallback } from 'react';
import DiagramEditor from './components/DiagramEditor/DiagramEditor';
import InputPanel from './components/InputPanel/InputPanel';
import CodePanel from './components/CodePanel/CodePanel';
import AIAssistant from './components/AIAssistant/AIAssistant';
import { 
  Box, 
  Paper, 
  Typography, 
  CircularProgress, 
  Snackbar, 
  Alert, 
  IconButton, 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  TextField, 
  DialogActions, 
  Button 
} from '@mui/material';
import { motion } from 'framer-motion';
import SettingsIcon from '@mui/icons-material/Settings';
import RefreshIcon from '@mui/icons-material/Refresh';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import { Node, Edge } from 'reactflow';

// Определение типа для состояния диаграммы с иерархией
interface DiagramData {
  nodes: Node[];
  edges: Edge[];
  hierarchy?: any; // Добавлено свойство hierarchy
}

const App: React.FC = () => {
  const [diagramData, setDiagramData] = useState<DiagramData | null>(null); // Исправленный тип
  const [generatedCode, setGeneratedCode] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<DiagramData[]>([]); // Обновленный тип истории
  const [historyIndex, setHistoryIndex] = useState<number>(-1);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [editDialogOpen, setEditDialogOpen] = useState<boolean>(false);
  const [newLabel, setNewLabel] = useState<string>('');
  const [editMode, setEditMode] = useState<'select' | 'addNode' | 'addConnection'>('select');
  const [connectionSource, setConnectionSource] = useState<string | null>(null);
  const [connectionType, setConnectionType] = useState('uses');

  // Функция для автоматического расположения узлов
  const layoutElements = useCallback((nodes: Node[], edges: Edge[]): DiagramData => { // Возвращает DiagramData
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
  }, []);

  // Обработчик клика по узлу в режиме добавления связи
  const handleNodeClickForConnection = (node: Node) => {
    if (editMode === 'addConnection') {
      if (!connectionSource) {
        setConnectionSource(node.id);
      } else {
        const newEdge: Edge = {
          id: `edge-${connectionSource}-${node.id}-${Date.now()}`,
          source: connectionSource,
          target: node.id,
          label: connectionType,
          animated: true
        };

        if (diagramData) {
          const updatedEdges = [...diagramData.edges, newEdge];
          const updatedData = {
            ...diagramData,
            edges: updatedEdges
          };
          
          setDiagramData(updatedData);
          
          // Обновляем историю
          const newHistory = [...history.slice(0, historyIndex + 1), updatedData];
          setHistory(newHistory);
          setHistoryIndex(newHistory.length - 1);
        }

        setConnectionSource(null);
        setEditMode('select');
      }
    }
  };  

  // Обработка создания диаграммы
  const handleCreateDiagram = async (requirements: string) => {
    setIsProcessing(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:5000/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: requirements }),
      });
      
      if (!response.ok) {
        throw new Error('Ошибка при обработке запроса');
      }
      
      const data = await response.json();
      
      // Автоматическое расположение узлов
      const positionedData = layoutElements(data.nodes, data.edges);
      
      setDiagramData(positionedData);
      
      // Добавляем в историю
      const newHistory = [...history.slice(0, historyIndex + 1), positionedData];
      setHistory(newHistory);
      setHistoryIndex(newHistory.length - 1);
      
      setGeneratedCode(data.plantuml_code);
      
    } catch (err) {
      setError('Не удалось обработать требования. Пожалуйста, попробуйте снова.');
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };

  // Применение изменений кода
  const handleApplyCode = useCallback(async (code: string) => {
    try {
      const response = await fetch('http://localhost:5000/parse-plantuml', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      });
      
      if (!response.ok) {
        throw new Error('Ошибка при парсинге кода');
      }
      
      const data = await response.json();
      
      const positionedData = layoutElements(data.nodes, data.edges);
      
      setDiagramData(positionedData);
      
      const newHistory = [...history.slice(0, historyIndex + 1), positionedData];
      setHistory(newHistory);
      setHistoryIndex(newHistory.length - 1);
      
      setGeneratedCode(code);
      
    } catch (err) {
      setError('Не удалось обработать код. Пожалуйста, проверьте синтаксис.');
      console.error(err);
    }
  }, [history, historyIndex, layoutElements]);

  // Навигация по истории
  const handleUndo = () => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      setDiagramData(history[newIndex]);
    }
  };

  const handleRedo = () => {
    if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      setDiagramData(history[newIndex]);
    }
  };

  const handleReset = () => {
    setDiagramData(null);
    setGeneratedCode('');
    setHistory([]);
    setHistoryIndex(-1);
  };

  // Обработка действий ИИ
  const handleAIAction = useCallback(async (action: string) => {
    try {
      setIsProcessing(true);
      
      const response = await fetch('http://localhost:5000/ai-assistant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          action,
          currentDiagram: diagramData,
          currentCode: generatedCode
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to process AI request');
      }
      
      const data = await response.json();
      
      if (data.nodes && data.edges) {
        const positionedData = layoutElements(data.nodes, data.edges);
        
        setDiagramData(positionedData);
        
        const newHistory = [...history.slice(0, historyIndex + 1), positionedData];
        setHistory(newHistory);
        setHistoryIndex(newHistory.length - 1);
      }
      
      if (data.code) {
        setGeneratedCode(data.code);
      }
      
    } catch (err) {
      setError('Failed to process AI request');
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  }, [history, historyIndex, layoutElements, diagramData, generatedCode]);

  // Редактирование узлов
  const handleNodeClick = (node: Node) => {
    setSelectedNode(node);
    setNewLabel(node.data.label);
    setEditDialogOpen(true);
  };
  

  const handleLabelUpdate = () => {
    if (selectedNode && diagramData) {
      const updatedNodes = diagramData.nodes.map(n => 
        n.id === selectedNode.id 
          ? { ...n, data: { ...n.data, label: newLabel } } 
          : n
      );
      
      const updatedData = {
        ...diagramData,
        nodes: updatedNodes
      };
      
      setDiagramData(updatedData);
      
      const newHistory = [...history];
      newHistory[historyIndex] = updatedData;
      setHistory(newHistory);
      
      setEditDialogOpen(false);
    }
  };

  const handleAddNode = () => {
    if (diagramData) {
      const newNodeId = `node-${Date.now()}`;
      const newNode: Node = {
        id: newNodeId,
        position: { x: 300, y: 200 },
        data: { 
          label: 'New Node',
          entityType: 'COMPONENT'
        },
        type: 'c4'
      };
      
      const updatedNodes = [...diagramData.nodes, newNode];
      const updatedData = {
        ...diagramData,
        nodes: updatedNodes
      };
      
      setDiagramData(updatedData);
      
      const newHistory = [...history.slice(0, historyIndex + 1), updatedData];
      setHistory(newHistory);
      setHistoryIndex(newHistory.length - 1);
    }
  };

  const handleDeleteNode = () => {
    if (selectedNode && diagramData) {
      const updatedNodes = diagramData.nodes.filter(n => n.id !== selectedNode.id);
      const updatedEdges = diagramData.edges.filter(
        e => e.source !== selectedNode.id && e.target !== selectedNode.id
      );
      
      const updatedData = {
        nodes: updatedNodes,
        edges: updatedEdges
      };
      
      setDiagramData(updatedData);
      
      const newHistory = [...history.slice(0, historyIndex + 1), updatedData];
      setHistory(newHistory);
      setHistoryIndex(newHistory.length - 1);
      
      setEditDialogOpen(false);
    }
  };

  const handleCloseError = () => {
    setError(null);
  };

  return (
    <Box sx={{ 
      height: '100vh', 
      display: 'flex', 
      flexDirection: 'column', 
      bgcolor: 'background.default' 
    }}>
      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={handleCloseError}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
      
      {/* Диалог редактирования узла */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)}>
        <DialogTitle>Edit Node</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Node Label"
            fullWidth
            value={newLabel}
            onChange={(e) => setNewLabel(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={handleDeleteNode} 
            color="error"
            startIcon={<DeleteIcon />}
          >
            Delete
          </Button>
          <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleLabelUpdate} variant="contained">Save</Button>
        </DialogActions>
      </Dialog>
      
      {/* Шапка приложения */}
      <Box sx={{ 
        p: 2, 
        borderBottom: '1px solid', 
        borderColor: 'divider',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
          C4 Model Architect
        </Typography>
        
        <Box>
          <IconButton 
            onClick={handleUndo} 
            disabled={historyIndex <= 0}
            title="Undo"
          >
            <RefreshIcon sx={{ transform: 'scaleX(-1)' }} />
          </IconButton>
          
          <IconButton 
            onClick={handleRedo} 
            disabled={historyIndex >= history.length - 1}
            title="Redo"
          >
            <RefreshIcon />
          </IconButton>
          
          <IconButton 
            onClick={handleReset} 
            title="Reset"
          >
            <SettingsIcon />
          </IconButton>
          
          <IconButton 
            onClick={handleAddNode} 
            title="Add Node"
            color="primary"
          >
            <AddIcon />
          </IconButton>
        </Box>
      </Box>
      
      {/* Основной контент */}
      <Box sx={{ 
        flex: 1, 
        display: 'flex', 
        overflow: 'hidden',
        gap: '16px',
        p: '8px'
      }}>
        {/* Левая часть - диаграмма */}
        <Box sx={{ 
          flex: 3, 
          height: '100%',
          minWidth: 0,
          position: 'relative'
        }}>
          <Paper sx={{ 
            height: '100%', 
            borderRadius: 2, 
            overflow: 'hidden', 
            position: 'relative' 
          }}>
            <DiagramEditor 
              data={diagramData} 
              onNodeClick={editMode === 'addConnection' ? handleNodeClickForConnection : handleNodeClick}
            />
          </Paper>
          
          {isProcessing && (
            <Box sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              zIndex: 1000
            }}>
              <CircularProgress size={60} />
              <Typography variant="h6" sx={{ ml: 2, color: 'white' }}>
                Processing with ML...
              </Typography>
            </Box>
          )}
        </Box>
        
        {/* Правая часть - код и ассистент */}
        <Box sx={{ 
          flex: 1, 
          display: 'flex', 
          flexDirection: 'column', 
          height: '100%',
          minWidth: 0,
          gap: '16px'
        }}>
          <Paper sx={{ 
            flex: 1, 
            borderRadius: 2, 
            overflow: 'hidden',
            minHeight: 0
          }}>
            <CodePanel 
              code={generatedCode} 
              onApply={handleApplyCode}
            />
          </Paper>
          
          <Paper sx={{ 
            borderRadius: 2, 
            overflow: 'hidden',
            flexShrink: 0,
            height: '30%'
          }}>
            <AIAssistant onAction={handleAIAction} />
          </Paper>
        </Box>
      </Box>
      
      <motion.div
        initial={{ y: 100 }}
        animate={{ y: 0 }}
        transition={{ type: 'spring', damping: 25 }}
      >
        <InputPanel onCreate={handleCreateDiagram} isLoading={isProcessing} />
      </motion.div>
    </Box>
  );
};

export default App;