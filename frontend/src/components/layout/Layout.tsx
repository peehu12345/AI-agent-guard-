import React from 'react';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';
import { DemoBanner } from '../ui/DemoBanner';

interface LayoutProps {
  children: React.ReactNode;
  onRefreshData?: () => void;
}

export const Layout: React.FC<LayoutProps> = ({ children, onRefreshData }) => {
  return (
    <div className="flex h-screen overflow-hidden bg-slate-950 text-slate-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <DemoBanner />
        <TopBar onRefreshData={onRefreshData} />
        <main className="flex-1 overflow-y-auto px-8 py-8">
          <div className="max-w-7xl mx-auto space-y-8 pb-16">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
export default Layout;
