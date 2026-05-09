import { useEffect, useState } from "react";
import api from "../api/axios";

import Navbar from "../components/Navbar";
import SectionRow from "../components/SectionRow";
import Loader from "../components/Loader";

export default function HomePage() {
  const [loading, setLoading] = useState(true);

  const [trendingMovies, setTrendingMovies] = useState([]);
  const [popularMovies, setPopularMovies] = useState([]);
  const [tvSeries, setTvSeries] = useState([]);
  const [featuredMovie, setFeaturedMovie] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [trendingRes, moviesRes, seriesRes] =
        await Promise.all([
          api.get("/content/movies/trending/"),
          api.get("/content/movies/"),
          api.get("/content/series/"),
        ]);

      setTrendingMovies(trendingRes.data);
      setPopularMovies(moviesRes.data.results || []);
      setTvSeries(seriesRes.data.results || []);

      setFeaturedMovie(trendingRes.data?.[0]);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className="min-h-screen bg-black text-white">
      <Navbar />

      {/* Hero */}
      <section
        className="relative h-[90vh] bg-cover bg-center flex items-center"
        style={{
          backgroundImage: `url(${featuredMovie?.backdrop_path})`,
        }}
      >
        <div className="absolute inset-0 bg-black/70"></div>

        <div className="relative z-10 px-8 md:px-16 max-w-2xl">
          <h1 className="text-6xl font-black">
            {featuredMovie?.title}
          </h1>

          <p className="text-gray-300 mt-6">
            {featuredMovie?.overview}
          </p>
        </div>
      </section>

      <main className="px-6 md:px-12 py-10 space-y-12">
        <SectionRow
          title="Trending Now"
          items={trendingMovies}
          type="movie"
        />

        <SectionRow
          title="Popular Movies"
          items={popularMovies}
          type="movie"
        />

        <SectionRow
          title="TV Series"
          items={tvSeries}
          type="series"
        />
      </main>
    </div>
  );
}