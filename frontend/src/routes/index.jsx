import {
  createBrowserRouter
} from "react-router-dom";

import HomePage
  from "../pages/HomePage";

import DetailPage
  from "../pages/DetailPage";

import WatchPage
  from "../pages/WatchPage";

import MoviesPage
  from "../pages/MoviesPage";

import SeriesPage
  from "../pages/SeriesPage";

const router =
  createBrowserRouter([

    {
      path: "/",
      element: <HomePage />
    },

    {
      path: "/movies",
      element: <MoviesPage />
    },

    {
      path: "/series",
      element: <SeriesPage />
    },

    {
      path: "/:type/:id",
      element: <DetailPage />
    },

    {
      path: "/watch/:type/:id",
      element: <WatchPage />
    }
  ]);

export default router;