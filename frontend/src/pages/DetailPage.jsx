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

import EpisodeCard
  from "../components/EpisodeCard";

import SeasonDropdown
  from "../components/SeasonDropdown";

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

      {/* Banner */}
      <div
        className="h-[80vh] bg-cover bg-center relative"
        style={{
          backgroundImage:
            `url(${data.backdrop_path})`
        }}
      >

        <div className="absolute inset-0 bg-gradient-to-r from-black via-black/80 to-transparent" />

        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black/20" />

        <div className="relative z-10 px-10 md:px-20 flex flex-col justify-end h-full pb-20 max-w-3xl">

          <h1 className="text-6xl font-black">
            {data.title || data.name}
          </h1>

          <p className="text-gray-300 mt-6 leading-relaxed">
            {data.overview}
          </p>

          <div className="flex gap-4 mt-8">

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
              className="bg-white text-black px-8 py-3 rounded-xl font-bold hover:bg-gray-200 transition"
            >
              ▶ Play
            </button>

          </div>
        </div>
      </div>

      {/* TV SERIES */}
      {type === "series" && (

        <div className="px-6 md:px-16 py-12">

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
              episode => (

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
  );
}