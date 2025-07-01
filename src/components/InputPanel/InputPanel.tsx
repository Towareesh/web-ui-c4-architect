import React, { useState, useEffect } from 'react'; // Добавлен useEffect
import { Button, TextField, Typography, CircularProgress } from '@mui/material';
import './InputPanel.css';
import { motion } from 'framer-motion';

interface InputPanelProps {
  onCreate: (requirements: string) => void;
  isLoading: boolean;
}

const InputPanel: React.FC<InputPanelProps> = ({ onCreate, isLoading }) => {
  const [requirements, setRequirements] = useState('');
  const [examples, setExamples] = useState<any[]>([]);
  const [selectedExample, setSelectedExample] = useState<number | null>(null);
  const [isLoadingExamples, setIsLoadingExamples] = useState(false);

  // Загрузка примеров при монтировании
  useEffect(() => {
    const fetchExamples = async () => {
      setIsLoadingExamples(true);
      try {
        const response = await fetch('http://localhost:5000/get-examples');
        const data = await response.json();
        setExamples(data);
      } catch (error) {
        console.error('Ошибка загрузки примеров:', error);
      } finally {
        setIsLoadingExamples(false);
      }
    };
    fetchExamples();
  }, []);

  // Загрузка выбранного примера
  useEffect(() => {
    if (selectedExample !== null) {
      const loadExample = async () => {
        try {
          const response = await fetch(`http://localhost:5000/load-example/${selectedExample}`);
          const data = await response.json();
          if (data.success) {
            setRequirements(data.text);
          }
        } catch (error) {
          console.error('Ошибка загрузки примера:', error);
        }
      };
      loadExample();
    }
  }, [selectedExample]);

  const handleCreate = () => {
    if (requirements.trim()) {
      onCreate(requirements);
    }
  };

  return (
    <motion.div 
      className="input-panel"
      initial={{ y: 100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="examples-section">
        <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 'bold' }}>
          Быстрый старт с готовыми примерами:
        </Typography>
        
        {isLoadingExamples ? (
          <div className="loading-examples">
            <CircularProgress size={20} />
            <Typography variant="body2" sx={{ ml: 1 }}>Загрузка примеров...</Typography>
          </div>
        ) : (
          <div className="example-buttons">
            {examples.map(example => (
              <Button
                key={example.id}
                variant={selectedExample === example.id ? "contained" : "outlined"}
                color={selectedExample === example.id ? "primary" : "inherit"}
                onClick={() => setSelectedExample(example.id)}
                disabled={isLoading}
                sx={{
                  flex: 1,
                  minWidth: 120,
                  textTransform: 'none',
                  m: 0.5,
                  fontWeight: selectedExample === example.id ? 'bold' : 'normal'
                }}
              >
                {example.title}
              </Button>
            ))}
          </div>
        )}
      </div>

      <TextField
        label="Опишите вашу систему"
        placeholder="Пример: Система управления библиотекой с веб-интерфейсом, API сервером и базой данных..."
        multiline
        rows={4}
        fullWidth
        value={requirements}
        onChange={(e) => setRequirements(e.target.value)}
        disabled={isLoading}
        variant="outlined"
        sx={{
          mb: 2,
          '& .MuiInputBase-root': {
            borderRadius: '12px',
            backgroundColor: 'background.paper'
          }
        }}
      />
      
      <Button
        variant="contained"
        color="primary"
        onClick={handleCreate}
        disabled={isLoading || !requirements.trim()}
        fullWidth
        size="large"
        sx={{
          py: 1.5,
          borderRadius: '12px',
          fontWeight: 'bold',
          fontSize: '1.1rem'
        }}
      >
        {isLoading ? (
          <>
            <CircularProgress size={24} sx={{ mr: 2 }} />
            Обработка...
          </>
        ) : (
          "Создать диаграмму"
        )}
      </Button>
    </motion.div>
  );
};

export default InputPanel;