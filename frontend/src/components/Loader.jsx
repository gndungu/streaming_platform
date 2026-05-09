export default function Loader() {
  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center text-white">
      <div className="w-16 h-16 border-4 border-zinc-700 border-t-red-600 rounded-full animate-spin"></div>

      <p className="mt-4 text-gray-400 text-sm">
        Loading content...
      </p>
    </div>
  );
}