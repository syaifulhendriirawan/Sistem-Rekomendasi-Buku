/**
 * App Component - Root component with routing
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RecommendationPage from './features/recommendations';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RecommendationPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
