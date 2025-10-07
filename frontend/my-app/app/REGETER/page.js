import Link from 'next/link';

async function handleRegister(formData) {
    'use server';
    
    const email = formData.get('email');
    const password = formData.get('password');
    const confirm = formData.get('confirm');
    
    const errors = [];

    if (!email || !password || !confirm) {
        errors.push('All fields are required');
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errors.push('Please enter a valid email address');
    }

    if (password.length < 6) {
        errors.push('Password must be at least 6 characters');
    }

    if (password !== confirm) {
        errors.push('Passwords do not match');
    }

    if (errors.length > 0) {
        return { success: false, errors };
    }

    try {

        return { success: true };
    } catch (error) {
        return { 
            success: false, 
            errors: ['Registration failed. Please try again.'] 
        };
    }
}

export default function Register() {

    return (
        <div className="max-w-[400px] mx-auto mt-10 p-6 border border-gray-200 rounded-lg shadow-md bg-white">
            <h2 className="text-2xl font-bold text-center mb-5" style={{color:'black'}}>Register</h2>
            <form action={handleRegister}>
                <div className="mb-4">
                    <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-700">Email</label>
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
                    <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-700">Password</label>
                    <input 
                        type="password" 
                        id="password" 
                        name="password" 
                        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" 
                        style={{color:'black'}} 
                        required 
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="confirm" className="block mb-2 text-sm font-medium text-gray-700">Confirm Password</label>
                    <input 
                        type="password" 
                        id="confirm" 
                        name="confirm" 
                        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400" 
                        style={{color:'black'}} 
                        required 
                    />
                </div>
                <button 
                    type="submit" 
                    className="w-full py-2 bg-blue-600 text-white rounded font-semibold hover:bg-blue-700 transition-colors"
                >
                    Register
                </button>
                <p className="mt-4 text-center text-sm text-gray-600">
                    Already have an account?{' '}
                    <Link href="/LOGIN" className="font-medium text-blue-600 hover:text-blue-500">
                        Login here
                    </Link>
                </p>
            </form>
        </div>
    );


}