export type PaginatedResponse<T> = {
  total_count: number;
  limit: number;
  offset: number;
  items: T[];
}
