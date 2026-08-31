import React from 'react';
import clsx from 'clsx';

interface AgentBadgeProps {
  agentId: string;
}

export const AGENT_COLORS: Record<string, { bg: string, border: string, text: string }> = {
  SubscriptionRecoveryAgent: {
    bg: 'bg-indigo-500/10',
    border: 'border-indigo-500/20',
    text: 'text-indigo-400'
  },
  PaymentRecoveryAgent: {
    bg: 'bg-emerald-500/10',
    border: 'border-emerald-500/20',
    text: 'text-emerald-400'
  },
  CheckoutRecoveryAgent: {
    bg: 'bg-sky-500/10',
    border: 'border-sky-500/20',
    text: 'text-sky-400'
  },
  ReceivablesAgent: {
    bg: 'bg-violet-500/10',
    border: 'border-violet-500/20',
    text: 'text-violet-400'
  }
};

export const AgentBadge: React.FC<AgentBadgeProps> = ({ agentId }) => {
  const cleanName = agentId.replace('Agent', '');
  const colors = AGENT_COLORS[agentId] || {
    bg: 'bg-slate-500/10',
    border: 'border-slate-500/20',
    text: 'text-slate-400'
  };

  return (
    <span className={clsx(
      "px-2.5 py-1 rounded-md text-xs font-semibold border inline-flex items-center gap-1.5",
      colors.bg,
      colors.border,
      colors.text
    )}>
      {cleanName}
    </span>
  );
};
