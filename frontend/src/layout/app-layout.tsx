
import { FC, useState } from "react";
import { Outlet, Link } from "react-router-dom";
import { Nav } from "react-bootstrap";
import AppHeader from "./app-header";
import './app-layout.scss';

const AppLayout: FC = () => {
  const [isPanelOpen, setIsPanelOpen] = useState(true);

  const toggleSidePanel = () => {
    setIsPanelOpen(!isPanelOpen);
  };

  return (
    <div className="app-wrapper">
      <AppHeader toggleSidePanel={toggleSidePanel} />
      <div className={`side-panel ${!isPanelOpen ? 'closed' : ''}`}>
        <Nav className="flex-column">
          <Nav.Link as={Link} to="/">Home</Nav.Link>
          <Nav.Link as={Link} to="/add-expense">Add Expense</Nav.Link>
          <Nav.Link as={Link} to="/logout">Logout</Nav.Link>
        </Nav>
      </div>
      <div className={`container ${!isPanelOpen ? 'panel-closed' : ''}`}>
        <Outlet />
      </div>
    </div>
  );
}

export default AppLayout;
