Вот готовый проект MVP для вашей системы с красивым интерфейсом. Начнем с создания структуры и установки:

### 1. Создание проекта и установка зависимостей

```bash
# Создаем проект
npm create vite@latest open-webui -- --template react-ts
cd open-webui

# Устанавливаем зависимости
npm install
npm install @mui/material @emotion/react @emotion/styled
npm install reactflow
npm install @monaco-editor/react
npm install framer-motion
```

### 2. Структура проекта
```
src/
├── components/
│   ├── DiagramEditor/
│   │   ├── DiagramEditor.tsx
│   │   └── DiagramEditor.css
│   ├── InputPanel/
│   │   ├── InputPanel.tsx
│   │   └── InputPanel.css
│   ├── CodePanel/
│   │   ├── CodePanel.tsx
│   │   └── CodePanel.css
│   └── AIAssistant/
│       └── AIAssistant.tsx
├── App.tsx
├── main.tsx
├── index.css
└── assets/
    └── styles/
        └── global.css
```

### 3. Код компонентов

**src/main.tsx** (обновляем):
```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { ThemeProvider, createTheme } from '@mui/material'
import CssBaseline from '@mui/material/CssBaseline'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1976d2',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
  typography: {
    fontFamily: "'Inter', sans-serif",
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>
)
```

**src/App.tsx**:
```tsx
import React, { useState } from 'react'
import DiagramEditor from './components/DiagramEditor/DiagramEditor'
import InputPanel from './components/InputPanel/InputPanel'
import CodePanel from './components/CodePanel/CodePanel'
import AIAssistant from './components/AIAssistant/AIAssistant'
import { Box, Grid, Paper, Typography } from '@mui/material'
import { motion } from 'framer-motion'

const App: React.FC = () => {
  const [diagramData, setDiagramData] = useState<any>(null)
  const [generatedCode, setGeneratedCode] = useState<string>('')
  const [isProcessing, setIsProcessing] = useState<boolean>(false)

  const handleCreateDiagram = (requirements: string) => {
    setIsProcessing(true)
    
    // Эмуляция работы ML-ядра
    setTimeout(() => {
      const mockDiagram = {
        nodes: [
          { id: '1', position: { x: 100, y: 100 }, data: { label: 'Client App' } },
          { id: '2', position: { x: 400, y: 100 }, data: { label: 'API Server' } },
          { id: '3', position: { x: 400, y: 300 }, data: { label: 'Database' } },
        ],
        edges: [
          { id: 'e1-2', source: '1', target: '2', label: 'HTTP Requests' },
          { id: 'e2-3', source: '2', target: '3', label: 'SQL Queries' },
        ]
      }
      
      const mockCode = `// C4 Diagram Code
System(clientApp, "Client Application", "React-based UI")
System(apiServer, "API Server", "Node.js with Express")
System(db, "Database", "PostgreSQL")

Rel(clientApp, apiServer, "HTTP Requests", "JSON/HTTPS")
Rel(apiServer, db, "SQL Queries", "TCP")`
      
      setDiagramData(mockDiagram)
      setGeneratedCode(mockCode)
      setIsProcessing(false)
    }, 2000)
  }

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column', bgcolor: 'background.default' }}>
      <Box sx={{ p: 2, borderBottom: '1px solid', borderColor: 'divider' }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
          C4 Model Architect
        </Typography>
      </Box>
      
      <Grid container sx={{ flex: 1, overflow: 'hidden' }}>
        <Grid item xs={8} sx={{ height: '100%' }}>
          <Paper sx={{ height: '100%', borderRadius: 2, m: 1, overflow: 'hidden', position: 'relative' }}>
            <DiagramEditor data={diagramData} />
          </Paper>
        </Grid>
        
        <Grid item xs={4} sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          <Paper sx={{ flex: 1, borderRadius: 2, m: 1, overflow: 'hidden' }}>
            <CodePanel code={generatedCode} />
          </Paper>
          
          <Paper sx={{ borderRadius: 2, m: 1, overflow: 'hidden' }}>
            <AIAssistant />
          </Paper>
        </Grid>
      </Grid>
      
      <motion.div
        initial={{ y: 100 }}
        animate={{ y: 0 }}
        transition={{ type: 'spring', damping: 25 }}
      >
        <InputPanel onCreate={handleCreateDiagram} isLoading={isProcessing} />
      </motion.div>
    </Box>
  )
}

export default App
```

