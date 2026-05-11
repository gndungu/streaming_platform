import { useEffect, useState } from "react";

import axios from "axios";

import Navbar from "../components/Navbar";
import MovieCard from "../components/MovieCard";
import LoadingScreen from "../components/Loader";

const API_BASE =
  "http://127.0.0.1:8000/api/content";

export default function MoviesPage() {

  const [movies, setMovies] = useState([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    fetchMovies();
  }, []);

  const fetchMovies = async () => {

    try {

      const response =
        await axios.get(
          `${API_BASE}/movies/`
        );

      setMovies(
        response.data.results ||
        response.data
      );

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingScreen />;
  }

  return (

    <div className="min-h-screen bg-black text-white">

      <Navbar />

      <div className="pt-28 px-6 md:px-12 pb-20">

        <div className="flex items-center justify-between mb-8">

          <div>

            <h1 className="text-4xl font-black">
              Movies
            </h1>

            <p className="text-gray-400 mt-2">
              Browse all movies
            </p>

          </div>

        </div>

        {
          movies.length === 0 ? (

            <div className="text-center py-20 text-gray-400">
              No movies found
            </div>

          ) : (

            <div className="
              grid
              grid-cols-2
              sm:grid-cols-3
              md:grid-cols-4
              lg:grid-cols-6
              gap-5
            ">

              {movies.map((movie) => (

                <MovieCard
                  key={movie.id}
                  item={movie}
                  type="movie"
                />

              ))}

            </div>

          )
        }

      </div>

    </div>
  );
}