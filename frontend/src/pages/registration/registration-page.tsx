import React, { useState } from 'react';
import { Form, Button, Alert, Container, Row, Col } from 'react-bootstrap';
import './registration-page.scss';
import EtButton from '../../components/et-button/et-button';
import { EtButtonStyle } from '../../components/et-button/et-button-style';

const RegistrationPage: React.FC = () => {
  const [form, setForm] = useState({
    firstName: '',
    lastName: '',
    email: '',
    username: '',
    password: '',
    passwordConfirm: '',
  });

  const [touched, setTouched] = useState({
    firstName: false,
    lastName: false,
    email: false,
    username: false,
    password: false,
    passwordConfirm: false,
  });

  const [formError, setFormError] = useState('');

  const handleChange = (field: string, value: string) => {
    setForm({ ...form, [field]: value });
  };

  const handleBlur = (field: keyof typeof touched) => {
    setTouched({ ...touched, [field]: true });
  };

  const validatePassword = (password: string): boolean => {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
    return regex.test(password);
  };

  const validate = () => {
    const errors: Record<string, string> = {};

    if (!form.firstName.trim()) errors.firstName = 'First name is required.';
    if (!form.lastName.trim()) errors.lastName = 'Last name is required.';
    if (!form.email.trim()) errors.email = 'Email is required.';
    if (!form.username.trim()) errors.username = 'Username is required.';
    if (!form.password) {
      errors.password = 'Password is required.';
    } else if (!validatePassword(form.password)) {
      errors.password = 'Password must be at least 8 characters, include uppercase, lowercase, and a number.';
    }
    if (!form.passwordConfirm) {
      errors.passwordConfirm = 'Please confirm your password.';
    } else if (form.passwordConfirm !== form.password) {
      errors.passwordConfirm = 'Passwords do not match.';
    }

    return errors;
  };

  const errors = validate();
  const isFormValid = Object.keys(errors).length === 0;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!isFormValid) {
      setFormError('Please fix the errors before submitting.');
      setTouched({
        firstName: true,
        lastName: true,
        email: true,
        username: true,
        password: true,
        passwordConfirm: true,
      });
      return;
    }

    setFormError('');

    console.log('Submitting: ', form);

  };

  return (
    <Container className="registration-container">
      <Row className="justify-content-md-center">
        <Col md={6}>
          <h2 className="text-center mb-4">User Registration</h2>
          <Form noValidate onSubmit={handleSubmit}>

            {['firstName', 'lastName', 'email', 'username'].map((field) => (
              <Form.Group key={field} className="mb-4 position-relative" controlId={`form${field}`}>
                <Form.Label>{field.replace(/([A-Z])/g, ' $1')}</Form.Label>
                <Form.Control
                  type="text"
                  value={form[field as keyof typeof form]}
                  onChange={(e) => handleChange(field, e.target.value)}
                  onBlur={() => handleBlur(field as keyof typeof touched)}
                  isInvalid={touched[field as keyof typeof touched] && !!errors[field]}
                  placeholder={`Enter ${field.toLowerCase()}`}
                />
                <Form.Control.Feedback type="invalid" className="field-error">
                  {errors[field]}
                </Form.Control.Feedback>
              </Form.Group>
            ))}

            <Form.Group className="mb-4 position-relative" controlId="formPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                value={form.password}
                onChange={(e) => handleChange('password', e.target.value)}
                onBlur={() => handleBlur('password')}
                isInvalid={touched.password && !!errors.password}
                placeholder="Enter password"
              />
              <Form.Control.Feedback type="invalid" className="field-error">
                {errors.password}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-4 position-relative" controlId="formPasswordConfirm">
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control
                type="password"
                value={form.passwordConfirm}
                onChange={(e) => handleChange('passwordConfirm', e.target.value)}
                onBlur={() => handleBlur('passwordConfirm')}
                isInvalid={touched.passwordConfirm && !!errors.passwordConfirm}
                placeholder="Confirm password"
              />
              <Form.Control.Feedback type="invalid" className="field-error">
                {errors.passwordConfirm}
              </Form.Control.Feedback>
            </Form.Group>

            { formError && <div className='alert-container'>
                <Alert variant="danger">{formError}</Alert>
              </div>
            }

            <div className='button-container'>
              <EtButton
                label='Register'
                style={ EtButtonStyle.primary }
                type='submit'
              />
            </div>

          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default RegistrationPage;