**src/components/DiagramEditor/DiagramEditor.tsx**:
```tsx
import React, { useCallback } from 'react'
import ReactFlow, { 
  Controls, 
  Background, 
  MiniMap,
  Node,
  Edge,
  NodeTypes,
  ReactFlowProvider
} from 'reactflow'
import 'reactflow/dist/style.css'
import './DiagramEditor.css'
import { motion } from 'framer-motion'
import CustomNode from './CustomNode'

const nodeTypes: NodeTypes = {
  custom: CustomNode,
}

const DiagramEditor: React.FC<{ data: any }> = ({ data }) => {
  const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    console.log('Node clicked:', node)
  }, [])

  if (!data) {
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
    )
  }

  return (
    <ReactFlowProvider>
      <ReactFlow
        nodes={data.nodes}
        edges={data.edges}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}
        fitView
      >
        <Background color="#5f5f5f" gap={16} />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </ReactFlowProvider>
  )
}

export default DiagramEditor
```

**src/components/DiagramEditor/CustomNode.tsx**:
```tsx
import React from 'react'
import { Handle, Position, NodeProps } from 'reactflow'
import { motion } from 'framer-motion'

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
        <div className="node-icon">📱</div>
        <div className="node-title">{data.label}</div>
      </div>
      <div className="node-body">
        <div className="node-info">Type: System Component</div>
        <div className="node-status">Status: Active</div>
      </div>
      <Handle type="source" position={Position.Right} />
      <Handle type="target" position={Position.Left} />
    </motion.div>
  )
}

export default CustomNode
```

**src/components/DiagramEditor/DiagramEditor.css**:
```css
.diagram-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background: #1e1e1e;
  color: #a0a0a0;
}

.placeholder-content {
  text-align: center;
  max-width: 500px;
}

.animation-container {
  position: relative;
  height: 120px;
  margin-bottom: 30px;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(145deg, #1976d2, #5e9ce0);
  opacity: 0.7;
}

.circle-1 {
  width: 80px;
  height: 80px;
  top: 20px;
  left: calc(50% - 40px);
  animation: pulse 3s infinite ease-in-out;
}

.circle-2 {
  width: 60px;
  height: 60px;
  top: 30px;
  left: calc(50% - 70px);
  animation: pulse 3s infinite 0.5s ease-in-out;
}

.circle-3 {
  width: 60px;
  height: 60px;
  top: 30px;
  left: calc(50% + 10px);
  animation: pulse 3s infinite 1s ease-in-out;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.1); opacity: 0.4; }
  100% { transform: scale(1); opacity: 0.7; }
}

.custom-node {
  background: #252526;
  border: 1px solid #3a3a3a;
  border-radius: 8px;
  padding: 15px;
  width: 250px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: box-shadow 0.3s ease;
}

.node-header {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #3a3a3a;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.node-icon {
  font-size: 24px;
  margin-right: 10px;
}

.node-title {
  font-weight: bold;
  font-size: 16px;
  color: #e0e0e0;
}

.node-body {
  font-size: 14px;
}

.node-info {
  color: #a0a0a0;
  margin-bottom: 5px;
}

.node-status {
  color: #4caf50;
  font-weight: 500;
}
```

