import { useMutation, useQueryClient } from "@tanstack/react-query";
import { config } from "../../services/config-service";
import { useAuthStateStore } from "../../state/auth/auth-state";

const useDeleteTransaction = () => {
  const { bearerToken } = useAuthStateStore();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      const response = await fetch(`${config.API_URL}transactions/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${bearerToken}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to delete transaction');
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions']});
    },
  });
}

export default useDeleteTransaction;