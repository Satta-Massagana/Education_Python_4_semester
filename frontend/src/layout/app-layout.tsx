import { FC, useState } from "react";
import { Outlet, Link } from "react-router-dom";
import { Nav } from "react-bootstrap";
import AppHeader from "./app-header";
import "./app-layout.scss";
import { useAuthStateStore } from "../state/auth/auth-state";

const AppLayout: FC = () => {
  const [isPanelOpen, setIsPanelOpen] = useState(true);
  const authState = useAuthStateStore();

  const toggleSidePanel = () => {
    setIsPanelOpen(!isPanelOpen);
  };

  return (
    <div className="app-wrapper">
      <AppHeader toggleSidePanel={toggleSidePanel} />
      <div className={`side-panel ${!isPanelOpen ? "closed" : ""}`}>
        <Nav className="flex-column">
          { !authState.hasBearerToken() &&
            <>
              <Nav.Link as={Link} to="/login">
                Login
              </Nav.Link>
              <Nav.Link as={Link} to="/register">
                Register
              </Nav.Link>
              </>
          }
          { authState.hasBearerToken() &&
            <>
              <Nav.Link as={Link} to="/">
                Home
              </Nav.Link>
              <Nav.Link as={Link} to="/list-expenses">
                List My Expenses
              </Nav.Link>
              <Nav.Link as={Link} to="/add-expense">
                Add Expense
              </Nav.Link>
              <Nav.Link as={Link} to="/list-groups">
                List Groups
              </Nav.Link>
              <Nav.Link as={Link} to="/add-group">
                Add Group
              </Nav.Link>
              <Nav.Link as={Link} to="/logout">
                Logout
              </Nav.Link>
            </>
          }
        </Nav>
      </div>
      <div className={`main-content ${!isPanelOpen ? "panel-closed" : ""}`}>
        <Outlet />
      </div>
    </div>
  );
};

export default AppLayout;
