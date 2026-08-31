import React from 'react';
import { AlertTriangle } from 'lucide-react';

export const DemoBanner: React.FC = () => {
  return (
    <div className="w-full bg-amber-500/10 border-b border-amber-500/20 px-4 py-2 text-center text-xs text-amber-400 font-medium flex items-center justify-center gap-2">
      <AlertTriangle className="w-4 h-4 animate-pulse text-amber-500" />
      <span>⚠️ SYNTHETIC DEMO DATA — All customers, transactions, and metrics are simulated. No real financial data is used.</span>
    </div>
  );
};
