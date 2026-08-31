import React from 'react';
import clsx from 'clsx';

interface StatusBadgeProps {
  status: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const norm = status.toUpperCase();

  let styles = 'bg-slate-500/10 border-slate-500/20 text-slate-400';
  if (norm === 'ALLOW' || norm === 'COMPLETED' || norm === 'SUCCESS' || norm === 'RECOVERED' || norm === 'APPROVED') {
    styles = 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400';
  } else if (norm === 'REVIEW' || norm === 'PENDING' || norm === 'AWAITING_REVIEW' || norm === 'MODIFIED') {
    styles = 'bg-amber-500/10 border-amber-500/20 text-amber-400';
  } else if (norm === 'STOP' || norm === 'FAILED' || norm === 'BLOCKED' || norm === 'REJECTED') {
    styles = 'bg-red-500/10 border-red-500/20 text-red-400';
  } else if (norm === 'RUNNING') {
    styles = 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400 animate-pulse';
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
