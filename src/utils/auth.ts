import SHA256 from 'crypto-js/sha256';

// Simulated quantum-inspired hash function
export const quantumHash = (input: string): string => {
  // Create multiple hash rounds to simulate quantum superposition
  const round1 = SHA256(input).toString();
  const round2 = SHA256(round1 + input).toString();
  const round3 = SHA256(round2 + round1).toString();

  // Combine the rounds in a way that simulates quantum interference
  return SHA256(round1 + round2 + round3).toString();
};

export const validatePassword = (password: string): boolean => {
  const minLength = 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

  return (
    password.length >= minLength &&
    hasUpperCase &&
    hasLowerCase &&
    hasNumbers &&
    hasSpecialChar
  );
};