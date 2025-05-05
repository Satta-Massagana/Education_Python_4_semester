
export type ExpenseCategory = 'Other'
  | 'Cafe'
  | 'Taxi'
  | 'Work'
  | 'Groceries'
  | 'Housing'
  | 'Salary'
  | 'Communication'
  | 'Children';


export function getExpenseCategories(): ExpenseCategory[] {
  return [
    'Other',
    'Cafe',
    'Taxi',
    'Work',
    'Groceries',
    'Housing',
    'Salary',
    'Communication',
    'Children'
  ];
}
