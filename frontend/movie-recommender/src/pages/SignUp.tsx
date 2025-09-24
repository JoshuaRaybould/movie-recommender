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
    <div className="w-full h-full">
      <h1 className="relative bottom-50">Movie Recommender</h1>
      <h3 className="relative bottom-40 text-2xl mt-1">
        AI powered movie recommendations
      </h3>
      <h4 className="relative bottom-30 text-2xl mt-1">Sign up</h4>

      <div className="relative bottom-25 mt-1 mb-2">
        <input
          name="myInput"
          className="rounded-xs outline-1 h-9 mt-1 mb-1"
          placeholder=" Enter name"
          onChange={(e) => {
            setToken(e.target.value);
          }}
        />
        <p className="text-sm">This will be used to sign in</p>
        <p className="text-sm">So don't forget it!</p>
        <button
          onClick={attemptSignUp}
          className="rounded-md bg-blue-500 hover:bg-blue-600 text-white font-bold border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 cursor-pointer h-10 mt-1 mb-2 w-25"
        >
          Next
        </button>
      </div>
      {isDuplicate && (
        <p className="relative bottom-25 text-red-500 mb-1">
          Account already exists
        </p>
      )}
      <a className="relative bottom-25 text-blue-500" href="/">
        Have an account? Sign in here
      </a>
    </div>
  );
};

export default SignUp;
