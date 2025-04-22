
export interface Config {
  API_URL: string;
}

const getApiUrl = (): string => {
  return import.meta.env.VITE_API_URL;
}


const getConfig = (): Config => {
  return {
    API_URL: getApiUrl(),
  };
}

export const config = getConfig();
