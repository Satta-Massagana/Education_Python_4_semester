import React, { useEffect, useState } from 'react';
import { Form, Alert, Container, Row, Col } from 'react-bootstrap';
import './login-page.scss';
import EtButton from '../../components/et-button/et-button';
import { EtButtonStyle } from '../../components/et-button/et-button-style';
import { useAuthStateStore } from '../../state/auth/auth-state';
import { useNavigate } from 'react-router-dom';
import { config } from "../../services/config-service";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [touched, setTouched] = useState({ username: false, password: false });
  const [formError, setFormError] = useState('');
  const authState = useAuthStateStore();
  const navigate = useNavigate();
  const apiUrl = config.API_URL;

  useEffect(() => {
    if (authState.hasBearerToken()) {
      navigate('/');
    }
  }, [ authState ]);

  const validate = () => ({
    username: !username.trim() ? 'Username is required.' : '',
    password: !password.trim() ? 'Password is required.' : ''
  });

  const errors = validate();

  const isFormValid = () => !errors.username && !errors.password;

  const handleBlur = (field: 'username' | 'password') => {
    setTouched({ ...touched, [field]: true });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!isFormValid()) {
      setFormError('Please fix the errors before submitting.');
      setTouched({ username: true, password: true });
      return;
    }

    setFormError('');

    const body = new URLSearchParams();
    body.append('grant_type', 'password');
    body.append('username', username);
    body.append('password', password);

    try {
      const response = await fetch(`${apiUrl}auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
        },
        body,
      });

      if (!response.ok) {
        const err = await response.json();
        setFormError(err.detail || 'Login failed.');
        return;
      }

      const data = await response.json();
      authState.setBearerToken(data.access_token);
      navigate('/');

    } catch (err) {
      setFormError('Login failed. Please try again.');
      console.error(err);
    }

  };

  return (
    <Container className="login-container">
      <Row className="justify-content-md-center">
        <Col md={8} lg={6} xl={4} className="form-container">
          <h2 className="text-center mb-3">Login</h2>
          <Form noValidate onSubmit={handleSubmit}>

            <Form.Group controlId="formUsername" className="mb-3 position-relative">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                onBlur={() => handleBlur('username')}
                isInvalid={touched.username && !!errors.username}
                placeholder="Enter username"
              />
              <Form.Control.Feedback type="invalid" className="field-error">
                {errors.username}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group controlId="formPassword" className="mb-3 position-relative">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onBlur={() => handleBlur('password')}
                isInvalid={touched.password && !!errors.password}
                placeholder="Enter password"
              />
              <Form.Control.Feedback type="invalid" className="field-error">
                {errors.password}
              </Form.Control.Feedback>
            </Form.Group>

            <div className="text-left mt-3 registration-container">
              <span>Don't have an account? </span>
              <a href="/#/register" className="registration-link">Register here</a>
            </div>

            {formError && <Alert variant="danger">{formError}</Alert>}

            <EtButton
              label='Login'
              style={ EtButtonStyle.primary }
              type='submit'
            />

          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default LoginPage;