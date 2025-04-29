import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { useAuthStateStore } from '../../state/auth/auth-state';
import { config } from "../../services/config-service";
import { UserProfile } from '../../models/user-profile';

export const useProfile = (): UseQueryResult<UserProfile> => {
  const bearerToken = useAuthStateStore(state => state.bearerToken);

  return useQuery({
    queryKey: ['userProfile'],
    queryFn: async () => {
      if (!bearerToken) throw new Error('No token available');

      const response = await fetch(`${config.API_URL}auth/profile`, {
        headers: {
          'Authorization': `Bearer ${bearerToken}`,
          'Accept': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch user profile');
      }

      return response.json();
    },
    enabled: !!bearerToken,
  });
};
