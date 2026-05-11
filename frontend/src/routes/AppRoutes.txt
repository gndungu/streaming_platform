import { BrowserRouter, Routes, Route } from "react-router-dom";

import HomePage from "../pages/HomePage";
import DetailPage from "../pages/DetailPage";
import PlayerPage from "../pages/PlayerPage";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={<HomePage />}
        />

        <Route
          path="/:type/:id"
          element={<DetailPage />}
        />

        <Route
          path="/watch/:type/:id"
          element={<PlayerPage />}
        />
      </Routes>
    </BrowserRouter>
  );
}