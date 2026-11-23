import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../auth/authContext";
import Input from "../components/Input";
import PasswordInput from "../components/PasswordInput";

const LogIn = () => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const { login } = useAuth();
  const navigate = useNavigate();

  async function attemptLogIn() {
    try {
      await login(username, password);
      navigate("/movies");
    } catch (error) {
      console.log(error); // todo, check what we want to do here
    }
  }

  return (
    <>
      <title>Log In | NextBestMovie</title>
      <div className="flex-col flex w-full h-screen items-center justify-center">
        <form
          action={attemptLogIn}
          className="flex flex-col items-center justify-center gap-5 outline-2 outline-gray-400 p-12 rounded-md bg-gray-100 mb-20"
        >
          <h1 className="flex text-4xl">NextBestMovie</h1>{" "}
          <h3 className="flex text-xl">AI powered movie recommendations</h3>
          <h4 className="flex text-2xl">Log In</h4>
          <Input
            placeholder="Username"
            onChange={(e) => {
              setUsername(e.target.value);
            }}
          />
          <PasswordInput
            placeholder="Password"
            onChange={(e) => {
              setPassword(e.target.value);
            }}
          />
          <div className="flex">
            <button
              type="submit"
              className="rounded-md bg-blue-500 hover:bg-blue-600 text-white font-bold border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 cursor-pointer h-10 w-35"
            >
              Next
            </button>
          </div>
          <p>
            Don't have an account?&nbsp;
            <Link className="text-blue-500" to="/signup">
              Sign up
            </Link>
          </p>
        </form>
      </div>
    </>
  );
};

export default LogIn;
