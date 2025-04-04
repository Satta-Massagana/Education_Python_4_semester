import { FC } from "react";
import { Outlet } from "react-router-dom";
import AppHeader from "./app-header";

const  AppLayout: FC = () => {

  return <div className="app-wrapper">
    <AppHeader />
    <div className="container">
      <Outlet />
    </div>
  </div>;

}

export default AppLayout
