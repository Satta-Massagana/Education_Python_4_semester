import React, { useState } from 'react';
import { Form, Alert, Container, Row, Col } from 'react-bootstrap';
import './registration-page.scss';
import EtButton from '../../components/et-button/et-button';
import { EtButtonStyle } from '../../components/et-button/et-button-style';
import { config } from "../../services/config-service";
import { useNavigate } from 'react-router-dom';

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
  const navigate = useNavigate();
  const apiUrl = config.API_URL;

  const [formError, setFormError] = useState<string | {msg: string}[]>('');

  const handleChange = (field: string, value: string) => {
    setForm({ ...form, [field]: value });
  };

  const handleBlur = (field: keyof typeof touched) => {
    setTouched({ ...touched, [field]: true });
  };

  const validatePassword = (password: string): boolean => {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{10,}$/;
    return regex.test(password);
  };

  const setAllTouched = (value: boolean) => {
    setTouched({
      firstName: value,
      lastName: value,
      email: value,
      username: value,
      password: value,
      passwordConfirm: false,
    });
  }

  const validate = () => {
    const errors: Record<string, string> = {};

    if (!form.firstName.trim()) errors.firstName = 'First name is required.';
    if (!form.lastName.trim()) errors.lastName = 'Last name is required.';
    if (!form.email.trim()) errors.email = 'Email is required.';
    if (!form.username.trim()) errors.username = 'Username is required.';
    if (!form.password) {
      errors.password = 'Password is required.';
    } else if (!validatePassword(form.password)) {
      errors.password = 'Password must be at least 10 characters, include uppercase, lowercase, and a number.';
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

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
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

    const payload = {
      first_name: form.firstName,
      last_name: form.lastName,
      login: form.username,
      email: form.email,
      password: form.password,
      active: true,
    };

    try {
      const response = await fetch(`${apiUrl}auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        // const err = await response.json();
        // setFormError(err.detail || 'Registration failed.');
        setFormError('Registration failed. Please check data and try again.');
        return;
      }

      const data = await response.json();
      console.log('Registration successful', data);

      navigate('/login');
    } catch (err) {
      console.error(err);
      setFormError('Network error. Please try again.');
    }
  };

  const handleReset = (e: React.FormEvent) => {
    e.preventDefault();
    setForm({
      firstName: '',
      lastName: '',
      email: '',
      username: '',
      password: '',
      passwordConfirm: '',
    });
    setAllTouched(false);
    setFormError('');
  }

  return (
    <Container className="registration-container">
      <Row className="justify-content-md-center">
        <Col lg={8} xl={6} className='form-container'>
          <h2 className="text-center mb-4">User Registration</h2>
          <Form noValidate onSubmit={handleSubmit} onReset={handleReset}>

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
                <Alert variant="danger">
                  { Array.isArray(formError) && formError.map((err, idx) => <div key={idx}>{err.msg}</div>) }
                  { !(Array.isArray(formError)) && <div>{formError}</div> }
                </Alert>
              </div>
            }

            <div className='button-container'>
              <EtButton
                label='Register'
                style={ EtButtonStyle.primary }
                type='submit'
              />
              <EtButton
                label='Reset'
                style={ EtButtonStyle.secondary }
                type='reset'
              />
            </div>

          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default RegistrationPage;
