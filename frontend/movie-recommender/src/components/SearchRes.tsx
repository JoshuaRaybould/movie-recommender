import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios, { type AxiosResponse } from "axios";
import { useDebouncedCallback } from "use-debounce";
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";
import Navbar from "./Navbar";
import Modal from "./Modal";

/*const query = useQuery({
   queryKey: ['all-movies'],
   queryFn: 
})*/

type Movie = {
  movieId: number;
  title: string;
  genres: string;
  tmdbId: number;
  picUrl: string;
  rating: number | null;
};

type results = {
  movies: Array<Movie>;
  token: string;
};

const SearchRes = ({ movies, token }: results) => {
  return (
    <div className="grid grid-cols-4 grid-rows-2 justify-center content-normal gap-3 h-200 w-200">
      {movies.map((item: Movie) => (
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
              token={token}
              movieId={item.movieId}
              movieTitle={item.title}
              prevRating={item.rating}
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
