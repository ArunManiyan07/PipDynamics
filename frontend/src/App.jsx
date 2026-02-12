import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Markets from "./pages/Markets";
import Dashboard from "./pages/Dashboard";
import Navbar from "./components/Navbar";
import { AppProvider } from "./context/AppContext";
import "./App.css";

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/markets" element={<Markets />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
    </AppProvider>
  );
}
