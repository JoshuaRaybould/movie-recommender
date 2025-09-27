import axios from "axios";
import { useState } from "react";
import { FaRegStar, FaStar } from "react-icons/fa";
import { RxCross2 } from "react-icons/rx";

type ratingInfo = {
  token: string;
  movieId: number;
  movieTitle: string;
  prevRating: number | null;
};

const Modal = ({ token, movieId, movieTitle, prevRating }: ratingInfo) => {
  if (prevRating) {
    prevRating = prevRating * 2;
  }
  const [active, setActive] = useState<boolean>(false);
  const [rating, setRating] = useState<number | null>(prevRating);
  const [accRating, setAccRating] = useState<number | null>(prevRating);

  function toggleActive() {
    setRating(accRating);
    setActive(!active);
  }

  async function applyRating() {
    if (rating) {
      setAccRating(rating);
      await axios.post(`/api/rate/${token}/${movieId}/${rating / 2}`);
      setActive(false);
    } else {
      alert("try again");
    }
  }

  async function resetRating() {
    setRating(null);
    await axios.post(`/api/delete/rate/${token}/${movieId}/None`);
    setActive(false);
  }

  return (
    <>
      <div className="flex ml-1 mt-1">
        {accRating ? (
          <p className="font-semibold">{accRating}/10&nbsp;&nbsp;</p>
        ) : (
          <p className="font-semibold">?/10&nbsp;&nbsp;</p>
        )}
        <button
          className="rounded-sm bg-blue-500 hover:bg-blue-600 text-white border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 cursor-pointer w-20"
          onClick={toggleActive}
        >
          <div className="flex items-center justify-center">
            <p>Rate&nbsp;</p>
            <FaRegStar></FaRegStar>
          </div>
        </button>
      </div>
      {active && (
        <div className="fixed h-full w-full right-0 left-0 top-0">
          <div
            onClick={toggleActive}
            className="fixed h-full w-full bg-black opacity-75"
          />

          <div className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
            <div className="flex-col flex items-center w-116 h-66 bg-white rounded-sm">
              <div className="ml-auto mr-2 mt-2">
                <RxCross2
                  onClick={toggleActive}
                  size={25}
                  className="cursor-pointer hover:bg-red-300 rounded-4xl"
                />
              </div>

              <h3 className="flex text-md">Rate</h3>
              <h3 className="text-xl mt-1">{movieTitle}</h3>

              <div className="flex flex-wrap justify-center">
                {[...Array(10)].map((star, i) => (
                  <>
                    <label className="mt-2">
                      <input
                        className="cursor-pointer hidden"
                        type="radio"
                        name="editList"
                        value="always"
                        onClick={() => setRating(i + 1)}
                      />
                      {!rating || i >= rating ? (
                        <FaRegStar
                          className="cursor-pointer opacity-85"
                          color="gold"
                          size={35}
                        ></FaRegStar>
                      ) : (
                        <FaStar
                          className="cursor-pointer opacity-85"
                          color="gold"
                          size={35}
                        ></FaStar>
                      )}
                    </label>
                  </>
                ))}
              </div>

              <div className="flex justify-center h-full">
                {rating ? (
                  <>
                    <p className="text-xl mt-auto mb-auto">{rating}</p>
                  </>
                ) : (
                  <>
                    <p className="text-xl mt-auto mb-auto">?</p>
                  </>
                )}
              </div>

              <span></span>
              <div className="flex justify-center h-full">
                {rating ? (
                  <>
                    <button
                      className="rounded-md mt-auto mb-3 bg-gray-500 hover:bg-gray-600 text-white border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 h-10 w-30 cursor-pointer mr-1"
                      onClick={resetRating}
                    >
                      Reset
                    </button>
                    <button
                      className="rounded-md mt-auto mb-3 bg-blue-500 hover:bg-blue-600 text-white border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 h-10 w-30 cursor-pointer"
                      onClick={applyRating}
                    >
                      Rate
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      className="rounded-md mt-auto mb-3 bg-gray-300 text-white border-1 border-solid focus:outline-none h-10 w-30 mr-1"
                      disabled={true}
                    >
                      Reset
                    </button>
                    <button
                      className="mt-5 mt-auto mb-3 rounded-md bg-blue-300 text-white border-1 border-solid focus:outline-none h-10 w-30"
                      disabled={true}
                    >
                      Rate
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Modal;
