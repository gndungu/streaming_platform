import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");

    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const logout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setUser(null);
    window.location.href = "/";
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-b from-black/90 to-transparent">
      <div className="flex items-center justify-between px-6 py-4">

        {/* LEFT SIDE */}
        <div className="flex items-center gap-10">

          <Link to="/" className="text-3xl font-black text-red-600">
            STREAMIX
          </Link>

          <nav className="hidden md:flex gap-6 text-sm text-gray-300">
            <Link to="/" className="hover:text-white">Home</Link>
            <Link to="/movies" className="hover:text-white">Movies</Link>
            <Link to="/series" className="hover:text-white">TV Series</Link>
          </nav>

        </div>

        {/* RIGHT SIDE */}
        <div className="flex items-center gap-4">

          {/* NOT LOGGED IN */}
          {!user && (
            <>
              <Link
                to="/login"
                className="text-sm text-gray-300 hover:text-white"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="bg-red-600 px-4 py-1 rounded text-sm hover:bg-red-700"
              >
                Register
              </Link>
            </>
          )}

          {/* LOGGED IN */}
          {user && (
            <>
              <span className="text-sm text-gray-300">
                {user.username}
              </span>

              <button
                onClick={logout}
                className="bg-gray-800 px-3 py-1 rounded text-sm hover:bg-gray-700"
              >
                Logout
              </button>
            </>
          )}

        </div>

      </div>
    </header>
  );
}