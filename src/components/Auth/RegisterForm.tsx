import React, { useState } from 'react';
import { Box, TextField, Button, Typography, CircularProgress } from '@mui/material';

interface RegisterFormProps {
  onRegister: (username: string, password: string) => Promise<void>;
  onSwitchToLogin: () => void;
  error?: string;
  isLoading: boolean;
}

const RegisterForm: React.FC<RegisterFormProps> = ({ 
  onRegister, 
  onSwitchToLogin,
  error, 
  isLoading 
}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("Passwords don't match");
      return;
    }
    onRegister(username, password);
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
      <TextField
        label="Confirm Password"
        fullWidth
        margin="normal"
        type="password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
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
        {isLoading ? <CircularProgress size={24} /> : 'Register'}
      </Button>
      <Typography align="center">
        Already have an account?{' '}
        <Button 
          color="primary" 
          onClick={onSwitchToLogin}
          sx={{ textTransform: 'none' }}
        >
          Sign in
        </Button>
      </Typography>
    </Box>
  );
};

export default RegisterForm;