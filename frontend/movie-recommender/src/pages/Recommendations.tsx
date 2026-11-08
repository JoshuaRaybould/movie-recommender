import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDebouncedCallback } from "use-debounce";

import Navbar from "../components/Navbar";
import Modal from "../components/Modal";
import SearchRes from "../components/SearchRes";
import { fullFetch } from "../api";
import {
  MovieAndReviewSchema,
  RecommendedMovieSchema,
  type MovieAndReview,
  type RecommendedMovie,
} from "../types";
import { useAuth } from "../auth/authContext";

/*const query = useQuery({
   queryKey: ['all-movies'],
   queryFn: 
})*/

function Loading() {
  return (
    <svg
      aria-hidden="true"
      className="inline w-20 h-20 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
      viewBox="0 0 100 101"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
        fill="currentColor"
      />
      <path
        d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
        fill="currentFill"
      />
    </svg>
  );
}

const Recommendations = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const debounced = useDebouncedCallback((value) => {
    setSearchTerm(value);
  }, 700);
  const [reccomendedMovies, setRecommendedMovie] = useState<RecommendedMovie[]>(
    [],
  );
  const [searchedMovies, setSearchedMovies] = useState<MovieAndReview[]>([]);
  const [modelTrained, setModelTrained] = useState<boolean>(false);
  const { user } = useAuth();

  const navigate = useNavigate();

  async function trainModel() {
    setIsLoading(true);
    /*const options = { method: "POST" };
    await apiFetch("/train", options);
    */

    let movies;
    try {
      movies = await fullFetch(
        "/recommendation",
        {},
        RecommendedMovieSchema.array(),
      );
      setRecommendedMovie(movies);
    } catch (error) {
      console.log(error); // todo
    }
    setModelTrained(true);
    setIsLoading(false);
  }

  async function getData() {
    setIsLoading(true);
    try {
      let movies;
      if (searchTerm) {
        movies = await fullFetch(
          "/movies/" + searchTerm,
          {},
          MovieAndReviewSchema.array(),
        );
        setSearchedMovies(movies);
      } else {
        movies = await fullFetch(
          "/recommendation",
          {},
          RecommendedMovieSchema.array(),
        );
        setRecommendedMovie(movies);
      }
    } catch (error) {
      console.log(error); // todo
    }

    setIsLoading(false);
  }

  useEffect(() => {
    if (searchTerm) {
      getData();
    }
  }, [searchTerm]);

  useEffect(() => {
    if (user) {
      if (!modelTrained) {
        trainModel();
      } else {
        getData();
      }
    } else {
      navigate("/");
    }
  }, []);

  if (searchTerm) {
    return (
      <>
        <Navbar searchFunc={debounced} />

        <div className="w-full flex h-full items-center justify-center">
          {isLoading ? (
            <div className="w-full flex h-200 items-center justify-center">
              <Loading />
            </div>
          ) : (
            <SearchRes movies={searchedMovies}></SearchRes>
          )}
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar searchFunc={debounced} />

      <div className="w-full flex h-full items-center justify-center">
        {isLoading ? (
          <div className="w-full flex h-200 items-center justify-center">
            <Loading />
          </div>
        ) : (
          <div className="flex items-center justify-center">
            {reccomendedMovies.map((movie: RecommendedMovie) => (
              <div className="flex-col flex">
                <div
                  className="rounded-sm bottom-0 bg-gray-300 overflow-hidden outline-2 outline-gray-300"
                  key={movie.movieId}
                >
                  <h2 className="block w-90 text-xl overflow-hidden text-ellipsis text-wrap break-normal mt-2 mb-2 ml-1">
                    {movie.title}
                  </h2>
                  <img
                    className="rounded-sm"
                    src={`https://image.tmdb.org/t/p/w400${movie.picUrl}`}
                  />
                  <div>
                    <Modal
                      movieId={movie.movieId}
                      movieTitle={movie.title}
                      prevRating={null}
                    ></Modal>
                  </div>
                </div>
                <div className="flex items-center justify-center mt-3 bg-blue-200">
                  <details className="flex items-center justify-center mt-1 mb-1">
                    <summary className="text-xl">Expected Rating</summary>
                    <p className="flex justify-center text-4xl font-semibold">
                      {movie.expectedScore.toFixed(2)}
                    </p>
                  </details>
                </div>
                <button
                  className="rounded-md mt-3 bg-blue-500 hover:bg-blue-600 text-white border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 h-15 w-100 cursor-pointer text-lg"
                  onClick={getData}
                >
                  New Recommendation
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default Recommendations;
