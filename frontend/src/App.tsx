import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { BookOpen, Layers, LayoutDashboard, LogOut } from "lucide-react";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import Prototypes from "./pages/Prototypes";

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-gray-100">
      <aside className="w-64 bg-white shadow-md flex flex-col">
        <div className="p-4 border-b">
          <h1 className="text-xl font-bold text-indigo-600">Prototype Hub</h1>
        </div>
        <nav className="p-4 space-y-2 flex-grow">
          <Link to="/" className="flex items-center space-x-2 p-2 hover:bg-gray-50 rounded-md">
            <LayoutDashboard size={20} />
            <span>Dashboard</span>
          </Link>
          <Link to="/projects" className="flex items-center space-x-2 p-2 hover:bg-gray-50 rounded-md">
            <BookOpen size={20} />
            <span>Projects</span>
          </Link>
          <Link to="/prototypes" className="flex items-center space-x-2 p-2 hover:bg-gray-50 rounded-md">
            <Layers size={20} />
            <span>Prototypes</span>
          </Link>
        </nav>
        <div className="p-4 border-t">
          <button 
            onClick={() => alert("Logged out successfully!")} 
            className="flex items-center space-x-2 p-2 hover:bg-red-50 text-red-600 rounded-md w-full text-left font-medium transition-colors cursor-pointer"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>
      <main className="flex-1 p-8 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/prototypes" element={<Prototypes />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
