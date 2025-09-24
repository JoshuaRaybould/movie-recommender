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
    <div className="w-full h-full">
      <h1 className="relative bottom-50">Movie Recommender</h1>
      <h3 className="relative bottom-40 text-2xl mt-1">
        AI powered movie recommendations
      </h3>
      <h4 className="relative bottom-30 text-2xl mt-1">Sign in</h4>
      <div className="relative bottom-25 mt-1 mb-2">
        <input
          name="myInput"
          className="rounded-xs outline-1 h-9 mt-1 mb-1"
          placeholder=" Enter name"
          onChange={(e) => {
            setToken(e.target.value);
          }}
        />
      </div>
      <div className="relative bottom-25">
        <button
          onClick={attemptSignIn}
          className="rounded-md bg-blue-500 hover:bg-blue-600 text-white font-bold border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 cursor-pointer h-10 mt-1 mb-2 w-35"
        >
          Next
        </button>
      </div>
      {failSignIn && (
        <p className="relative bottom-25 text-red-500 mb-1">
          No account with that name
        </p>
      )}
      <a className="relative bottom-25 text-blue-500" href="/signup">
        Don't have an account? Sign up here
      </a>
    </div>
  );
};

export default SignIn;