**src/components/InputPanel/InputPanel.tsx**:
```tsx
import React, { useState } from 'react'
import { 
  TextField, 
  Button, 
  Box, 
  CircularProgress,
  Typography,
  IconButton
} from '@mui/material'
import SendIcon from '@mui/icons-material/Send'
import './InputPanel.css'
import { motion } from 'framer-motion'

interface InputPanelProps {
  onCreate: (requirements: string) => void
  isLoading: boolean
}

const InputPanel: React.FC<InputPanelProps> = ({ onCreate, isLoading }) => {
  const [requirements, setRequirements] = useState('')
  const [isFocused, setIsFocused] = useState(false)

  const handleSubmit = () => {
    if (requirements.trim() && !isLoading) {
      onCreate(requirements)
    }
  }

  return (
    <Box className={`input-panel ${isFocused ? 'focused' : ''}`}>
      <TextField
        fullWidth
        multiline
        minRows={2}
        maxRows={6}
        variant="outlined"
        placeholder="Enter FR/NFR requirements for client-server system..."
        value={requirements}
        onChange={(e) => setRequirements(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        disabled={isLoading}
        InputProps={{
          endAdornment: (
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <IconButton
                color="primary"
                onClick={handleSubmit}
                disabled={isLoading || !requirements.trim()}
              >
                {isLoading ? (
                  <CircularProgress size={24} color="inherit" />
                ) : (
                  <SendIcon />
                )}
              </IconButton>
            </motion.div>
          ),
          sx: {
            color: 'white',
            backgroundColor: '#252526',
            borderRadius: '12px',
            padding: '10px 15px',
          }
        }}
      />
      
      <Box className="examples-container">
        <Typography variant="caption" color="textSecondary" sx={{ mr: 1 }}>
          Try:
        </Typography>
        <Button 
          variant="outlined" 
          size="small"
          onClick={() => setRequirements('User authentication with JWT tokens')}
        >
          Auth Example
        </Button>
        <Button 
          variant="outlined" 
          size="small"
          sx={{ ml: 1 }}
          onClick={() => setRequirements('Payment processing with Stripe API')}
        >
          Payment Example
        </Button>
      </Box>
    </Box>
  )
}

export default InputPanel
```

**src/components/InputPanel/InputPanel.css**:
```css
.input-panel {
  padding: 16px;
  background: #1e1e1e;
  border-top: 1px solid #333;
  transition: all 0.3s ease;
}

.input-panel.focused {
  background: #252526;
  box-shadow: 0 -5px 15px rgba(0, 0, 0, 0.3);
}

.examples-container {
  display: flex;
  align-items: center;
  margin-top: 10px;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.input-panel:hover .examples-container {
  opacity: 1;
}
```

**src/components/CodePanel/CodePanel.tsx**:
```tsx
import React from 'react'
import Editor from '@monaco-editor/react'
import { Box, Typography } from '@mui/material'
import './CodePanel.css'
import { motion } from 'framer-motion'

interface CodePanelProps {
  code: string
}

const CodePanel: React.FC<CodePanelProps> = ({ code }) => {
  return (
    <Box className="code-panel">
      <Typography variant="h6" sx={{ p: 2, borderBottom: '1px solid #333' }}>
        Generated Diagram Code
      </Typography>
      
      <motion.div 
        className="editor-container"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Editor
          height="100%"
          language="c4"
          value={code}
          theme="vs-dark"
          options={{
            readOnly: true,
            minimap: { enabled: true },
            fontSize: 14,
            scrollBeyondLastLine: false,
            automaticLayout: true,
          }}
        />
      </motion.div>
    </Box>
  )
}

export default CodePanel
```

**src/components/CodePanel/CodePanel.css**:
```css
.code-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.editor-container {
  flex: 1;
  overflow: hidden;
}
```

