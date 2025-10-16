'use client';

import Link from 'next/link';
import { useAuthStore } from '../../store/useAuthStore';
import { handleRegister } from '../../utils/authService';

export default function Register() {
  const { message, loading, setMessage, setLoading, login } = useAuthStore();

  async function onSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    const formData = new FormData(e.target);
    const result = await handleRegister(formData);

    if (result.error) {
      setMessage(result.error);
    } else {
      login(result.token, result.user);
      setMessage(result.message);
      e.target.reset();
    }

    setLoading(false);
  }

  return (
    <div className="max-w-[400px] mx-auto mt-10 p-6 border border-gray-200 rounded-lg shadow-md bg-white">
      <h2 className="text-2xl font-bold text-center mb-5 text-black">Register</h2>

      <form onSubmit={onSubmit}>
        <div className="mb-4">
          <label className="block mb-2 text-sm font-medium text-gray-700">Username</label>
          <input type="text" name="username" className="w-full px-3 py-2 border rounded" required />
        </div>

        <div className="mb-4">
          <label className="block mb-2 text-sm font-medium text-gray-700">Email</label>
          <input type="email" name="email" className="w-full px-3 py-2 border rounded" required />
        </div>

        <div className="mb-4">
          <label className="block mb-2 text-sm font-medium text-gray-700">Password</label>
          <input type="password" name="password" className="w-full px-3 py-2 border rounded" required />
        </div>

        <div className="mb-4">
          <label className="block mb-2 text-sm font-medium text-gray-700">Confirm Password</label>
          <input type="password" name="confirm" className="w-full px-3 py-2 border rounded" required />
        </div>

        {message && (
          <p className={`text-center text-sm mb-3 ${message.includes('success') ? 'text-green-600' : 'text-red-600'}`}>
            {message}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 bg-blue-600 text-white rounded font-semibold hover:bg-blue-700 transition-colors"
        >
          {loading ? 'Registering...' : 'Register'}
        </button>

        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link href="/LOGIN" className="font-medium text-blue-600 hover:text-blue-500">
            Login
          </Link>
        </p>
      </form>
    </div>
  );
}


