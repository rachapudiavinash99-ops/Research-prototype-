import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const navigate = useNavigate();
  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Research Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-gray-500 text-sm font-medium">Active Projects</h3>
          <p className="text-3xl font-bold mt-2">12</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-gray-500 text-sm font-medium">Total Prototypes</h3>
          <p className="text-3xl font-bold mt-2">48</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-gray-500 text-sm font-medium">Experiments Running</h3>
          <p className="text-3xl font-bold mt-2">5</p>
        </div>
      </div>
      <div className="mt-8 bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-bold mb-4">Recent Activity</h3>
        <ul className="space-y-4">
          <li className="flex items-center justify-between border-b pb-4">
            <div>
              <p className="font-medium">Alpha Version 2.0 Uploaded</p>
              <p className="text-sm text-gray-500">By Dr. Smith • 2 hours ago</p>
            </div>
            <button onClick={() => navigate('/prototypes')} className="px-4 py-2 bg-indigo-50 text-indigo-600 rounded-md text-sm font-medium hover:bg-indigo-100 transition-colors cursor-pointer">View</button>
          </li>
          <li className="flex items-center justify-between border-b pb-4">
            <div>
              <p className="font-medium">Quantum Simulator Trial Failed</p>
              <p className="text-sm text-gray-500">System • 5 hours ago</p>
            </div>
            <button onClick={() => navigate('/experiments')} className="px-4 py-2 bg-indigo-50 text-indigo-600 rounded-md text-sm font-medium hover:bg-indigo-100 transition-colors cursor-pointer">View</button>
          </li>
          <li className="flex items-center justify-between">
            <div>
              <p className="font-medium">New Project Created: Gene Therapy</p>
              <p className="text-sm text-gray-500">By Admin • 1 day ago</p>
            </div>
            <button onClick={() => navigate('/projects')} className="px-4 py-2 bg-indigo-50 text-indigo-600 rounded-md text-sm font-medium hover:bg-indigo-100 transition-colors cursor-pointer">View</button>
          </li>
        </ul>
      </div>
    </div>
  );
}
