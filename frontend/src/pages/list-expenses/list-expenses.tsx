
import { useState, FC, useMemo } from 'react';
import { Table, Spinner, Alert, Modal } from 'react-bootstrap';
import useTransactions from '../../api/transactions/use-transactions';
import useDeleteTransaction from '../../api/transactions/use-delete-transaction';

import "./list-expenses.scss";
import EtButton from '../../components/et-button/et-button';
import { EtButtonStyle } from '../../components/et-button/et-button-style';

const limit = 10;

export const ListExpenses: FC = () => {
  const [showModal, setShowModal] = useState(false);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [ offset, setOffset ] = useState(0);

  const { data, isLoading, isError } = useTransactions(offset, limit);
  const deleteMutation = useDeleteTransaction();

  const hasMore = useMemo(() => {
    return (data?.total_count ?? 0) > offset + limit;
  }, [ data, offset, limit ]);

  const confirmDelete = (id: number) => {
    setSelectedId(id);
    setShowModal(true);
  };

  const handleDelete = () => {
    if (selectedId !== null) {
      deleteMutation.mutate(selectedId);
    }
    setShowModal(false);
  };

  const handleNextPage = () => {
    if (hasMore) {
      setOffset(offset + limit);
    }
  };

  const handlePreviousPage = () => {
    if (offset >= limit) {
      setOffset(offset - limit);
    }
  };
  
  if (isLoading) return <Spinner animation="border" />;
  if (isError) return <Alert variant="danger">Error loading expenses</Alert>;

  return (
    <div className="p-3">
      <h2>Expense List</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Date</th>
            <th>Category</th>
            <th>Amount</th>
            <th className="d-none d-md-table-cell">Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data?.items?.map((expense: any) => (
            <tr key={expense.id}>
              <td>{expense.date.split('T')[0]}</td>
              <td>{expense.category}</td>
              <td>{expense.amount}</td>
              <td className="d-none d-md-table-cell">{expense.description}</td>
              <td>
                <EtButton
                  label="Delete"
                  style={EtButtonStyle.danger}
                  onClick={() => confirmDelete(expense.id)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      <div className="d-flex justify-content-between">
        <EtButton
          label="Prev"
          style={EtButtonStyle.primary}
          onClick={handlePreviousPage}
          disabled={offset === 0}
        />
        <EtButton
          label="Next"
          style={EtButtonStyle.primary}
          onClick={handleNextPage}
          disabled={!hasMore}
        />
      </div>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Deletion</Modal.Title>
        </Modal.Header>
        <Modal.Body>Are you sure you want to delete this transaction?</Modal.Body>
        <Modal.Footer>

          <EtButton
            label="Cancel"
            style={EtButtonStyle.secondary}
            onClick={() => setShowModal(false)}
          />

          <EtButton
            label={deleteMutation.isPending ? 'Deleting...' : 'Delete'}
            style={EtButtonStyle.danger}
            onClick={handleDelete}
            disabled={deleteMutation.isPending}
          />

        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default ListExpenses
