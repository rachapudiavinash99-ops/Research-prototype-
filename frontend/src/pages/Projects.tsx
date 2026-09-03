import React, { useEffect, useState } from 'react';

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
    const saved = localStorage.getItem('local_projects');
    if (saved) {
      setProjects(JSON.parse(saved));
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const saveProjects = (updatedProjects: Project[]) => {
    setProjects(updatedProjects);
    localStorage.setItem('local_projects', JSON.stringify(updatedProjects));
  };

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    const projectToSave: Project = {
      id: Date.now(),
      name: newProject.name,
      description: newProject.description,
      status: newProject.status
    };
    saveProjects([projectToSave, ...projects]);
    setShowForm(false);
    setNewProject({ name: '', description: '', status: 'active' });
    alert("Successfully created project!");
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      const projectToSave: Project = {
        id: Date.now(),
        name: `Imported: ${file.name}`,
        description: `Automatically generated project from imported file. Size: ${(file.size / 1024).toFixed(2)} KB.`,
        status: 'active'
      };
      saveProjects([projectToSave, ...projects]);
      alert(`Successfully imported ${file.name} and added it to your Projects list!`);
    }
  };

  const handleDelete = (id: number) => {
    if (confirm("Are you sure you want to delete this project?")) {
      const updated = projects.filter(p => p.id !== id);
      saveProjects(updated);
      alert("Successfully deleted project!");
    }
  };

  const handleDownload = (p: Project) => {
    const data = JSON.stringify(p, null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${p.name.replace(/\s+/g, "_")}_data.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
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
        <form onSubmit={handleCreate} className="bg-white p-6 rounded-lg shadow-sm border mb-6 animate-fade-in-up">
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
            <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 font-medium cursor-pointer">Save Project</button>
          </div>
        </form>
      )}
      
      {loading ? (
        <p>Loading projects...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map(p => (
            <div key={p.id} className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition-shadow flex flex-col">
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-bold text-lg leading-tight">{p.name}</h3>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${p.status === 'active' ? 'bg-green-100 text-green-800' : p.status === 'planning' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'}`}>
                  {p.status}
                </span>
              </div>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2 flex-grow">{p.description}</p>
              
              <div className="mt-4 pt-4 border-t flex justify-between items-center space-x-2">
                <button 
                  className="bg-indigo-50 text-indigo-600 px-3 py-1.5 rounded-md text-sm font-medium hover:bg-indigo-100 transition-colors flex-1 cursor-pointer" 
                  onClick={() => handleDownload(p)}
                >
                  Download
                </button>
                <button 
                  className="bg-red-50 text-red-600 px-3 py-1.5 rounded-md text-sm font-medium hover:bg-red-100 transition-colors flex-1 cursor-pointer" 
                  onClick={() => handleDelete(p.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
          {projects.length === 0 && !showForm && (
            <div className="col-span-full flex flex-col items-center justify-center h-48 border-2 border-dashed border-gray-300 rounded-xl text-gray-500 bg-gray-50">
              <p className="text-lg mb-2">No projects found.</p>
              <p className="text-sm">Click "+ New Project" or "Import Files" to get started!</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
