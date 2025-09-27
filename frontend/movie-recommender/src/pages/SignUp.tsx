import axios from "axios";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const SignUp = () => {
  const [token, setToken] = useState<string>("");
  const [isDuplicate, setIsDuplicate] = useState<boolean>(false);

  const navigate = useNavigate();

  async function attemptSignUp() {
    if (token.length) {
      var res = await axios.post("/api/signup/" + token).catch(function () {
        setIsDuplicate(true);
        return;
      });
      if (res && res.data) {
        navigate(`/${token}`);
      }
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
        placeholder="Enter name"
        onChange={(e) => {
          setToken(e.target.value);
        }}
      />

      <p className="flex text-sm mt-1">This will be used to sign in</p>
      <p className="flex text-sm">So don't forget it!</p>
      <div className="flex">
        <button
          onClick={attemptSignUp}
          className="rounded-md bg-blue-500 hover:bg-blue-600 text-white font-bold border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 cursor-pointer h-10 mt-3 w-25"
        >
          Next
        </button>
      </div>

      {isDuplicate && (
        <p className="flex text-red-500 mt-1">Account already exists</p>
      )}
      <a className="flex text-blue-500 mt-1" href="/">
        Have an account? Sign in here
      </a>
    </div>
  );
};

export default SignUp;
