'use server'

import { z } from 'zod'


const profileSchema = z.object({
  user_name: z
    .string()
    .min(3, { message: 'Username must be at least 3 characters' })
    .max(30, { message: 'Username must be at most 30 characters' }),
  user_email: z.string().email({ message: 'Invalid email address' }),
  user_phone: z
    .string()
    .optional()
    .refine(
      (val) => {
        if (!val) return true
        return /^[0-9+\-\s().]{7,20}$/.test(val.trim())
      },
      { message: 'Invalid phone number' }
    ),
  user_address: z.string().optional().max(300, { message: 'Address too long' }),
  avatar: z
    .string()
    .optional()
    .refine((v) => {
      if (!v) return true
      try {
        const url = new URL(v)
        return url.protocol === 'http:' || url.protocol === 'https:'
      } catch {
        return false
      }
    }, { message: 'Invalid avatar URL' }),
})


export async function handleProfileUpdate(formData, token) {
  const data = {
    user_name: formData.get('user_name'),
    user_email: formData.get('user_email'),
    user_phone: formData.get('user_phone'),
    user_address: formData.get('user_address'),
    avatar: formData.get('avatar'),
  }

  const result = profileSchema.safeParse(data)
  if (!result.success) {
    return { error: result.error.issues[0].message }
  }

  try {
    const res = await fetch('http://0.0.0.0:8001/api/v1/user/update', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(result.data),
    })

    const response = await res.json()

    if (!res.ok) throw new Error(response.message || 'Profile update failed')

    return {
      success: true,
      message: 'Profile updated successfully ✅',
      user: response.user,
    }
  } catch (err) {
    return { error: err.message }
  }
}
