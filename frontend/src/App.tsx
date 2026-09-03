import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { Activity, BookOpen, Layers, LayoutDashboard, Settings } from "lucide-react";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import Prototypes from "./pages/Prototypes";
import PlaceholderPage from "./pages/Placeholder";

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-gray-100">
      <aside className="w-64 bg-white shadow-md">
        <div className="p-4 border-b">
          <h1 className="text-xl font-bold text-indigo-600">Prototype Hub</h1>
        </div>
        <nav className="p-4 space-y-2">
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
          <Link to="/experiments" className="flex items-center space-x-2 p-2 hover:bg-gray-50 rounded-md">
            <Activity size={20} />
            <span>Experiments</span>
          </Link>
          <Link to="/settings" className="flex items-center space-x-2 p-2 hover:bg-gray-50 rounded-md">
            <Settings size={20} />
            <span>Settings</span>
          </Link>
        </nav>
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
          <Route path="/experiments" element={<PlaceholderPage title="Experiments Module" />} />
          <Route path="/settings" element={<PlaceholderPage title="Settings" />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
