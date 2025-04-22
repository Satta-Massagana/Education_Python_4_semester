import { FC } from "react";
import EtButton from "../../components/et-button/et-button";
import { EtButtonStyle } from "../../components/et-button/et-button-style";
import "./home-page.scss";
import { config } from "../../services/config-service";

const HomePage: FC = () => {

  const apiUrl = config.API_URL;

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

      <div className="config-info">
        API URL: {apiUrl}
      </div>

    </div>
  );
};

export default HomePage;
