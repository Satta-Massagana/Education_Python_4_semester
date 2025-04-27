
import { FC, useEffect } from "react";
import { useAuthStateStore } from "../../state/auth/auth-state";

const LogoutPage: FC = () => {

  const authState = useAuthStateStore();

  useEffect(() => {
    authState.logout();
  }, [ authState ]);

  return <div className="app-page">
  </div>
}

export default LogoutPage;
