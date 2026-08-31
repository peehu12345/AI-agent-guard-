import React, { useState, useEffect } from 'react';
import { Play, RotateCcw, Activity } from 'lucide-react';
import api from '../../services/api';

interface TopBarProps {
  onRefreshData?: () => void;
}

export const TopBar: React.FC<TopBarProps> = ({ onRefreshData }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [statusText, setStatusText] = useState('Idle');
  const [progress, setProgress] = useState(0);

  const checkStatus = async () => {
    try {
      const data = await api.getSimulationStatus();
      if (data.status === 'RUNNING') {
        setIsRunning(true);
        setStatusText(`Running (${data.processed_events}/${data.total_events})`);
        const pct = data.total_events > 0 ? (data.processed_events / data.total_events) * 100 : 0;
        setProgress(pct);
      } else {
        setIsRunning(false);
        setStatusText(data.status === 'COMPLETED' ? 'Completed' : 'Idle');
        setProgress(100);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    checkStatus();
    let timer: any = null;
    if (isRunning) {
      timer = setInterval(checkStatus, 1500);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [isRunning]);

  const handleStartSimulation = async () => {
    if (isRunning) return;
    try {
      setIsRunning(true);
      setStatusText('Starting...');
      setProgress(0);
      await api.runSimulation();
      if (onRefreshData) onRefreshData();
    } catch (e) {
      console.error(e);
      setIsRunning(false);
      setStatusText('Error');
    }
  };

  return (
    <header className="h-16 border-b border-slate-900 bg-slate-950/70 backdrop-blur px-8 flex justify-between items-center sticky top-0 z-40">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
          <span className="text-xs font-semibold uppercase tracking-wider text-emerald-400">System Live</span>
        </div>
      </div>
      <div className="flex items-center gap-4">
        {isRunning && (
          <div className="flex flex-col items-end gap-1">
            <span className="text-xs text-slate-400 font-semibold">{statusText}</span>
            <div className="w-32 h-1.5 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-indigo-500 transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        )}
        <button
          onClick={handleStartSimulation}
          disabled={isRunning}
          className="flex items-center gap-2 bg-gradient-to-r from-indigo-500 to-violet-600 hover:from-indigo-600 hover:to-violet-700 disabled:from-slate-800 disabled:to-slate-800 text-slate-100 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 shadow-[0_0_15px_rgba(99,102,241,0.2)] disabled:shadow-none cursor-pointer"
        >
          {isRunning ? (
            <>
              <Activity className="w-4 h-4 animate-spin" />
              <span>Simulating...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4" />
              <span>Run Simulation</span>
            </>
          )}
        </button>
      </div>
    </header>
  );
};
export default TopBar;
