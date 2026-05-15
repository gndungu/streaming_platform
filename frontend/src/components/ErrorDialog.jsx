export default function ErrorDialog({ message, onClose }) {
  if (!message) return null;

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">

      <div className="bg-gray-900 p-6 rounded-lg w-80 text-white shadow-xl">

        <h2 className="text-xl font-bold text-red-500 mb-3">
          Error
        </h2>

        <p className="text-gray-300 mb-5">
          {message}
        </p>

        <button
          onClick={onClose}
          className="w-full bg-red-600 hover:bg-red-700 p-2 rounded"
        >
          Close
        </button>

      </div>

    </div>
  );
}