import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useDebouncedCallback } from "use-debounce";
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";
import Navbar from "./Navbar";
import Modal from "./Modal";
import type { MovieAndReview } from "../types";

/*const query = useQuery({
   queryKey: ['all-movies'],
   queryFn: 
})*/

const SearchRes = ({ movies }: { movies: MovieAndReview[] }) => {
  return (
    <div className="grid grid-cols-4 grid-rows-2 justify-center content-normal gap-3 h-200 w-200">
      {movies.map((item: MovieAndReview) => (
        <div
          className="rounded-sm bottom-0 bg-gray-300 overflow-hidden"
          key={item.movieId}
        >
          <img
            className="rounded-sm ml-auto mr-auto"
            src={`https://image.tmdb.org/t/p/w200${item.picUrl}`}
          />
          <div>
            <Modal
              movieId={item.movieId}
              movieTitle={item.title}
              prevRating={item.review && item.review.rating}
            ></Modal>
          </div>
          <span className="block w-46 overflow-hidden text-ellipsis text-wrap break-normal ml-1">
            {item.title}
          </span>
        </div>
      ))}
    </div>
  );
};

export default SearchRes;
