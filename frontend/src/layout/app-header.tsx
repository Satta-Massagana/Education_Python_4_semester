
import { FC } from "react";
import { Navbar } from "react-bootstrap";
import { Link } from "react-router-dom";
import { FaBars } from "react-icons/fa";
import './app-header.scss';
import { useAuthStateStore } from "../state/auth/auth-state";

interface AppHeaderProps {
  toggleSidePanel: () => void;
}

const AppHeader: FC<AppHeaderProps> = ({ toggleSidePanel }) => {

  const authState = useAuthStateStore();

  return <Navbar expand="sm" className="app-header fixed-top">
      <button 
        className="me-2 burger-button" 
        onClick={toggleSidePanel}
      >
        <FaBars size={20} />
      </button>
      <Navbar.Brand as={Link} to="/" className="header-title">
        Expense tracking app
      </Navbar.Brand>
      { authState.hasBearerToken() && 
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>
            Signed in
          </Navbar.Text>
        </Navbar.Collapse>
      }
  </Navbar>
}

export default AppHeader;
