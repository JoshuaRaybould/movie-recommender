import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";
import { fullFetch } from "../api";
import { TokenSchema, UserSchema, type Token, type User } from "../types";
import { Spinner } from "../components/Spinner";
const AuthContext = createContext<AuthInformation | null>(null);

interface AuthInformation {
  user: User | null;
  signup: (username: string, password: string) => Promise<void>;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const signup = async (username: string, password: string) => {
    const options = {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify({ username: username, password: password }),
    };

    const res = await fullFetch<Token>("/signup", options, TokenSchema);
    localStorage.setItem("token", res.accessToken);

    const user = await fullFetch<User>("/users/me", {}, UserSchema);
    setUser(user);
  };

  const login = async (username: string, password: string) => {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    const options = {
      method: "POST",
      body: formData,
    };

    const token = await fullFetch<Token>("/token", options, TokenSchema);
    localStorage.setItem("token", token.accessToken);

    const userRes = await fullFetch<User>("/users/me", {}, UserSchema);
    setUser(userRes);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("token");
  };

  useEffect(() => {
    async function restoreSession() {
      const token = localStorage.getItem("token");
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const userRes = await fullFetch<User>("/users/me", {}, UserSchema);
        setUser(userRes);
      } catch {
        localStorage.removeItem("token");
      } finally {
        setLoading(false);
      }
    }

    restoreSession();
  }, []);

  return loading ? (
    <div className="w-full flex h-200 items-center justify-center">
      <Spinner />
    </div>
  ) : (
    <AuthContext value={{ user, signup, login, logout }}>
      {children}
    </AuthContext>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
