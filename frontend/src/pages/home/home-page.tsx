import { FC } from "react";
import EtButton from "../../components/et-button/et-button";
import { EtButtonStyle } from "../../components/et-button/et-button-style";
import "./home-page.scss";

const HomePage: FC = () => {
  return (
    <div className="app-page">
      <h3>Home page</h3>
      <p>ля-ля-ля...</p>
      <div className="button-list">
        <EtButton
          label="Primary"
          style={EtButtonStyle.primary}
          onClick={() => {}}
        />
        <EtButton
          label="Secondary"
          style={EtButtonStyle.secondary}
          onClick={() => {}}
        />
        <EtButton
          label="Success"
          style={EtButtonStyle.success}
          onClick={() => {}}
        />
        <EtButton
          label="Warning"
          style={EtButtonStyle.warning}
          onClick={() => {}}
        />
        <EtButton
          label="Danger"
          style={EtButtonStyle.danger}
          onClick={() => {}}
        />
        <EtButton
          label="Disabled"
          style={EtButtonStyle.primary}
          onClick={() => {}}
          disabled
        />
      </div>
    </div>
  );
};

export default HomePage;
