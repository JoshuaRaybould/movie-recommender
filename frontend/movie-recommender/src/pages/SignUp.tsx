import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { fullFetch } from "../api";
import { TokenSchema } from "../types";
import type { Token } from "../types";
const SignUp = () => {
  const [password, setPassword] = useState<string>("");
  const [username, setUsername] = useState<string>("");

  const navigate = useNavigate();

  async function attemptSignUp() {
    const options = {
      method: "POST",
      headers: new Headers({ "Content-type": "application/json" }),
      body: JSON.stringify({ username: username, password: password }),
    };
    let res;
    try {
      res = await fullFetch<Token>("/signup", options, TokenSchema);
      if (res && res.accessToken) {
        localStorage.setItem("token", res.accessToken);
        navigate(`/movies`);
      }
    } catch (error) {
      console.log(error); // todo
    }
  }

  return (
    <div className="flex-col flex w-full h-screen items-center">
      <h1 className="flex text-4xl mt-10">Movie Recommender</h1>
      <h3 className="flex text-xl mt-5">AI powered movie recommendations</h3>
      <h4 className="flex text-2xl mt-20">Sign up</h4>

      <input
        name="myInput"
        className="flex rounded-xs pl-2 outline-1 h-9 mt-5"
        placeholder="Username"
        onChange={(e) => {
          setUsername(e.target.value);
        }}
      />
      <input
        name="myInput"
        className="flex rounded-xs pl-2 outline-1 h-9 mt-5"
        placeholder="Password"
        onChange={(e) => {
          setPassword(e.target.value);
        }}
      />
      <div className="flex">
        <button
          onClick={attemptSignUp}
          className="rounded-md bg-blue-500 hover:bg-blue-600 text-white font-bold border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 cursor-pointer h-10 mt-3 w-25"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default SignUp;
