import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { Activity, BookOpen, Layers, LayoutDashboard, Settings } from "lucide-react";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";

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
          <a href="#" className="flex items-center space-x-2 p-2 hover:bg-gray-50 rounded-md">
            <Layers size={20} />
            <span>Prototypes</span>
          </a>
          <a href="#" className="flex items-center space-x-2 p-2 hover:bg-gray-50 rounded-md">
            <Activity size={20} />
            <span>Experiments</span>
          </a>
          <a href="#" className="flex items-center space-x-2 p-2 hover:bg-gray-50 rounded-md">
            <Settings size={20} />
            <span>Settings</span>
          </a>
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
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
