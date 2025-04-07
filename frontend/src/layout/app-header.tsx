
import { FC } from "react";
import { Container, Nav, Navbar } from "react-bootstrap";
import { Link } from "react-router-dom";
import { FaBars } from "react-icons/fa";
import './app-header.scss';

interface AppHeaderProps {
  toggleSidePanel: () => void;
}

const AppHeader: FC<AppHeaderProps> = ({ toggleSidePanel }) => {
  return <Navbar expand="lg" className="app-header fixed-top">
      <button 
        className="me-2 burger-button" 
        onClick={toggleSidePanel}
      >
        <FaBars size={20} />
      </button>
      <Navbar.Brand as={Link} to="/" className="header-title">
        Expense tracking app
      </Navbar.Brand>
  </Navbar>
}

export default AppHeader;
