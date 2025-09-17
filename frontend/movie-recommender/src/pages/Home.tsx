import React from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";

/*const query = useQuery({
   queryKey: ['all-movies'],
   queryFn: 
})*/

type Movie = {
  title: string;
  genres: string;
  imdbId: number;
  tmdbId: number;
};

const response = await axios.get("/api/");

console.log(response.data);

const Home = () => {
  const nav = useNavigate();

  function handleClick() {
    nav("/recommendations");
  }

  function constructor() {}

  return (
    <>
      <div className="grid grid-cols-3 gap-4">
        {response.data.map((item: Movie) => (
          <div key={item.imdbId}>
            <p>
              {item.tmdbId}
              {item.title}
            </p>
          </div>
        ))}
      </div>
    </>
  );
};

export default Home;
