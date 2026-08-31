import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Overview from './pages/Overview';
import LiveActivity from './pages/LiveActivity';
import Conflicts from './pages/Conflicts';
import HumanReview from './pages/HumanReview';
import Transactions from './pages/Transactions';
import Decisions from './pages/Decisions';
import AuditTrail from './pages/AuditTrail';
import Policies from './pages/Policies';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/activity" element={<LiveActivity />} />
          <Route path="/conflicts" element={<Conflicts />} />
          <Route path="/reviews" element={<HumanReview />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/decisions" element={<Decisions />} />
          <Route path="/audit" element={<AuditTrail />} />
          <Route path="/policies" element={<Policies />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};
export default App;
