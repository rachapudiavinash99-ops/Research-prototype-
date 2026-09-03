import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Project {
  id: number;
  name: string;
  description: string;
  status: string;
}

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [newProject, setNewProject] = useState({ name: '', description: '', status: 'active' });

  const fetchProjects = () => {
    setLoading(true);
    axios.get('http://localhost:8001/api/projects')
      .then(res => setProjects(res.data))
      .catch(() => {
        console.error("Failed to fetch projects");
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8001/api/projects', newProject);
      setShowForm(false);
      setNewProject({ name: '', description: '', status: 'active' });
      fetchProjects();
    } catch (err) {
      alert("Failed to create project");
    }
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      try {
        await axios.post('http://localhost:8001/api/projects', {
          name: `Imported: ${file.name}`,
          description: `Automatically generated project from imported file. Size: ${(file.size / 1024).toFixed(2)} KB.`,
          status: 'active'
        });
        fetchProjects();
        alert(`Successfully imported ${file.name} and added it to your Projects list!`);
      } catch (err) {
        alert("Failed to import file as project");
      }
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Research Projects</h2>
        <div className="flex space-x-3">
          <label className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 font-medium cursor-pointer flex items-center">
            Import Files
            <input 
              type="file" 
              className="hidden" 
              multiple 
              onChange={handleImport} 
            />
          </label>
          <button 
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 font-medium cursor-pointer" 
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? 'Cancel' : '+ New Project'}
          </button>
        </div>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="bg-white p-6 rounded-lg shadow-sm border mb-6">
          <h3 className="font-bold mb-4">Create New Project</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Project Name</label>
              <input type="text" required value={newProject.name} onChange={e => setNewProject({...newProject, name: e.target.value})} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <textarea required value={newProject.description} onChange={e => setNewProject({...newProject, description: e.target.value})} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2" />
            </div>
            <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 font-medium">Save Project</button>
          </div>
        </form>
      )}
      
      {loading ? (
        <p>Loading projects...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map(p => (
            <div key={p.id} className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-bold text-lg leading-tight">{p.name}</h3>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${p.status === 'active' ? 'bg-green-100 text-green-800' : p.status === 'planning' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'}`}>
                  {p.status}
                </span>
              </div>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{p.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
