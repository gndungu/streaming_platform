import { useEffect, useRef, useState } from "react";
import Hls from "hls.js";
import BackButton from "../components/BackButton";

export default function VideoPlayer({ source }) {
  const videoRef = useRef(null);
  const containerRef = useRef(null);

  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [showControls, setShowControls] = useState(true);

  if (!source) return null;

  const src = source.is_hls
    ? source.master_playlist_url
    : source.file;

  // 🎬 HLS setup
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    if (source.is_hls && Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource(src);
      hls.attachMedia(video);

      return () => hls.destroy();
    } else {
      video.src = src;
    }
  }, [src]);

  // ▶ Play / Pause
  const togglePlay = () => {
    const video = videoRef.current;

    if (video.paused) {
      video.play();
      setIsPlaying(true);
    } else {
      video.pause();
      setIsPlaying(false);
    }
  };

  // ⏱ Update time
  const handleTimeUpdate = () => {
    const video = videoRef.current;

    setCurrentTime(video.currentTime);
    setDuration(video.duration || 0);

    setProgress((video.currentTime / video.duration) * 100);
  };

  // ⏩ Seek
  const handleSeek = (e) => {
    const video = videoRef.current;
    const value = e.target.value;

    video.currentTime = (value / 100) * video.duration;
    setProgress(value);
  };

  // ⛶ Fullscreen
  const toggleFullscreen = () => {
    const el = containerRef.current;
    if (el.requestFullscreen) el.requestFullscreen();
  };

  // ⏱ format HH:MM:SS
  const formatTime = (time) => {
    if (!time || isNaN(time)) return "00:00:00";

    const hours = Math.floor(time / 3600);
    const minutes = Math.floor((time % 3600) / 60);
    const seconds = Math.floor(time % 60);

    return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(
      2,
      "0"
    )}:${String(seconds).padStart(2, "0")}`;
  };

  return (
    <div
      ref={containerRef}
      className="relative w-full bg-black rounded-2xl overflow-hidden group"
      onMouseMove={() => setShowControls(true)}
    >
      <div className="absolute top-6 left-6 z-20">
              <BackButton to="/" label="Back to Home" />
          </div>
      {/* VIDEO */}
      <video
        ref={videoRef}
        className="w-full h-[75vh] bg-black"
        onTimeUpdate={handleTimeUpdate}
        onClick={togglePlay}
      />

      {/* CENTER PLAY BUTTON */}
      {!isPlaying && (
        <div
          className="absolute inset-0 flex items-center justify-center"
          onClick={togglePlay}
        >
          <button className="bg-black/60 hover:bg-black/80 text-white w-20 h-20 rounded-full flex items-center justify-center text-3xl">
            ▶
          </button>
        </div>
      )}

      {/* CONTROLS */}
      <div
        className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 to-transparent p-4 transition-opacity ${
          showControls ? "opacity-100" : "opacity-0"
        }`}
      >
        {/* SEEK BAR */}
        <input
          type="range"
          value={progress}
          onChange={handleSeek}
          className="w-full accent-red-600"
        />

        <div className="flex items-center justify-between text-white mt-2">
          {/* Play */}
          <button onClick={togglePlay} className="text-lg">
            {isPlaying ? "⏸" : "▶"}
          </button>

          {/* Time */}
          <div className="text-sm font-mono">
            {formatTime(currentTime)} / {formatTime(duration)}
          </div>

          {/* Fullscreen */}
          <button onClick={toggleFullscreen} className="text-lg">
            ⛶
          </button>
        </div>
      </div>
    </div>
  );
}