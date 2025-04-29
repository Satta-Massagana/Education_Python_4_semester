
import { FC } from "react";
import { Navbar } from "react-bootstrap";
import { Link } from "react-router-dom";
import { FaBars } from "react-icons/fa";
import './app-header.scss';
import { useAuthStateStore } from "../state/auth/auth-state";
import { useProfile } from "../api/auth/use-profile";

interface AppHeaderProps {
  toggleSidePanel: () => void;
}

const AppHeader: FC<AppHeaderProps> = ({ toggleSidePanel }) => {

  const authState = useAuthStateStore();
  const userProfile = useProfile();

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
      { authState.hasBearerToken() && userProfile.isSuccess && userProfile.data &&
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>
            Signed as: { userProfile.data.first_name } { userProfile.data.last_name }
          </Navbar.Text>
        </Navbar.Collapse>
      }
  </Navbar>
}

export default AppHeader;
