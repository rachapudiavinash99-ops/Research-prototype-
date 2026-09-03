import React, { useState } from 'react';

export default function Dashboard() {
  const [profilePhoto, setProfilePhoto] = useState<string | null>(null);

  const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      // Create a local URL for the uploaded photo so we can display it
      const url = URL.createObjectURL(file);
      setProfilePhoto(url);
    }
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

        <label className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 font-medium cursor-pointer shadow-sm transition-colors w-full text-center">
          Upload Profile Photo
          <input 
            type="file" 
            className="hidden" 
            accept="image/*" 
            onChange={handlePhotoUpload} 
          />
        </label>
        
        <p className="text-sm text-gray-500 mt-4 text-center">
          Supported formats: JPEG, PNG, GIF, WebP.
        </p>

      </div>
    </div>
  );
}
