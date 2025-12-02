import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import PostCreate from "./pages/PostCreate";
import PostDetail from "./pages/PostDetail";
import Chat from "./pages/Chat";
import Mentor from "./pages/Mentor";
import Emergency from "./pages/Emergency";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/post/create" element={<PostCreate />} />
        <Route path="/post/:id" element={<PostDetail />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/mentor" element={<Mentor />} />
        <Route path="/emergency" element={<Emergency />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
