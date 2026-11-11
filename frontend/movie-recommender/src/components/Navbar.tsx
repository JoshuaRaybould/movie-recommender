import { useState } from "react";
import { useAuth } from "../auth/authContext";
import { Sun, Moon } from "lucide-react";
import { Link } from "react-router-dom";

type navInfo = {
  searchFunc: Function;
};

const NavBar = ({ searchFunc }: navInfo) => {
  const [isDark, setIsDark] = useState(false);
  const { user } = useAuth();

  function toggleDark() {
    document.documentElement.classList.toggle("dark");
    const res = !isDark;
    localStorage.setItem("theme", res ? "dark" : "light");
    setIsDark(res);
  }

  return (
    <nav className="flex justify-between items-center bg-nav-background mb-4 h-16">
      <div className="flex justify-center items-center h-full">
        <Link
          className="text-4xl text-main-gold font-title ml-10"
          to={`/movies`}
        >
          NBMovie
        </Link>
      </div>
      <div className="flex h-full w-full justify-center items-center">
        <input
          className="pl-2 rounded-lg outline-solid outline-1 h-1/2 w-150 bg-main-bg"
          placeholder="Search"
          onChange={(e) => {
            searchFunc(e.target.value);
          }}
        />
      </div>
      <div className="h-full">
        <ul className="flex justify-center items-center h-full">
          <li className="block mr-10">
            <button onClick={toggleDark}>
              {isDark ? (
                <Sun size={30} color="white" />
              ) : (
                <Moon size={25} color="white" />
              )}
            </button>
          </li>
          <li className="block mr-10">
            <Link className="text-white" to={`/movies`}>
              Home
            </Link>
          </li>
          {user ? (
            <li className="block mr-5">
              <Link className="text-white" to={`/recommendations`}>
                Recommendations
              </Link>
            </li>
          ) : (
            <li className="block mr-5">
              <Link className="text-white" to="/">
                Recommendations
              </Link>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;
