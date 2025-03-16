export interface User {
  username: string;
  hash: string;
}

export interface AuthState {
  users: User[];
  currentUser: string | null;
  isAuthenticated: boolean;
}