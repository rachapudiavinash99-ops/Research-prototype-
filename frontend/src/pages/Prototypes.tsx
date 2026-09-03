import React, { useState, useEffect } from 'react';

interface Idea {
  id: string;
  content: string;
  createdAt: string;
}

export default function Prototypes() {
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentNote, setCurrentNote] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('prototype_ideas');
    if (saved) {
      setIdeas(JSON.parse(saved));
    }
  }, []);

  const saveIdeas = (newIdeas: Idea[]) => {
    setIdeas(newIdeas);
    localStorage.setItem('prototype_ideas', JSON.stringify(newIdeas));
  };

  const handleSave = () => {
    if (!currentNote.trim()) return;

    if (editingId) {
      const updated = ideas.map(idea => 
        idea.id === editingId ? { ...idea, content: currentNote } : idea
      );
      saveIdeas(updated);
    } else {
      const newIdea: Idea = {
        id: Date.now().toString(),
        content: currentNote,
        createdAt: new Date().toLocaleString()
      };
      saveIdeas([newIdea, ...ideas]);
    }
    
    setIsEditing(false);
    setCurrentNote('');
    setEditingId(null);
  };

  const handleEdit = (idea: Idea) => {
    setCurrentNote(idea.content);
    setEditingId(idea.id);
    setIsEditing(true);
  };

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this idea?')) {
      const updated = ideas.filter(idea => idea.id !== id);
      saveIdeas(updated);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Prototype Ideas</h2>
        {!isEditing && (
          <button 
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 font-medium shadow-sm transition-colors cursor-pointer"
            onClick={() => setIsEditing(true)}
          >
            + Add Your Ideas
          </button>
        )}
      </div>

      {isEditing && (
        <div className="bg-white p-6 rounded-xl shadow-md border mb-8 animate-fade-in">
          <h3 className="text-lg font-bold mb-4 text-gray-800 flex items-center">
            📝 {editingId ? 'Edit Idea' : 'Notepad'}
          </h3>
          <textarea
            className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none bg-yellow-50/50 mb-4 font-mono text-sm shadow-inner"
            placeholder="Write your prototype ideas, rough notes, or brainstorming thoughts here..."
            value={currentNote}
            onChange={(e) => setCurrentNote(e.target.value)}
            autoFocus
          />
          <div className="flex justify-end space-x-3">
            <button 
              className="px-4 py-2 text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-md font-medium cursor-pointer transition-colors"
              onClick={() => {
                setIsEditing(false);
                setCurrentNote('');
                setEditingId(null);
              }}
            >
              Cancel
            </button>
            <button 
              className="px-4 py-2 bg-green-600 text-white hover:bg-green-700 rounded-md font-medium cursor-pointer shadow-sm transition-colors"
              onClick={handleSave}
            >
              Save Note
            </button>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {ideas.map((idea) => (
          <div key={idea.id} className="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow flex flex-col h-64">
            <div className="text-xs text-gray-400 mb-3 border-b pb-2 flex justify-between">
              <span>Saved on:</span>
              <span className="font-medium">{idea.createdAt}</span>
            </div>
            <div className="flex-grow overflow-y-auto mb-4 bg-yellow-50/50 p-4 rounded-lg border border-yellow-100 shadow-inner">
              <p className="text-gray-800 whitespace-pre-wrap text-sm leading-relaxed">{idea.content}</p>
            </div>
            <div className="flex space-x-2 mt-auto">
              <button 
                className="bg-indigo-50 text-indigo-700 px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-100 flex-1 cursor-pointer transition-colors"
                onClick={() => handleEdit(idea)}
              >
                Edit
              </button>
              <button 
                className="bg-red-50 text-red-600 px-3 py-2 rounded-md text-sm font-medium hover:bg-red-100 flex-1 cursor-pointer transition-colors"
                onClick={() => handleDelete(idea.id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
        {ideas.length === 0 && !isEditing && (
          <div className="col-span-full flex flex-col items-center justify-center h-48 border-2 border-dashed border-gray-300 rounded-xl text-gray-500 bg-gray-50">
            <p className="text-lg mb-2">No ideas recorded yet.</p>
            <p className="text-sm">Click "+ Add Your Ideas" to open the notepad and start brainstorming!</p>
          </div>
        )}
      </div>
    </div>
  );
}
