import {
  useEffect,
  useState
} from "react";

import {
  useParams,
  useNavigate
} from "react-router-dom";

import api from "../api/axios";
import Loader from "../components/Loader";
import EpisodeCard from "../components/EpisodeCard";
import SeasonDropdown from "../components/SeasonDropdown";
import BackButton from "../components/BackButton";

export default function DetailPage() {

  const { type, id } = useParams();

  const navigate = useNavigate();

  const [loading, setLoading] =
    useState(true);

  const [data, setData] =
    useState(null);

  const [selectedSeason,
    setSelectedSeason] =
      useState(null);

  useEffect(() => {
    loadData();
  }, [id, type]);

  const loadData = async () => {

    setLoading(true);

    try {

      const endpoint =
        type === "movie"
          ? `/content/movies/${id}/`
          : `/content/series/${id}/`;

      const response =
        await api.get(endpoint);

      setData(response.data);

      if (
        response.data.seasons?.length
      ) {

        setSelectedSeason(
          response.data.seasons[0]
            .season_number
        );
      }

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);
    }
  };

  if (loading) return <Loader />;

  const currentSeason =
    data?.seasons?.find(
      s =>
        s.season_number ==
        selectedSeason
    );

  return (
    <div className="bg-black text-white min-h-screen">

      {/* HERO SECTION */}
      

      <div
        className="relative h-[95vh] bg-cover bg-center"
        style={{
          backgroundImage:
            `url(${data.backdrop_path})`
        }}
      >
        <div className="absolute top-6 left-6 z-20">
          <BackButton to="/" label="Back to Home" />
        </div>

        {/* overlays */}
        <div className="absolute inset-0 bg-gradient-to-r from-black via-black/85 to-black/30" />

        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black/40" />

        {/* content */}
        <div className="relative z-10 h-full flex items-end px-6 md:px-20 pb-16">

          <div className="max-w-4xl">

            {/* title */}
            <h1 className="text-5xl md:text-7xl font-black leading-tight">
              {data.title || data.name}
            </h1>

            {/* metadata */}
            <div className="flex flex-wrap items-center gap-4 mt-6 text-sm md:text-base">

              {data.release_date && (
                <span className="bg-white/10 px-3 py-1 rounded-full">
                  {new Date(
                    data.release_date
                  ).getFullYear()}
                </span>
              )}

              {data.runtime && (
                <span className="bg-white/10 px-3 py-1 rounded-full">
                  {Math.floor(data.runtime / 60)}h{" "}
                  {data.runtime % 60}m
                </span>
              )}

              {data.vote_average && (
                <span className="bg-yellow-500/20 text-yellow-400 px-3 py-1 rounded-full">
                  ⭐ {data.vote_average}
                </span>
              )}

              {data.status && (
                <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full">
                  {data.status}
                </span>
              )}

            </div>

            {/* genres */}
            {data.genres?.length > 0 && (

              <div className="flex flex-wrap gap-3 mt-6">

                {data.genres.map((genre) => (

                  <span
                    key={genre.id}
                    className="bg-red-600/20 border border-red-500/30 text-red-300 px-4 py-1 rounded-full text-sm"
                  >
                    {genre.name}
                  </span>

                ))}

              </div>

            )}

            {/* overview */}
            <p className="text-gray-300 text-lg leading-relaxed mt-8 max-w-3xl">
              {data.overview}
            </p>

            {/* buttons */}
            <div className="flex flex-wrap gap-4 mt-10">

              <button
                onClick={() => {

                  if (type === "movie") {

                    navigate(
                      `/watch/movie/${id}`
                    );

                  } else {

                    const firstEpisode =
                      currentSeason
                        ?.episodes?.[0];

                    if (firstEpisode) {

                      navigate(
                        `/watch/episode/${firstEpisode.id}`
                      );
                    }
                  }
                }}
                className="bg-white text-black px-8 py-4 rounded-2xl font-bold text-lg hover:bg-gray-200 transition flex items-center gap-3"
              >
                ▶ Play Now
              </button>

              <button
                className="bg-white/10 backdrop-blur-md border border-white/20 px-8 py-4 rounded-2xl font-semibold hover:bg-white/20 transition"
              >
                + My List
              </button>

            </div>

          </div>
        </div>
      </div>

      {/* DETAILS */}
      <div className="px-6 md:px-20 py-14">

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">

          {/* LEFT */}
          <div className="lg:col-span-2">

            {/* STORY */}
            <div className="bg-zinc-900 rounded-3xl p-8 border border-white/5">

              <h2 className="text-3xl font-bold mb-6">
                Storyline
              </h2>

              <p className="text-gray-300 leading-loose text-lg">
                {data.overview}
              </p>

            </div>

            {/* SERIES */}
            {type === "series" && (

              <div className="mt-12">

                <div className="flex items-center justify-between mb-8">

                  <h2 className="text-3xl font-bold">
                    Episodes
                  </h2>

                  <SeasonDropdown
                    seasons={data.seasons}
                    selected={selectedSeason}
                    onChange={setSelectedSeason}
                  />

                </div>

                <div className="space-y-5">

                  {currentSeason?.episodes?.map(
                    (episode) => (

                      <EpisodeCard
                        key={episode.id}
                        episode={episode}
                      />

                    )
                  )}

                </div>

              </div>
            )}

          </div>

          {/* RIGHT SIDEBAR */}
          <div className="space-y-8">

            {/* poster */}
            <div className="bg-zinc-900 rounded-3xl overflow-hidden border border-white/5">

              <img
                src={data.poster_path}
                alt={data.title}
                className="w-full object-cover"
              />

            </div>

            {/* info */}
            <div className="bg-zinc-900 rounded-3xl p-8 border border-white/5">

              <h3 className="text-2xl font-bold mb-6">
                Details
              </h3>

              <div className="space-y-5 text-gray-300">

                {data.original_language && (
                  <div>
                    <p className="text-gray-500 text-sm">
                      Language
                    </p>

                    <p className="mt-1 uppercase">
                      {data.original_language}
                    </p>
                  </div>
                )}

                {data.release_date && (
                  <div>
                    <p className="text-gray-500 text-sm">
                      Release Date
                    </p>

                    <p className="mt-1">
                      {data.release_date}
                    </p>
                  </div>
                )}

                {data.number_of_seasons && (
                  <div>
                    <p className="text-gray-500 text-sm">
                      Seasons
                    </p>

                    <p className="mt-1">
                      {data.number_of_seasons}
                    </p>
                  </div>
                )}

                {data.number_of_episodes && (
                  <div>
                    <p className="text-gray-500 text-sm">
                      Episodes
                    </p>

                    <p className="mt-1">
                      {data.number_of_episodes}
                    </p>
                  </div>
                )}

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}