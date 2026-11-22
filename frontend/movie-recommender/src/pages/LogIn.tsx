import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../auth/authContext";
import Input from "../components/Input";

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
      <div className="flex-col flex w-full h-screen items-center gap-5">
        <h1 className="flex text-4xl mt-10">NextBestMovie</h1>
        <h3 className="flex text-2xl">AI powered movie recommendations</h3>
        <h4 className="flex text-2xl mt-15">Log in</h4>

        <form
          action={attemptLogIn}
          className="flex flex-col items-center justify-center gap-4 outline-1 p-3 rounded-md"
        >
          <Input
            placeholder="Username"
            onChange={(e) => {
              setUsername(e.target.value);
            }}
          />
          <Input
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
        </form>

        <a className="flex text-blue-500 mt-2" href="/signup">
          Don't have an account? Sign up here
        </a>
      </div>
    </>
  );
};

export default LogIn;
