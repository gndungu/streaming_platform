import { Link } from "react-router-dom";

export default function MovieCard({ item, type }) {
  return (
    <Link
      to={`/${type}/${item.id}`}
      className="group relative overflow-hidden rounded-2xl bg-zinc-900 shadow-lg hover:scale-105 transition duration-300"
    >
      <img
        src={
          item.poster_path ||
          "https://placehold.co/500x750?text=No+Image"
        }
        alt={item.title || item.name}
        className="w-full h-72 object-cover"
      />

      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition duration-300 flex flex-col justify-end p-4">
        <h4 className="font-semibold text-lg line-clamp-1">
          {item.title || item.name}
        </h4>

        <div className="flex items-center gap-2 mt-3 text-xs text-gray-300">
          <span className="text-green-400 font-semibold">
            ⭐ {item.vote_average || 0}/10
          </span>

          <span>
            {item.release_date || item.first_air_date}
          </span>
        </div>
      </div>
    </Link>
  );
}