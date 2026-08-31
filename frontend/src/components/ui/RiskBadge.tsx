import React from 'react';
import clsx from 'clsx';

interface RiskBadgeProps {
  risk: string;
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ risk }) => {
  const norm = risk.toUpperCase();

  let styles = 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400';
  if (norm === 'MEDIUM') {
    styles = 'bg-amber-500/10 border-amber-500/20 text-amber-400';
  } else if (norm === 'HIGH') {
    styles = 'bg-red-500/10 border-red-500/20 text-red-400';
  } else if (norm === 'CRITICAL') {
    styles = 'bg-red-500/20 border-red-500/30 text-red-400 animate-pulse font-bold shadow-[0_0_10px_rgba(239,68,68,0.2)]';
  }

  return (
    <span className={clsx(
      "px-2.5 py-1 rounded-md text-xs font-semibold border inline-flex items-center gap-1.5",
      styles
    )}>
      {norm}
    </span>
  );
};
