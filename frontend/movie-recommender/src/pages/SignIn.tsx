import axios from "axios";
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

const SignIn = () => {
  const [token, setToken] = useState<string>("");
  const [failSignIn, setFailSignIn] = useState<boolean>(false);

  const navigate = useNavigate();

  async function attemptSignIn() {
    if (token.length) {
      var res = await axios.get("/api/signin/" + token).catch(function () {
        setFailSignIn(true);
        return;
      });
      if (res && res.data) {
        console.log(res.data);
        navigate(`/${token}`);
      } else {
        setFailSignIn(true);
      }
    }
  }

  return (
    <div className="flex-col flex w-full h-screen items-center">
      <h1 className="flex text-4xl mt-10">Movie Recommender</h1>
      <h3 className="flex text-2xl mt-5">AI powered movie recommendations</h3>
      <h4 className="flex text-2xl mt-20">Sign in</h4>

      <input
        name="myInput"
        className="flex rounded-xs pl-2 outline-1 h-9 mt-3"
        placeholder="Enter name"
        onChange={(e) => {
          setToken(e.target.value);
        }}
      />

      <div className="flex">
        <button
          onClick={attemptSignIn}
          className="rounded-md bg-blue-500 hover:bg-blue-600 text-white font-bold border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 cursor-pointer h-10 mt-3 w-35"
        >
          Next
        </button>
      </div>

      {failSignIn && (
        <p className="flex text-red-500 mt-2">No account with that name</p>
      )}
      <a className="flex text-blue-500 mt-2" href="/signup">
        Don't have an account? Sign up here
      </a>
    </div>
  );
};

export default SignIn;
