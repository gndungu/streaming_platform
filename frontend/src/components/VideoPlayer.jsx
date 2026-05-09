export default function VideoPlayer({
  source
}) {

  if (!source) return null;

  return (
    <div className="w-full rounded-2xl overflow-hidden bg-black">

      <video
        controls
        autoPlay
        className="w-full h-[75vh]"
        src={
          source.is_hls
            ? source.master_playlist_url
            : source.url
        }
      />
    </div>
  );
}