import { useNavigate } from "react-router-dom";

export default function BackButton({
  to = "/",
  label = "Back"
}) {
  const navigate = useNavigate();

  return (
    <button
      onClick={() => navigate(to)}
      className="
        flex items-center gap-2
        bg-black/50 backdrop-blur-md
        hover:bg-black/70
        border border-white/10
        px-5 py-3
        rounded-2xl
        text-white
        transition
      "
    >
      ← {label}
    </button>
  );
}