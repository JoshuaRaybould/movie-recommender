import "./App.css";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Recommendations from "./pages/Recommendations";
import LogIn from "./pages/LogIn";
import SignUp from "./pages/SignUp";
import { AuthProvider } from "./auth/authContext";

function App() {
  return (
    <>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<LogIn />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/movies" element={<Home />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Routes>
      </AuthProvider>
    </>
  );
}

export default App;