**src/components/AIAssistant/AIAssistant.tsx**:
```tsx
import React, { useState } from 'react'
import { 
  Box, 
  Typography, 
  TextField, 
  IconButton, 
  List, 
  ListItem, 
  ListItemText,
  Avatar,
  Paper
} from '@mui/material'
import SendIcon from '@mui/icons-material/Send'
import SmartToyIcon from '@mui/icons-material/SmartToy'
import { motion, AnimatePresence } from 'framer-motion'

const AIAssistant: React.FC = () => {
  const [messages, setMessages] = useState<{ text: string; isUser: boolean }[]>([
    { text: "Hello! I'm your AI assistant. How can I help with your diagram?", isUser: false }
  ])
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim()) {
      // Add user message
      setMessages([...messages, { text: input, isUser: true }])
      setInput('')
      
      // Simulate AI response
      setTimeout(() => {
        setMessages(prev => [
          ...prev, 
          { 
            text: "I've updated the diagram based on your request. The authentication flow now includes JWT tokens and refresh tokens.", 
            isUser: false 
          }
        ])
      }, 1500)
    }
  }

  return (
    <Box className="ai-assistant">
      <Typography variant="h6" sx={{ p: 2, borderBottom: '1px solid #333' }}>
        AI Assistant
      </Typography>
      
      <Box className="chat-container">
        <List sx={{ p: 1, height: '200px', overflowY: 'auto' }}>
          <AnimatePresence>
            {messages.map((msg, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
              >
                <ListItem sx={{ 
                  justifyContent: msg.isUser ? 'flex-end' : 'flex-start',
                  alignItems: 'flex-start',
                  mb: 1
                }}>
                  {!msg.isUser && (
                    <Avatar sx={{ bgcolor: 'primary.main', mr: 1 }}>
                      <SmartToyIcon />
                    </Avatar>
                  )}
                  <Paper sx={{ 
                    p: 1.5, 
                    maxWidth: '70%',
                    bgcolor: msg.isUser ? 'primary.dark' : 'grey.800',
                    borderRadius: msg.isUser 
                      ? '18px 18px 0 18px' 
                      : '18px 18px 18px 0'
                  }}>
                    <ListItemText 
                      primary={msg.text} 
                      sx={{ color: 'white' }} 
                    />
                  </Paper>
                </ListItem>
              </motion.div>
            ))}
          </AnimatePresence>
        </List>
        
        <Box sx={{ display: 'flex', p: 1, borderTop: '1px solid #333' }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Ask AI to modify the diagram..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            size="small"
            sx={{ 
              backgroundColor: '#252526',
              borderRadius: '20px',
              '& .MuiOutlinedInput-root': {
                borderRadius: '20px',
                paddingRight: '12px'
              }
            }}
            InputProps={{
              endAdornment: (
                <IconButton 
                  onClick={handleSend}
                  disabled={!input.trim()}
                  size="small"
                  sx={{ color: 'primary.main' }}
                >
                  <SendIcon />
                </IconButton>
              )
            }}
          />
        </Box>
      </Box>
    </Box>
  )
}

export default AIAssistant
```

**src/index.css**:
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #121212;
  color: #e0e0e0;
  height: 100vh;
  overflow: hidden;
}

#root {
  height: 100%;
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #1e1e1e;
}

::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
```

### 4. Запуск приложения
```bash
npm run dev
```

### 5. Функциональность MVP
1. **Ввод требований**: Пользователь вводит FR/NFR в нижней панели
2. **Генерация диаграммы**: ML-ядро обрабатывает требования (пока эмуляция)
3. **Визуализация**: Диаграмма отображается в основном окне как интерактивный граф
4. **Код диаграммы**: Сгенерированный код отображается справа
5. **AI Assistant**: Правая панель снизу для взаимодействия с ИИ

### 6. Следующие этапы разработки
1. **Интеграция с ML-моделями**:
   - Подключение Python-бекенда через REST API
   - Формат запроса: `{ "requirements": "текст требований" }`
   - Формат ответа: `{ "diagram": {...}, "code": "строка" }`

2. **Редактирование диаграммы**:
   - Drag-n-drop элементов
   - Контекстное меню для узлов
   - Связывание элементов
   - Автоматическая перегенерация при изменении

3. **ИИ-ассистент**:
   - Реальная интеграция с GPT/LLM
   - Обработка запросов: "Добавь балансировщик нагрузки"
   - Автоматическое обновление диаграммы

4. **Экспорт и сохранение**:
   - Экспорт в PNG/SVG
   - Сохранение проектов
   - Генерация документации

5. **Анимации и UX-улучшения**:
   - Плавные переходы между состояниями
   - Интерактивные туториалы
   - Визуализация процессов генерации

### 7. Команды для запуска (Windows)
```powershell
# Установка зависимостей
npm install

# Запуск dev-сервера
npm run dev

# Сборка для production
npm run build
```

Этот MVP реализует запрошенный интерфейс с анимациями, плавными переходами и профессиональным дизайном в стиле современных инструментов. Код структурирован для легкой интеграции с ML-ядром и дальнейшего расширения функциональности.