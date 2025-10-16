'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useAuthStore } from '../../store/useAuthStore'
import { handleProfileUpdate } from '../../utils/profileService' 

export default function Profile() {
  const { user, token, updateUser } = useAuthStore()
  const [editedUser, setEditedUser] = useState(user || {})
  const [isEditing, setIsEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  const handleInputChange = (field, value) => {
    setEditedUser((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleSave = async () => {
    setLoading(true)
    setMessage(null)

    const formData = new FormData()
    formData.append('user_name', editedUser.user_name || '')
    formData.append('user_email', editedUser.user_email || '')
    formData.append('user_phone', editedUser.user_phone || '')
    formData.append('user_address', editedUser.user_address || '')
    formData.append('avatar', editedUser.avatar || '')

    const res = await handleProfileUpdate(formData, token)

    if (res.error) {
      setMessage(res.error)
    } else {
      updateUser(res.user)
      setMessage(res.message)
      setIsEditing(false)
    }

    setLoading(false)
  }

  if (!user) {
    return (
      <div className="text-center mt-20 text-gray-700">
        You must be logged in to view this page.
        <Link href="/LOGIN" className="text-blue-600 ml-2 underline">
          Login
        </Link>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <Link href="/" className="text-blue-600 hover:text-blue-800 font-medium">
            ← Back to Home
          </Link>
        </div>

        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-2xl font-bold text-gray-900">User Profile</h1>
              <button
                onClick={() => (isEditing ? handleSave() : setIsEditing(true))}
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                {loading ? 'Saving...' : isEditing ? 'Save Changes' : 'Edit Profile'}
              </button>
            </div>

            {message && (
              <p className={`mb-4 text-center ${message.includes('✅') ? 'text-green-600' : 'text-red-600'}`}>
                {message}
              </p>
            )}

            <div className="flex flex-col md:flex-row gap-8">
              <div className="flex-shrink-0">
                <img
                  className="h-32 w-32 rounded-full object-cover"
                  src={editedUser.avatar || 'https://via.placeholder.com/150'}
                  alt="Profile"
                />
              </div>

              <div className="flex-1 space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editedUser.user_name || ''}
                      onChange={(e) => handleInputChange('user_name', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    />
                  ) : (
                    <p className="text-lg text-gray-900">{user.user_name}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <p className="text-lg text-gray-900">{user.user_email}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                  <p className="text-lg text-gray-900">{user.user_role}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
