import React, { useState } from 'react';
import { Box, TextField, Button, Typography, CircularProgress } from '@mui/material';

interface LoginFormProps {
  onLogin: (username: string, password: string) => Promise<void>;
  onSwitchToRegister: () => void;
  error?: string;
  isLoading: boolean;
}

const LoginForm: React.FC<LoginFormProps> = ({ 
  onLogin, 
  onSwitchToRegister,
  error, 
  isLoading 
}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onLogin(username, password);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <TextField
        label="Username"
        fullWidth
        margin="normal"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <TextField
        label="Password"
        fullWidth
        margin="normal"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      {error && (
        <Typography color="error" sx={{ mt: 1 }}>
          {error}
        </Typography>
      )}
      <Button
        type="submit"
        fullWidth
        variant="contained"
        sx={{ mt: 3, mb: 2 }}
        disabled={isLoading}
      >
        {isLoading ? <CircularProgress size={24} /> : 'Sign In'}
      </Button>
      <Typography align="center">
        Don't have an account?{' '}
        <Button 
          color="primary" 
          onClick={onSwitchToRegister}
          sx={{ textTransform: 'none' }}
        >
          Register
        </Button>
      </Typography>
    </Box>
  );
};

export default LoginForm;