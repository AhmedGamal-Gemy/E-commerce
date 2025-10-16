'use server';

import { z } from 'zod';

// (Validation Schema)
const loginSchema = z.object({
  email: z.string().email({ message: 'Invalid email address' }),
  password: z.string().min(6, { message: 'Password must be at least 6 characters' }),
});

const registerSchema = loginSchema
  .extend({
    username: z.string().min(3, { message: 'Username must be at least 3 characters' }),
    confirm: z.string(),
  })
  .refine((data) => data.password === data.confirm, {
    message: "Passwords don't match",
    path: ['confirm'],
  });


  
// LOGIN
export async function handleLogin(formData) {
  const data = {
    email: formData.get('email'),
    password: formData.get('password'),
  };

  const result = loginSchema.safeParse(data);
  if (!result.success) return { error: result.error.issues[0].message };

  try {
    const res = await fetch('http://0.0.0.0:8001/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_email: data.email,
        password: data.password,
      }),
    });

    const response = await res.json();

    if (!res.ok) {
      throw new Error(response.message || 'Login failed');
    }

    // { user, access_token }
    return {
      success: true,
      message: 'Login successful',
      token: response.access_token,
      user: response.user,
    };
  } catch (err) {
    return { error: err.message };
  }
}


// REGISTER
export async function handleRegister(formData) {
  const data = {
    username: formData.get('username'),
    email: formData.get('email'),
    password: formData.get('password'),
    confirm: formData.get('confirm'),
  };

  const result = registerSchema.safeParse(data);
  if (!result.success) return { error: result.error.issues[0].message };

  try {
    const res = await fetch('http://0.0.0.0:8001/api/v1/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_name: data.username,
        user_email: data.email,
        password: data.password,
      }),
    });

    const response = await res.json();

    if (!res.ok) {
      throw new Error(response.message || 'Registration failed');
    }

    return {
      success: true,
      message: 'Registration successful',
      token: response.access_token,
      user: response.user,
    };
  } catch (err) {
    return { error: err.message };
  }
}
