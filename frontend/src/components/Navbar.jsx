import {
  Link
} from "react-router-dom";

export default function Navbar() {

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-b from-black/90 to-transparent">

      <div className="flex items-center justify-between px-6 py-4">

        <div className="flex items-center gap-10">

          <Link
            to="/"
            className="text-3xl font-black text-red-600"
          >
            STREAMIX
          </Link>

          <nav className="hidden md:flex gap-6 text-sm text-gray-300">

            <Link
              to="/"
              className="hover:text-white"
            >
              Home
            </Link>

            <Link
              to="/movies"
              className="hover:text-white"
            >
              Movies
            </Link>

            <Link
              to="/series"
              className="hover:text-white"
            >
              TV Series
            </Link>

          </nav>

        </div>
      </div>
    </header>
  );
}