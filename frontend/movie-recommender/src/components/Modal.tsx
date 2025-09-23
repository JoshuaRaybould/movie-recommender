import { useState } from "react";
import { FaRegStar, FaStar } from "react-icons/fa";
import { RxCross2 } from "react-icons/rx";

type ratingInfo = {
  movieId: number;
  movieTitle: string;
  prevRating: number | null;
};

const Modal = ({ movieId, movieTitle, prevRating }: ratingInfo) => {
  const [active, setActive] = useState<boolean>(false);
  const [rating, setRating] = useState<number | null>(prevRating);

  function toggleActive() {
    setActive(!active);
  }

  return (
    <>
      <div>
        {rating ? (
          <p className="inline">{rating}/5 </p>
        ) : (
          <p className="font-semibold inline">?/10 </p>
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
        <>
          <div className="fixed h-full w-full right-0 left-0 top-0">
            <div
              onClick={toggleActive}
              className="fixed h-full w-full right-0 left-0 top-0 bg-black opacity-75"
            ></div>
            <div className="flex-col h-full w-full">
              <div className="relative top-3/9 w-105 h-60 ml-auto mr-auto items-center justify-center bg-white">
                <div>
                  <RxCross2
                    onClick={toggleActive}
                    size={30}
                    className="cursor-pointer ml-auto hover:bg-red-300 rounded-4xl"
                  ></RxCross2>
                  <h3 className="text-xl">Rate</h3>
                  <h3 className="text-2xl mt-1">{movieTitle}</h3>
                </div>

                <div className="flex flex-wrap items-center justify-center">
                  {[...Array(10)].map((star, i) => (
                    <>
                      <label className="mt-2">
                        <input
                          className="cursor-pointer hidden"
                          type="radio"
                          name="editList"
                          value="always"
                        />
                        <FaStar
                          className="cursor-pointer opacity-85"
                          color="gold"
                          size={35}
                        ></FaStar>
                      </label>
                    </>
                  ))}
                </div>
                <button
                  className="mt-5 rounded-md bg-blue-500 hover:bg-blue-600 text-white border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 h-10 w-30 cursor-pointer"
                  onClick={toggleActive}
                >
                  Rate
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
};

export default Modal;
