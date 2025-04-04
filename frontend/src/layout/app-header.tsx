import { FC } from "react";
import { Container, Nav, Navbar } from "react-bootstrap";

import './app-header.scss';

const AppHeader: FC = () => {

  return <Navbar expand="lg" className="app-header">
    <Container>
      <Navbar.Brand href="/#/" className="header-title">
        Expense tracking app
      </Navbar.Brand>
      <Navbar.Toggle />
      <Navbar.Collapse className="justify-content-end">
        <Nav>
          <Nav.Link href="/#/about">About</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>

}

export default AppHeader;
