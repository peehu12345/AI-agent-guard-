import React from 'react';
import type { LucideIcon } from 'lucide-react';
import clsx from 'clsx';

interface MetricCardProps {
  icon: LucideIcon;
  label: string;
  value: string | number;
  glowColor?: 'primary' | 'success' | 'warning' | 'danger' | 'info';
  description?: string;
}

const glowStyles = {
  primary: 'border-indigo-500/20 shadow-[0_0_15px_rgba(99,102,241,0.15)]',
  success: 'border-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.15)]',
  warning: 'border-amber-500/20 shadow-[0_0_15px_rgba(245,158,11,0.15)]',
  danger: 'border-red-500/20 shadow-[0_0_15px_rgba(239,68,68,0.15)]',
  info: 'border-sky-500/20 shadow-[0_0_15px_rgba(14,165,233,0.15)]',
};

export const MetricCard: React.FC<MetricCardProps> = ({
  icon: Icon,
  label,
  value,
  glowColor = 'primary',
  description
}) => {
  return (
    <div className={clsx(
      "glass-panel rounded-xl p-6 transition-all duration-300 hover:scale-[1.02]",
      glowStyles[glowColor]
    )}>
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm font-medium text-slate-400">{label}</p>
          <p className="text-3xl font-bold font-mono text-slate-100 mt-2">{value}</p>
        </div>
        <div className={clsx(
          "p-2.5 rounded-lg border",
          glowColor === 'primary' && "bg-indigo-500/10 border-indigo-500/20 text-indigo-400",
          glowColor === 'success' && "bg-emerald-500/10 border-emerald-500/20 text-emerald-400",
          glowColor === 'warning' && "bg-amber-500/10 border-amber-500/20 text-amber-400",
          glowColor === 'danger' && "bg-red-500/10 border-red-500/20 text-red-400",
          glowColor === 'info' && "bg-sky-500/10 border-sky-500/20 text-sky-400"
        )}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      {description && (
        <p className="text-xs text-slate-400 mt-4 border-t border-slate-800/60 pt-3">
          {description}
        </p>
      )}
    </div>
  );
};
