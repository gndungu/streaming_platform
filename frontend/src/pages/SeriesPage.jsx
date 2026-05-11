import { useEffect, useState }
  from "react";

import axios from "axios";

import Navbar
  from "../components/Navbar";

import MovieCard
  from "../components/MovieCard";

import LoadingScreen
  from "../components/Loader";

const API_BASE =
  "http://127.0.0.1:8000/api/content";

export default function SeriesPage() {

  const [series, setSeries] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    fetchSeries();
  }, []);

  const fetchSeries = async () => {

    try {

      const response =
        await axios.get(
          `${API_BASE}/series/`
        );

      setSeries(
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

        <div className="mb-8">

          <h1 className="text-4xl font-black">
            TV Series
          </h1>

          <p className="text-gray-400 mt-2">
            Browse all TV series
          </p>

        </div>

        {
          series.length === 0 ? (

            <div className="
              text-center
              py-20
              text-gray-400
            ">
              No TV series found
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

              {series.map((item) => (

                <MovieCard
                  key={item.id}
                  item={item}
                  type="series"
                />

              ))}

            </div>

          )
        }

      </div>

    </div>
  );
}