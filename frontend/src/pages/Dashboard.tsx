import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [profilePhoto, setProfilePhoto] = useState<string | null>(null);

  useEffect(() => {
    const savedPhoto = localStorage.getItem('profilePhoto');
    if (savedPhoto) {
      setProfilePhoto(savedPhoto);
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
          alert("This image is too large to save permanently in your browser. It will disappear if you refresh.");
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemovePhoto = () => {
    setProfilePhoto(null);
    localStorage.removeItem('profilePhoto');
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
          <label className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 font-medium cursor-pointer shadow-sm transition-colors w-full text-center">
            Upload Profile Photo
            <input 
              type="file" 
              className="hidden" 
              accept="image/*" 
              onChange={handlePhotoUpload} 
            />
          </label>
        ) : (
          <div className="flex space-x-4 w-full">
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
        
        <p className="text-sm text-gray-500 mt-4 text-center">
          Supported formats: JPEG, PNG, GIF, WebP.
        </p>

      </div>
    </div>
  );
}
