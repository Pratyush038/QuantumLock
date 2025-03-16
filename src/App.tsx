import React, { useState, useEffect } from 'react';
import { Lock, Unlock, Database, User, Key, Eye, EyeOff } from 'lucide-react';
import { quantumHash, validatePassword } from './utils/auth';
import type { User as UserType, AuthState } from './types';

const STORAGE_KEY = 'quantum_auth_state';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [authState, setAuthState] = useState<AuthState>(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : {
      users: [],
      currentUser: null,
      isAuthenticated: false
    };
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(authState));
  }, [authState]);

  const clearMessages = () => {
    setError(null);
    setSuccess(null);
  };

  const handleRegister = () => {
    clearMessages();

    if (!username || !password) {
      setError('Please fill in all fields');
      return;
    }

    if (!validatePassword(password)) {
      setError('Password must be at least 8 characters and contain uppercase, lowercase, numbers, and special characters');
      return;
    }

    if (authState.users.some(user => user.username === username)) {
      setError('Username already exists');
      return;
    }

    const hash = quantumHash(password);
    const newUser: UserType = { username, hash };

    setAuthState(prev => ({
      ...prev,
      users: [...prev.users, newUser]
    }));

    setSuccess('Registration successful!');
    setUsername('');
    setPassword('');
  };

  const handleLogin = () => {
    clearMessages();

    if (!username || !password) {
      setError('Please fill in all fields');
      return;
    }

    const user = authState.users.find(u => u.username === username);
    if (!user) {
      setError('User not found');
      return;
    }

    const hash = quantumHash(password);
    if (hash !== user.hash) {
      setError('Invalid password');
      return;
    }

    setAuthState(prev => ({
      ...prev,
      currentUser: username,
      isAuthenticated: true
    }));

    setSuccess('Login successful!');
    setUsername('');
    setPassword('');
  };

  const handleLogout = () => {
    setAuthState(prev => ({
      ...prev,
      currentUser: null,
      isAuthenticated: false
    }));
    clearMessages();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-800 to-blue-900 flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 w-full max-w-md shadow-2xl border border-white/20">
        <div className="flex items-center justify-center mb-8">
          {authState.isAuthenticated ? (
            <Unlock className="w-12 h-12 text-green-400" />
          ) : (
            <Lock className="w-12 h-12 text-blue-400" />
          )}
        </div>

        <h1 className="text-3xl font-bold text-center mb-8 text-white">
          {authState.isAuthenticated ? 'Welcome Back!' : 'Quantum Auth'}
        </h1>

        {authState.isAuthenticated ? (
          <div className="text-center">
            <p className="text-green-400 mb-4">
              Logged in as {authState.currentUser}
            </p>
            <button
              onClick={handleLogout}
              className="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg transition-colors"
            >
              Logout
            </button>
          </div>
        ) : (
          <>
            <div className="space-y-4">
              <div className="relative">
                <User className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="relative">
                <Key className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-12 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
                />
                <button
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-300"
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5" />
                  ) : (
                    <Eye className="h-5 w-5" />
                  )}
                </button>
              </div>

              <div className="flex gap-4">
                <button
                  onClick={handleRegister}
                  className="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition-colors"
                >
                  Register
                </button>
                <button
                  onClick={handleLogin}
                  className="flex-1 bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg transition-colors"
                >
                  Login
                </button>
              </div>
            </div>

            {error && (
              <div className="mt-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm">
                {error}
              </div>
            )}
            {success && (
              <div className="mt-4 p-3 bg-green-500/10 border border-green-500/20 rounded-lg text-green-400 text-sm">
                {success}
              </div>
            )}

            {authState.users.length > 0 && (
              <div className="mt-8 p-4 bg-white/5 rounded-lg border border-white/10">
                <div className="flex items-center gap-2 text-gray-400 mb-2">
                  <Database className="h-4 w-4" />
                  <span className="text-sm font-medium">Registered Users</span>
                </div>
                <ul className="space-y-2">
                  {authState.users.map((user) => (
                    <li
                      key={user.username}
                      className="text-sm text-gray-300 flex items-center gap-2"
                    >
                      <User className="h-4 w-4" />
                      {user.username}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;