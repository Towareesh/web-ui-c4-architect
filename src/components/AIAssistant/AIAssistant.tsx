import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  TextField, 
  IconButton, 
  List, 
  ListItem, 
  ListItemText,
  Avatar,
  Paper,
  CircularProgress,
  Button
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import { motion, AnimatePresence } from 'framer-motion';

interface AIAssistantProps {
  onAction: (action: string) => void;
}

interface Message {
  text: string;
  isUser: boolean;
}

const AIAssistant: React.FC<AIAssistantProps> = ({ onAction }) => {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hello! I'm your AI assistant. How can I help with your diagram?", isUser: false }
  ]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  
  const predefinedActions = [
    "Add load balancer",
    "Simplify architecture",
    "Add security layer",
    "Optimize database access",
    "Add caching mechanism"
  ];

  const handleSend = () => {
    if (input.trim()) {
      const userMessage: Message = { text: input, isUser: true };
      setMessages(prev => [...prev, userMessage]);
      onAction(input);
      setIsProcessing(true);
      setInput('');
    }
  };

  useEffect(() => {
    if (isProcessing) {
      const timer = setTimeout(() => {
        setMessages(prev => [
          ...prev, 
          { 
            text: "I've updated the diagram based on your request. The authentication flow now includes JWT tokens and refresh tokens.", 
            isUser: false 
          }
        ]);
        setIsProcessing(false);
      }, 1500);
      
      return () => clearTimeout(timer);
    }
  }, [isProcessing]);

  // Исправленная функция с возвратом значения
  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
    const userMessage: Message = { text: suggestion, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    onAction(suggestion);
    setIsProcessing(true);
    setInput('');
  };

  return (
    <Box className="ai-assistant" sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h6" sx={{ 
        p: 2, 
        borderBottom: '1px solid #333',
        display: 'flex',
        alignItems: 'center',
        backgroundColor: '#1e1e1e'
      }}>
        <SmartToyIcon sx={{ mr: 1, color: 'primary.main' }} />
        AI Assistant
      </Typography>
      
      <Box sx={{ 
        flex: 1, 
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {messages.length <= 1 && (
          <Box sx={{ p: 2, borderBottom: '1px solid #333' }}>
            <Typography variant="subtitle2" sx={{ mb: 1, color: '#aaa' }}>
              Try asking:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {predefinedActions.map((suggestion, index) => (
                <motion.div
                  key={index}
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => handleSuggestionClick(suggestion)}
                    sx={{
                      textTransform: 'none',
                      fontSize: '0.8rem',
                      borderRadius: '12px',
                      color: '#ddd',
                      borderColor: '#444'
                    }}
                  >
                    {suggestion}
                  </Button>
                </motion.div>
              ))}
            </Box>
          </Box>
        )}
        
        <List sx={{ 
          flex: 1, 
          overflowY: 'auto',
          p: 1,
          backgroundColor: '#121212'
        }}>
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
                  mb: 1,
                  px: 0
                }}>
                  {!msg.isUser && (
                    <Avatar sx={{ 
                      bgcolor: 'primary.main', 
                      mr: 1,
                      width: 32,
                      height: 32
                    }}>
                      <SmartToyIcon fontSize="small" />
                    </Avatar>
                  )}
                  <Paper sx={{ 
                    p: 1.5, 
                    maxWidth: '85%',
                    bgcolor: msg.isUser ? 'primary.dark' : 'grey.800',
                    borderRadius: msg.isUser 
                      ? '18px 18px 0 18px' 
                      : '18px 18px 18px 0',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)'
                  }}>
                    <ListItemText 
                      primary={msg.text} 
                      sx={{ 
                        color: 'white',
                        '& .MuiListItemText-primary': {
                          fontSize: '0.9rem',
                          lineHeight: 1.4
                        }
                      }} 
                    />
                  </Paper>
                </ListItem>
              </motion.div>
            ))}
            
            {isProcessing && (
              <ListItem sx={{ justifyContent: 'flex-start', alignItems: 'center' }}>
                <Avatar sx={{ 
                  bgcolor: 'primary.main', 
                  mr: 1,
                  width: 32,
                  height: 32
                }}>
                  <SmartToyIcon fontSize="small" />
                </Avatar>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <CircularProgress size={20} sx={{ mr: 1 }} />
                  <Typography variant="body2" color="textSecondary">
                    Thinking...
                  </Typography>
                </Box>
              </ListItem>
            )}
          </AnimatePresence>
        </List>
        
        <Box sx={{ 
          p: 1, 
          borderTop: '1px solid #333',
          backgroundColor: '#1e1e1e'
        }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Ask AI to modify the diagram..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !isProcessing && handleSend()}
            size="small"
            disabled={isProcessing}
            sx={{ 
              backgroundColor: '#252526',
              borderRadius: '20px',
              '& .MuiOutlinedInput-root': {
                borderRadius: '20px',
                paddingRight: '8px',
                '& input': {
                  padding: '8px 16px',
                  fontSize: '0.9rem'
                }
              }
            }}
            InputProps={{
              endAdornment: (
                <IconButton 
                  onClick={handleSend}
                  disabled={!input.trim() || isProcessing}
                  size="small"
                  sx={{ color: 'primary.main' }}
                >
                  {isProcessing ? (
                    <CircularProgress size={20} />
                  ) : (
                    <SendIcon />
                  )}
                </IconButton>
              )
            }}
          />
        </Box>
      </Box>
    </Box>
  );
};

export default AIAssistant;