import { useState } from "react";
import { registerUser } from "../api/auth";
import { Link } from "react-router-dom";
import ErrorDialog from "../components/ErrorDialog";

export default function RegisterPage() {

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: ""
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await registerUser(form);
      setError(res.data.message || "Registration failed");
      window.location.href = "/login";
    } catch (err) {
      setError(err.response?.data?.error || "Registration failed");
    }
  };

  return (
    <div className="h-screen flex items-center justify-center relative text-white">

  {/* 🌑 Background Image + Overlay */}
  <div
    className="absolute inset-0 bg-cover bg-center"
    style={{
      backgroundImage:
        "url(https://images.unsplash.com/photo-1524985069026-dd778a71c7b4)"
    }}
  ></div>

  {/* Dark overlay for readability */}
  <div className="absolute inset-0 bg-black/70"></div>

  {/* 🧾 Form Card */}
  <div className="relative z-10 bg-black/80 backdrop-blur-md p-8 rounded-xl w-96 shadow-2xl">

    <h2 className="text-3xl font-bold mb-6 text-center">
      Register
    </h2>

    <input
      name="username"
      placeholder="Username"
      className="w-full p-3 mb-3 rounded bg-gray-800 text-white placeholder-gray-400 outline-none focus:ring-2 focus:ring-red-600"
      onChange={handleChange}
    />

    <input
      name="email"
      placeholder="Email"
      className="w-full p-3 mb-3 rounded bg-gray-800 text-white placeholder-gray-400 outline-none focus:ring-2 focus:ring-red-600"
      onChange={handleChange}
    />

    <input
      name="password"
      type="password"
      placeholder="Password"
      className="w-full p-3 mb-4 rounded bg-gray-800 text-white placeholder-gray-400 outline-none focus:ring-2 focus:ring-red-600"
      onChange={handleChange}
    />

    <button
      onClick={handleSubmit}
      className="w-full bg-red-600 hover:bg-red-700 transition p-3 rounded font-semibold"
    >
      Create Account
    </button>

    <p className="text-sm text-gray-400 mt-4 text-center">
    Already have an account?{" "}
    
    <Link
        to="/login"
        className="text-green-500 hover:text-green-400 font-semibold"
    >
        Login
    </Link>
    </p>

  </div>

  <ErrorDialog
          message={error}
          onClose={() => setError("")}
        />

</div>
  );
}