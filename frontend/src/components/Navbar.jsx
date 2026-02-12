import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/">PipDynamics</Link>
      </div>

      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/markets">Markets</Link>
        <Link to="/dashboard">Dashboard</Link>
      </div>
    </nav>
  );
}
