import { createHashRouter } from "react-router-dom";
import AppLayout from "./layout/app-layout";
import HomePage from "./pages/home/home-page";
import AboutPage from "./pages/about/about-page";

export const appRouter = createHashRouter([{
  element: <AppLayout />,
  children: [
    {
      path: '/',
      element: <HomePage />
    },
    {
      path: '/about',
      element: <AboutPage />
    }
  ]
}])
