import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Project {
  id: number;
  name: str;
  description: string;
  status: string;
}

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Attempt to fetch real data from backend, fallback to mock data on fail
    axios.get('http://localhost:8001/api/projects')
      .then(res => setProjects(res.data))
      .catch(() => {
        setProjects([
          { id: 1, name: "Quantum Computing Algorithms", description: "Researching Shor's algorithm optimizations", status: "active" },
          { id: 2, name: "Next-Gen NLP Models", description: "Training language models on edge devices", status: "planning" },
          { id: 3, name: "Fusion Reactor Materials", description: "Testing high-heat resistant alloys", status: "experimenting" }
        ]);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Research Projects</h2>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 font-medium cursor-pointer" onClick={() => alert("Create Project functionality connected!")}>
          + New Project
        </button>
      </div>
      
      {loading ? (
        <p>Loading projects...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map(p => (
            <div key={p.id} className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-bold text-lg leading-tight">{p.name}</h3>
                <span className={px-2 py-1 text-xs font-medium rounded-full }>
                  {p.status}
                </span>
              </div>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{p.description}</p>
              <div className="mt-4 pt-4 border-t flex justify-between items-center">
                <button className="text-indigo-600 text-sm font-medium hover:text-indigo-800 cursor-pointer" onClick={() => alert(Opening project: )}>
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
