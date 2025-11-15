import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import DocumentDetail from './pages/DocumentDetail';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/documents/:id" element={<DocumentDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
