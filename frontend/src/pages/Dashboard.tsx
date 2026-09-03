import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [profilePhoto, setProfilePhoto] = useState<string | null>(null);
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [email, setEmail] = useState('');
  
  // Password change states
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  useEffect(() => {
    const savedPhoto = localStorage.getItem('profilePhoto');
    if (savedPhoto) {
      setProfilePhoto(savedPhoto);
    }
    const savedEmail = localStorage.getItem('registeredEmail');
    if (savedEmail) {
      setEmail(savedEmail);
    }
  }, []);

  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result as string;
        setProfilePhoto(base64String);
        try {
          localStorage.setItem('profilePhoto', base64String);
        } catch (err) {
          alert("This image is too large to save permanently in your browser.");
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemovePhoto = () => {
    setProfilePhoto(null);
    localStorage.removeItem('profilePhoto');
  };

  const handleEmailSave = () => {
    if (!email) {
      alert("Email cannot be empty.");
      return;
    }
    localStorage.setItem('registeredEmail', email);
    alert("Email ID saved successfully! It is now permanently visible on your dashboard.");
  };

  const handleForgotPassword = () => {
    const savedEmail = localStorage.getItem('registeredEmail') || email;
    if (!savedEmail) {
      alert("Please save an Email ID first so we know where to send the OTP.");
      return;
    }
    
    // Generate a 6-digit OTP
    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    
    // Temporarily overwrite their password with the OTP
    localStorage.setItem('registeredPassword', otp);
    
    alert(`An OTP has been sent to your email ID: ${savedEmail}\n\n[DEMO MODE: Your OTP is ${otp}]\n\nPlease enter this OTP in the 'Current Password' box to authorize your password change.`);
  };

  const handlePasswordSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const savedPassword = localStorage.getItem('registeredPassword');
    
    if (currentPassword !== savedPassword) {
      alert("The Current Password (or OTP) you entered is incorrect.");
      return;
    }
    if (newPassword !== confirmPassword) {
      alert("The new passwords do not match.");
      return;
    }
    
    localStorage.setItem('registeredPassword', newPassword);
    alert("Password successfully updated!");
    
    // Reset form
    setShowPasswordForm(false);
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
  };

  return (
    <div className="flex flex-col items-center p-8">
      <h2 className="text-3xl font-bold mb-8 text-gray-800">My Profile Dashboard</h2>
      
      <div className="bg-white p-8 rounded-xl shadow-md border w-full max-w-md flex flex-col items-center">
        
        <div className="w-48 h-48 rounded-full border-4 border-indigo-100 overflow-hidden bg-gray-50 mb-8 flex items-center justify-center shadow-inner">
          {profilePhoto ? (
            <img src={profilePhoto} alt="Profile" className="w-full h-full object-cover" />
          ) : (
            <svg className="w-24 h-24 text-gray-300" fill="currentColor" viewBox="0 0 24 24">
              <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          )}
        </div>

        {!profilePhoto ? (
          <label className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 font-medium cursor-pointer shadow-sm transition-colors w-full text-center mb-6">
            Upload Profile Photo
            <input 
              type="file" 
              className="hidden" 
              accept="image/*" 
              onChange={handlePhotoUpload} 
            />
          </label>
        ) : (
          <div className="flex space-x-4 w-full mb-6">
            <label className="bg-indigo-50 text-indigo-700 border border-indigo-200 px-4 py-3 rounded-lg hover:bg-indigo-100 font-medium cursor-pointer shadow-sm transition-colors flex-1 text-center">
              Edit Profile
              <input 
                type="file" 
                className="hidden" 
                accept="image/*" 
                onChange={handlePhotoUpload} 
              />
            </label>
            <button 
              onClick={handleRemovePhoto}
              className="bg-red-50 text-red-600 border border-red-200 px-4 py-3 rounded-lg hover:bg-red-100 font-medium cursor-pointer shadow-sm transition-colors flex-1 text-center"
            >
              Remove Profile
            </button>
          </div>
        )}

        {/* Improved Email ID Section */}
        <div className="w-full border-t pt-6 mb-4 space-y-2">
          <label className="block text-sm font-bold text-gray-700">Registered Email ID</label>
          <div className="flex space-x-2">
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. user@example.com" 
              className="flex-1 rounded-md border-gray-300 border p-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-semibold text-indigo-900 bg-gray-50" 
            />
            <button 
              onClick={handleEmailSave}
              className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 font-medium text-sm shadow-sm cursor-pointer transition-colors"
            >
              Save
            </button>
          </div>
          <p className="text-xs text-gray-500">This email is used to recover your account if you forget your password.</p>
        </div>

        {/* Change Password Section */}
        <div className="w-full border-t pt-6 mt-2">
          {!showPasswordForm ? (
            <button 
              onClick={() => setShowPasswordForm(true)}
              className="w-full text-gray-600 bg-gray-100 hover:bg-gray-200 px-4 py-3 rounded-lg font-medium cursor-pointer transition-colors"
            >
              Change Password
            </button>
          ) : (
            <form onSubmit={handlePasswordSubmit} className="space-y-4 animate-fade-in">
              <h3 className="font-bold text-gray-700 mb-2">Update Password</h3>
              
              <div className="relative">
                <input 
                  type="password" 
                  value={currentPassword}
                  onChange={e => setCurrentPassword(e.target.value)}
                  placeholder="Current Password (or OTP)" 
                  required 
                  className="w-full rounded-md border-gray-300 border p-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none pr-20" 
                />
                <button 
                  type="button" 
                  onClick={handleForgotPassword}
                  className="absolute right-2 top-2 text-xs text-indigo-600 hover:text-indigo-800 font-bold bg-indigo-50 px-2 py-1 rounded cursor-pointer transition-colors"
                >
                  Forgot?
                </button>
              </div>

              <div>
                <input 
                  type="password" 
                  value={newPassword}
                  onChange={e => setNewPassword(e.target.value)}
                  placeholder="New Password" 
                  required 
                  className="w-full rounded-md border-gray-300 border p-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none" 
                />
              </div>
              
              <div>
                <input 
                  type="password" 
                  value={confirmPassword}
                  onChange={e => setConfirmPassword(e.target.value)}
                  placeholder="Confirm New Password" 
                  required 
                  className="w-full rounded-md border-gray-300 border p-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none" 
                />
              </div>
              
              <div className="flex space-x-2 pt-2">
                <button 
                  type="button" 
                  onClick={() => {
                    setShowPasswordForm(false);
                    setCurrentPassword('');
                    setNewPassword('');
                    setConfirmPassword('');
                  }} 
                  className="flex-1 bg-gray-100 text-gray-600 px-3 py-2 rounded-md hover:bg-gray-200 font-medium text-sm cursor-pointer transition-colors"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="flex-1 bg-indigo-600 text-white px-3 py-2 rounded-md hover:bg-indigo-700 font-medium text-sm shadow-sm cursor-pointer transition-colors"
                >
                  Update
                </button>
              </div>
            </form>
          )}
        </div>
        
      </div>
    </div>
  );
}
