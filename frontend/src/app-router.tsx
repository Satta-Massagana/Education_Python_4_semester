import { createHashRouter } from "react-router-dom";
import AppLayout from "./layout/app-layout";
import HomePage from "./pages/home/home-page";
import AddExpensePage from "./pages/add-expense/add-expense-page";
import LogoutPage from "./pages/logout/logout-page";

export const appRouter = createHashRouter([{
  element: <AppLayout />,
  children: [
    {
      path: '/',
      element: <HomePage />
    },
    {
      path: '/add-expense',
      element: <AddExpensePage />
    },
    {
      path: '/logout',
      element: <LogoutPage />
    }
  ]
}])
