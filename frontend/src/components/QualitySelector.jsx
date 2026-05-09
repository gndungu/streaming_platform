export default function QualitySelector({
  sources,
  current,
  onSelect
}) {

  return (
    <div className="flex gap-3 flex-wrap mt-6">

      {sources?.map((source) => (

        <button
          key={source.id}
          onClick={() => onSelect(source)}
          className={`px-4 py-2 rounded-xl transition font-semibold ${
            current?.id === source.id
              ? "bg-red-600"
              : "bg-zinc-800 hover:bg-zinc-700"
          }`}
        >
          {source.quality}
        </button>

      ))}

    </div>
  );
}