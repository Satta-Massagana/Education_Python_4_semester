
import { ChangeEventHandler, FC } from "react";
import React, { useState } from 'react';
import { Form, Button, Container, Row, Col, Alert } from 'react-bootstrap';
import { useMutation } from '@tanstack/react-query';
import { useAuthStateStore } from "../../state/auth/auth-state";
import { getExpenseCategories } from "../../types/expense-category";
import { config } from "../../services/config-service";
import "./add-expense-page.scss";
import { useProfile } from "../../api/auth/use-profile";

const categories = getExpenseCategories();

const AddExpensePage: FC = () => {
  const [form, setForm] = useState({
    category: '',
    amount: '',
    description: '',
  });
  const [touched, setTouched] = useState<{ [key: string]: boolean }>({});
  const bearerToken = useAuthStateStore(state => state.bearerToken);
  const profile = useProfile().data;

  const mutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await fetch(`${config.API_URL}transactions/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${bearerToken}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Failed to create expense');
      }

      return response.json();
    },
    onSuccess: () => {
      setForm({ category: '', amount: '', description: '' });
      setTouched({});
    },
  });

  const handleChange: ChangeEventHandler = (e: any) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleBlur = (field: string) => {
    setTouched({ ...touched, [field]: true });
  };

  const isFieldInvalid = (name: string) => {
    const value = form[name as keyof typeof form];
    if (!touched[name]) return false;
    if (name === 'amount') return isNaN(Number(value)) || Number(value) <= 0;
    return value.trim() === '';
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setTouched({ category: true, amount: true, description: true });

    if (Object.keys(form).some(isFieldInvalid)) {
      return;
    };
    
    mutation.mutate({
      ...form,
      amount: parseFloat(form.amount),
      currency: 'RUB',
      type: 'Expense',
      user_id: profile!.id
    });
  };

  return (
    <Container className="add-expense-form mt-5">
      <Row className="justify-content-md-center">
        <Col md={6}>
          <h2 className="mb-4">Add Expense</h2>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3 position-relative">
              <Form.Label>Category</Form.Label>
              <Form.Select
                name="category"
                value={form.category}
                onChange={handleChange}
                onBlur={() => handleBlur('category')}
                isInvalid={isFieldInvalid('category')}
              >
                <option value="">Select a category</option>
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </Form.Select>
              <Form.Control.Feedback type="invalid" className="position-absolute">
                Category is required
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3 position-relative">
              <Form.Label>Amount</Form.Label>
              <Form.Control
                type="number"
                name="amount"
                value={form.amount}
                onChange={handleChange}
                onBlur={() => handleBlur('amount')}
                isInvalid={isFieldInvalid('amount')}
              />
              <Form.Control.Feedback type="invalid" className="position-absolute">
                Enter a valid amount
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3 position-relative">
              <Form.Label>Description</Form.Label>
              <Form.Control
                type="text"
                name="description"
                value={form.description}
                onChange={handleChange}
                onBlur={() => handleBlur('description')}
                isInvalid={isFieldInvalid('description')}
              />
              <Form.Control.Feedback type="invalid" className="position-absolute">
                Description is required
              </Form.Control.Feedback>
            </Form.Group>

            { mutation.isError && 
              <Alert variant="danger" show={mutation.isError}>
                Failed to store data
              </Alert>
            }
            
            { mutation.isSuccess && 
                <Alert variant="success" show={mutation.isSuccess}>
                  Expense was successfully added
                </Alert>
            }

            <Button
              type="submit"
              className="w-100 submit-button"
              disabled={mutation.isPending}
            >
              {mutation.isPending ? 'Adding...' : 'Add Expense'}
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default AddExpensePage;