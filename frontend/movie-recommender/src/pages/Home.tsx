import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useDebouncedCallback } from "use-debounce";
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";
import Navbar from "../components/Navbar";
import Modal from "../components/Modal";
import SearchRes from "../components/SearchRes";
import { fullFetch } from "../api";
import { MovieSchema } from "../types";
import type { Movie } from "../types";
import { Spinner } from "../components/Spinner";
/*const query = useQuery({
   queryKey: ['all-movies'],
   queryFn: 
})*/

const Home = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const debounced = useDebouncedCallback((value) => {
    setSearchTerm(value);
  }, 700);
  const [movies, setMovies] = useState<Movie[]>([]);

  async function getData() {
    setIsLoading(true);
    try {
      let movies;
      if (searchTerm) {
        movies = await fullFetch(
          `/movies/{searchTerm}`,
          {},
          MovieSchema.array(),
        );
      } else {
        movies = await fullFetch("/movies", {}, MovieSchema.array());
      }
      setMovies(movies);
    } catch (error) {
      console.log(error); // todo
    }

    setIsLoading(false);
  }

  useEffect(() => {
    getData();
  }, [searchTerm]);

  return (
    <>
      <Navbar searchFunc={debounced} />

      <div className="w-full flex h-full justify-center">
        {isLoading ? (
          <div className="w-full flex h-200 items-center justify-center">
            <Spinner />
          </div>
        ) : (
          <SearchRes movies={movies}></SearchRes>
        )}
      </div>
    </>
  );
};

export default Home;
