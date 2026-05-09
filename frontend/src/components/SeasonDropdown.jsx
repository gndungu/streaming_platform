export default function SeasonDropdown({
  seasons,
  selected,
  onChange
}) {

  return (
    <select
      value={selected}
      onChange={(e) =>
        onChange(e.target.value)
      }
      className="bg-zinc-900 border border-zinc-700 px-4 py-3 rounded-xl text-white"
    >

      {seasons?.map((season) => (

        <option
          key={season.id}
          value={season.season_number}
        >
          Season {season.season_number}
        </option>

      ))}

    </select>
  );
}