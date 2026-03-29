import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SwamijiPage from './pages/SwamijiPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/swamiji" element={<SwamijiPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
