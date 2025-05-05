import { createHashRouter } from "react-router-dom";
import AppLayout from "./layout/app-layout";
import HomePage from "./pages/home/home-page";
import AddExpensePage from "./pages/add-expense/add-expense-page";
import LogoutPage from "./pages/logout/logout-page";
import Homework11Page from "./pages/homework11/homework11-page";
import LoginPage from "./pages/login/login-page";
import RegistrationPage from "./pages/registration/registration-page";
import RequireAuth from "./components/auth/require-auth";
import ListExpenses from "./pages/list-expenses/list-expenses";
import AddGroup from "./pages/add-group/add-group";
import ListGroups from "./pages/list-groups/list-groups";

export const appRouter = createHashRouter([{
  element: <AppLayout />,
  children: [
    {
      path: '/login',
      element: <LoginPage />
    },
    {
      path: '/register',
      element: <RegistrationPage />
    },
    {
      element: <RequireAuth redirectPath="/login" />,
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
          path: '/list-expenses',
          element: <ListExpenses />
        },
        {
          path: '/add-group',
          element: <AddGroup />
        },
        {
          path: '/list-groups',
          element: <ListGroups />
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
    }
  ]
}])
