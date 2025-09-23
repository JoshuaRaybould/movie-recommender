import "./App.css";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Recommendations from "./pages/Recommendations";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<SignIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/:userToken" element={<Home />} />
        <Route
          path="/:userToken/recommendations"
          element={<Recommendations />}
        />
      </Routes>
    </>
  );
}

export default App;
