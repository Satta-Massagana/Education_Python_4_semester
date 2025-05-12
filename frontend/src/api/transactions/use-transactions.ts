import { useQuery, UseQueryResult } from "@tanstack/react-query";
import { PaginatedResponse } from "../../types/paginated-response";
import { Transaction } from "../../models/transaction";
import { config } from "../../services/config-service";
import { useAuthStateStore } from "../../state/auth/auth-state";
import { useNavigate } from "react-router-dom";

export const useTransactions = (
  offset: number = 0,
  limit: number = 10
): UseQueryResult<PaginatedResponse<Transaction>> => {

  const { bearerToken } = useAuthStateStore();
  const navigate = useNavigate();

  return useQuery<PaginatedResponse<Transaction>>({
    queryKey: ['transactions', offset, limit],
    queryFn: async () => {
      let response: Response;
      response = await fetch(`${config.API_URL}transactions/?limit=${limit}&offset=${offset}`, {
        headers: {
          Authorization: `Bearer ${bearerToken}`,
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          navigate('/logout')
        }
        throw new Error('Failed to fetch transactions');
      }
      return response.json();
    }
  });
}

export default useTransactions;
