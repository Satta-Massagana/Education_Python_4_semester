import { createHashRouter } from "react-router-dom";
import AppLayout from "./layout/app-layout";
import HomePage from "./pages/home/home-page";
import AddExpensePage from "./pages/add-expense/add-expense-page";
import LogoutPage from "./pages/logout/logout-page";
import Homework11Page from "./pages/homework11/homework11-page";

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
      path: '/homework-11',
      element: <Homework11Page />
    },
    {
      path: '/logout',
      element: <LogoutPage />
    }
  ]
}])
