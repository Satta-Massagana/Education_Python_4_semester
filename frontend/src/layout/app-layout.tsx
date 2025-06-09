import { FC } from "react";
import { Outlet, Link } from "react-router-dom";
import { Nav } from "react-bootstrap";
import AppHeader from "./app-header";
import "./app-layout.scss";
import { useAuthStateStore } from "../state/auth/auth-state";
import { useSidePanelStore } from "../state/layout/side-panel-state";

const AppLayout: FC = () => {
  const { isOpen: isPanelOpen, setIsOpen: setIsPanelOpen, close: closePanel } = useSidePanelStore(state => state);
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
              <Nav.Link as={Link} to="/login" onClick={ closePanel }>
                Login
              </Nav.Link>
              <Nav.Link as={Link} to="/register" onClick={ closePanel }>
                Register
              </Nav.Link>
              </>
          }
          { authState.hasBearerToken() &&
            <>
              <Nav.Link as={Link} to="/" onClick={ closePanel }>
                Home
              </Nav.Link>
              <Nav.Link as={Link} to="/list-expenses" onClick={ closePanel }>
                List My Expenses
              </Nav.Link>
              <Nav.Link as={Link} to="/add-expense" onClick={ closePanel }>
                Add Expense
              </Nav.Link>
              <Nav.Link as={Link} to="/list-groups" onClick={ closePanel }>
                List Groups
              </Nav.Link>
              <Nav.Link as={Link} to="/add-group" onClick={ closePanel }>
                Add Group
              </Nav.Link>
              <Nav.Link as={Link} to="/logout" onClick={ closePanel }>
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
