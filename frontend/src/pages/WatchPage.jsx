import {
  useEffect,
  useState
} from "react";

import {
  useParams
} from "react-router-dom";

import api from "../api/axios";

import Loader from "../components/Loader";

import VideoPlayer
  from "../components/VideoPlayer";
import HLSPlayer from "../components/HLSPlayer"

import QualitySelector
  from "../components/QualitySelector";

export default function WatchPage() {

  const { type, id } = useParams();

  const [loading, setLoading] =
    useState(true);

  const [data, setData] =
    useState(null);

  const [selectedSource,
    setSelectedSource] =
      useState(null);

  useEffect(() => {
    loadData();
  }, [id, type]);

  const loadData = async () => {

    try {

      const endpoint =
        type === "movie"
          ? `/stream/movies/${id}/`
          : `/stream/episodes/${id}/`;

      const response =
        await api.get(endpoint);

      setData(response.data);

      if (
        response.data.video_sources
          ?.length
      ) {

        setSelectedSource(
          response.data.video_sources[0]
        );
      }

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className="min-h-screen bg-black text-white">

      <div className="max-w-7xl mx-auto px-6 py-8">

        <HLSPlayer
          source={selectedSource}
        />

        <div className="mt-8">

          <h1 className="text-4xl font-black">
            {data.title || data.name}
          </h1>

          <p className="text-gray-400 mt-4 max-w-4xl leading-relaxed">
            {data.overview}
          </p>

        </div>

        <QualitySelector
          sources={data.video_sources}
          current={selectedSource}
          onSelect={setSelectedSource}
        />

      </div>
    </div>
  );
}