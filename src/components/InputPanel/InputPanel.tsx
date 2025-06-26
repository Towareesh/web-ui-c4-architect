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