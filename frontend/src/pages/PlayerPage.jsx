import { useParams } from "react-router-dom";

export default function PlayerPage() {
  const { type, id } = useParams();

  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <video
        controls
        autoPlay
        className="w-full h-screen"
      >
        <source
          src="https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
          type="application/x-mpegURL"
        />
      </video>
    </div>
  );
}