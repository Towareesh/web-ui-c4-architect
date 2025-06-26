import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { Box, Typography, Button, CircularProgress } from '@mui/material';
import './CodePanel.css';
import { motion } from 'framer-motion';

interface CodePanelProps {
  code: string;
  onApply?: (code: string) => void;
}

const CodePanel: React.FC<CodePanelProps> = ({ 
  code, 
  onApply 
}) => {
  const [editorLoaded, setEditorLoaded] = useState(false);
  const [currentCode, setCurrentCode] = useState(code);
  const [isModified, setIsModified] = useState(false);
  const [isValid, setIsValid] = useState(true);

  // Синхронизируем текущий код при получении нового кода извне
  useEffect(() => {
    setCurrentCode(code);
    setIsModified(false);
  }, [code]);

  const handleEditorChange = (value: string | undefined) => {
    if (value !== undefined) {
      setCurrentCode(value);
      setIsModified(true);
      
      // Простая валидация кода
      const isValidCode = validatePlantUML(value);
      setIsValid(isValidCode);
    }
  };

  const validatePlantUML = (code: string) => {
    // Простая проверка на наличие ключевых слов
    return code.includes('System') || code.includes('Rel');
  };

  const handleApply = () => {
    if (onApply && isModified && isValid) {
      onApply(currentCode);
      setIsModified(false);
    }
  };

  return (
    <Box className="code-panel">
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        p: 2, 
        borderBottom: '1px solid #333',
        backgroundColor: '#1e1e1e'
      }}>
        <Typography variant="h6">
          Diagram Code
        </Typography>
        <Button
          variant="contained"
          color={isValid ? "primary" : "error"}
          size="small"
          disabled={!isModified || !isValid}
          onClick={handleApply}
          sx={{
            position: 'relative',
            overflow: 'hidden',
            '&:after': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              width: isModified ? '100%' : '0%',
              height: '100%',
              backgroundColor: 'rgba(255, 255, 255, 0.2)',
              transition: 'width 0.3s',
              pointerEvents: 'none'
            }
          }}
        >
          Apply Changes
          {!isValid && (
            <motion.span
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              style={{
                position: 'absolute',
                top: -5,
                right: -5,
                backgroundColor: 'red',
                color: 'white',
                borderRadius: '50%',
                width: 20,
                height: 20,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 12
              }}
            >
              !
            </motion.span>
          )}
        </Button>
      </Box>
      
      <motion.div 
        className="editor-container"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {!editorLoaded && (
          <Box sx={{ 
            height: '100%', 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center',
            backgroundColor: '#1e1e1e'
          }}>
            <CircularProgress size={24} />
            <Typography sx={{ ml: 2 }}>Loading editor...</Typography>
          </Box>
        )}
        
        <Editor
          height="100%"
          language="plantuml"
          value={currentCode}
          theme="vs-dark"
          options={{
            minimap: { enabled: true },
            fontSize: 14,
            scrollBeyondLastLine: false,
            automaticLayout: true,
          }}
          onChange={handleEditorChange}
          onMount={() => setEditorLoaded(true)}
        />
      </motion.div>
    </Box>
  );
};

export default CodePanel;