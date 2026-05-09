import { useNavigate } from "react-router-dom";

export default function EpisodeCard({
  episode
}) {

  const navigate = useNavigate();

  return (
    <div
      onClick={() =>
        navigate(
          `/watch/episode/${episode.id}`
        )
      }
      className="flex gap-4 bg-zinc-900 hover:bg-zinc-800 transition rounded-2xl overflow-hidden cursor-pointer"
    >

      <img
        src={
          episode.still_path ||
          "https://placehold.co/300x170"
        }
        className="w-52 h-32 object-cover"
      />

      <div className="p-4 flex-1">

        <h3 className="font-bold text-lg">
          Episode {episode.episode_number}
        </h3>

        <h4 className="text-gray-300 mt-1">
          {episode.name}
        </h4>

        <p className="text-sm text-gray-500 mt-2 line-clamp-2">
          {episode.overview}
        </p>

      </div>
    </div>
  );
}