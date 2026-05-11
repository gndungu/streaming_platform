import { useEffect, useRef } from "react";
import Hls from "hls.js";

export default function VideoPlayer({ source }) {

  const videoRef = useRef(null);

  useEffect(() => {

    if (!source) return;

    const video = videoRef.current;

    const src = source.is_hls
      ? source.master_playlist_url
      : source.url;

    // If HLS stream
    if (source.is_hls) {

      if (Hls.isSupported()) {

        const hls = new Hls();

        hls.loadSource(src);

        hls.attachMedia(video);

        return () => {
          hls.destroy();
        };

      } else if (
        video.canPlayType(
          "application/vnd.apple.mpegurl"
        )
      ) {

        // Safari native support
        video.src = src;
      }

    } else {

      // Normal MP4 playback
      video.src = src;
    }

  }, [source]);

  if (!source) return null;

  return (
    <div className="w-full rounded-2xl overflow-hidden bg-black">

      <video
        ref={videoRef}
        controls
        autoPlay
        className="w-full h-[75vh]"
      />

    </div>
  );
}