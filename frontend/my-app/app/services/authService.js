'use server';

export async function handleLogin(formData) {
    return handleAuth(formData, 'login');
}

export async function handleRegister(formData) {
    return handleAuth(formData, 'register');
}

async function handleAuth(formData , type = 'login') {
    // const email = formData.get('email');
    // const password = formData.get('password');
    // const errors = [];

    import * as z from "zod"; 
 
    const UserLoginSchema = z.object({ 
        
    email: 
    z.string("This is not string")
    .email("This is not email format")
    .min(12, "Must be greater than 12"),
    
    password: z.string()
    
    });

    try {
        UserLoginSchema.parse(formData);
    } catch(error){
    if(error instanceof z.ZodError){
        // error.issues;
        for (let index = 0; index < error.issues.length; index++) {
            error.push(error.issues[index].message)     
        }
    }
}



    // Common validation for both login and register
    if (!email || !password) {
        errors.push('All fields are required');
    }



    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errors.push('Please enter a valid email address');
    }

    // Additional validation for registration
    if (type === 'register') {
        const confirm = formData.get('confirm');
        
        if (!confirm) {
            errors.push('Please confirm your password');
        }

        if (password.length < 6) {
            errors.push('Password must be at least 6 characters');
        }

        if (password !== confirm) {
            errors.push('Passwords do not match');
        }
    }

    if (errors.length > 0) {
        return { success: false, errors };
    }

    try {
        // Here you would add your actual authentication logic
        // For example:
        if (type === 'register') {
            // await createUser({ email, password });
            // You can add your registration API call here
            return { success: true };
        } else {
            // await loginUser({ email, password });
            // You can add your login API call here
            return { success: true };
        }
    } catch (error) {
        return { 
            success: false, 
            errors: [`${type === 'login' ? 'Login' : 'Registration'} failed. Please try again.`] 
        };
    }
}