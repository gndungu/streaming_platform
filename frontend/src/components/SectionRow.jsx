import MovieCard from "./MovieCard";

export default function SectionRow({
  title,
  items,
  type,
}) {
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-2xl font-bold">
          {title}
        </h3>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {items.map((item) => (
          <MovieCard
            key={item.id}
            item={item}
            type={type}
          />
        ))}
      </div>
    </div>
  );
}