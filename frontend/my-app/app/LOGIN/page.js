
import Link from 'next/link';
import { handleLogin } from '../services/authService';

export default function Login() {
    return (
        <div className="max-w-[350px] mx-auto mt-10 p-6 border border-gray-200 rounded-lg shadow-md bg-white">
            <h2 className="text-2xl font-bold text-center mb-5" style={{color:'black'}}>Login</h2>
            <form action={handleLogin}>
                <div className="mb-4">
                    <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-700">
                        Email
                    </label>
                    <input 
                        type="email" 
                        id="email" 
                        name="email" 
                        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" 
                        style={{color:'black'}} 
                        required 
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-700">
                        Password
                    </label>
                    <input 
                        type="password" 
                        id="password" 
                        name="password" 
                        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" 
                        style={{color:'black'}} 
                        required 
                    />
                </div>
                <button 
                    type="submit" 
                    className="w-full py-2 bg-blue-600 text-white rounded font-semibold hover:bg-blue-700 transition-colors"
                >
                    Login
                </button>
                <p className="mt-4 text-center text-sm text-gray-600">
                    Don't have an account?{' '}
                    <Link href="/REGETER" className="font-medium text-blue-600 hover:text-blue-500">
                        Register here
                    </Link>
                </p>
            </form>
        </div>
    );
}
