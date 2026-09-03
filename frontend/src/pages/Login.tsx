import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [mode, setMode] = useState<'landing' | 'signin' | 'signup'>('landing');
  const navigate = useNavigate();
  
  const [isAnimationPlaying, setIsAnimationPlaying] = useState(true);

  // Form states for Signup
  const [signupUsername, setSignupUsername] = useState('');
  const [signupPassword, setSignupPassword] = useState('');
  const [signupConfirm, setSignupConfirm] = useState('');

  // Form states for Signin
  const [signinUsername, setSigninUsername] = useState('');
  const [signinPassword, setSigninPassword] = useState('');

  const handleModeChange = (newMode: 'signin' | 'signup') => {
    setMode(newMode);
    setIsAnimationPlaying(false);
  };

  const handleSigninSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const savedUsername = localStorage.getItem('registeredUsername');
    const savedPassword = localStorage.getItem('registeredPassword');

    if (savedUsername && savedUsername === signinUsername && savedPassword === signinPassword) {
      navigate('/dashboard');
    } else {
      alert("Invalid username or password!");
    }
  };

  const handleSignupSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (signupPassword !== signupConfirm) {
      alert("Re-enter password was not match");
      return;
    }
    
    // Save to local storage for realistic prototyping
    localStorage.setItem('registeredUsername', signupUsername);
    localStorage.setItem('registeredPassword', signupPassword);
    
    alert("Profile created successfully! Please sign in with your new credentials.");
    
    // Clear signin forms just in case and swap to signin mode
    setSigninUsername(signupUsername);
    setSigninPassword('');
    setMode('signin');
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-gray-900 flex flex-col items-center justify-center">
      
      <div 
        className={`absolute inset-0 z-0 transition-opacity duration-1000 ${isAnimationPlaying ? 'animate-gradient-x opacity-100' : 'opacity-30'}`}
        style={{
          background: 'linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab)',
          backgroundSize: '400% 400%',
          animationPlayState: isAnimationPlaying ? 'running' : 'paused'
        }}
      />
      
      <div className="absolute inset-0 z-0 bg-black/40" />

      <div className="relative z-10 w-full max-w-md p-8 flex flex-col items-center">
        
        <h1 className="text-5xl font-extrabold text-white mb-2 tracking-wider">THINK BIG</h1>
        <p className="text-gray-200 mb-12 text-center">Accelerate your research today.</p>

        {mode === 'landing' && (
          <div className="flex space-x-6 w-full animate-fade-in-up">
            <button 
              onClick={() => handleModeChange('signin')}
              className="flex-1 bg-white text-indigo-900 py-3 rounded-full font-bold text-lg hover:bg-gray-100 transition-colors shadow-lg cursor-pointer"
            >
              Sign In
            </button>
            <button 
              onClick={() => handleModeChange('signup')}
              className="flex-1 bg-indigo-600 text-white py-3 rounded-full font-bold text-lg hover:bg-indigo-700 transition-colors shadow-lg cursor-pointer border border-indigo-500"
            >
              Sign Up
            </button>
          </div>
        )}

        {mode === 'signin' && (
          <div className="w-full bg-white/10 backdrop-blur-md p-8 rounded-2xl shadow-2xl border border-white/20 animate-fade-in">
            <h2 className="text-2xl font-bold text-white mb-6 text-center">Welcome Back</h2>
            <form onSubmit={handleSigninSubmit} className="space-y-4">
              <div>
                <label className="block text-gray-200 text-sm font-medium mb-1">Username</label>
                <input 
                  type="text" 
                  required 
                  value={signinUsername}
                  onChange={(e) => setSigninUsername(e.target.value)}
                  className="w-full bg-white/20 border border-white/30 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white/50" 
                  placeholder="Enter your username" 
                />
              </div>
              <div>
                <label className="block text-gray-200 text-sm font-medium mb-1">Password</label>
                <input 
                  type="password" 
                  required 
                  value={signinPassword}
                  onChange={(e) => setSigninPassword(e.target.value)}
                  className="w-full bg-white/20 border border-white/30 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white/50" 
                  placeholder="Enter your password" 
                />
              </div>
              <button type="submit" className="w-full bg-indigo-600 text-white py-3 rounded-lg font-bold text-lg hover:bg-indigo-700 transition-colors mt-6 shadow-lg cursor-pointer">
                Login
              </button>
              <button type="button" onClick={() => { setMode('landing'); setIsAnimationPlaying(true); }} className="w-full text-gray-300 text-sm mt-4 hover:text-white cursor-pointer">
                ← Back
              </button>
            </form>
          </div>
        )}

        {mode === 'signup' && (
          <div className="w-full bg-white/10 backdrop-blur-md p-8 rounded-2xl shadow-2xl border border-white/20 animate-fade-in">
            <h2 className="text-2xl font-bold text-white mb-6 text-center">Create Account</h2>
            <form onSubmit={handleSignupSubmit} className="space-y-4">
              <div>
                <label className="block text-gray-200 text-sm font-medium mb-1">Username</label>
                <input 
                  type="text" 
                  required 
                  value={signupUsername}
                  onChange={(e) => setSignupUsername(e.target.value)}
                  className="w-full bg-white/20 border border-white/30 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white/50" 
                  placeholder="Choose a username" 
                />
              </div>
              <div>
                <label className="block text-gray-200 text-sm font-medium mb-1">Enter Password</label>
                <input 
                  type="password" 
                  required 
                  value={signupPassword}
                  onChange={(e) => setSignupPassword(e.target.value)}
                  className="w-full bg-white/20 border border-white/30 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white/50" 
                  placeholder="Create a password" 
                />
              </div>
              <div>
                <label className="block text-gray-200 text-sm font-medium mb-1">Re-enter Password</label>
                <input 
                  type="password" 
                  required 
                  value={signupConfirm}
                  onChange={(e) => setSignupConfirm(e.target.value)}
                  className="w-full bg-white/20 border border-white/30 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white/50" 
                  placeholder="Confirm your password" 
                />
              </div>
              <button type="submit" className="w-full bg-indigo-600 text-white py-3 rounded-lg font-bold text-lg hover:bg-indigo-700 transition-colors mt-6 shadow-lg cursor-pointer">
                Register
              </button>
              <button type="button" onClick={() => { setMode('landing'); setIsAnimationPlaying(true); }} className="w-full text-gray-300 text-sm mt-4 hover:text-white cursor-pointer">
                ← Back
              </button>
            </form>
          </div>
        )}

      </div>
    </div>
  );
}
