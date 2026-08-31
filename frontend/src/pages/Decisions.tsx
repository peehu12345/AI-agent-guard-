import React, { useState, useEffect } from 'react';
import { Activity } from 'lucide-react';
import api from '../services/api';
import { StatusBadge } from '../components/ui/StatusBadge';
import { RiskBadge } from '../components/ui/RiskBadge';
import { formatCurrency, formatDateTime } from '../utils/formatters';

export const Decisions: React.FC = () => {
  const [decisions, setDecisions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getDecisions()
      .then(data => setDecisions(data))
      .catch(e => console.error(e))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Activity className="w-8 h-8 text-indigo-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-slate-100">Decision Outcomes Log</h2>
        <p className="text-sm text-slate-400">Ledger of all AgentGuard policy evaluations, final actions and recovery values.</p>
      </div>

      <div className="glass-panel rounded-xl overflow-hidden border border-slate-900">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-900 bg-slate-900/10 text-xs text-slate-400 uppercase font-semibold">
                <th className="p-4">Tx ID</th>
                <th className="p-4">Customer</th>
                <th className="p-4">AI Rec.</th>
                <th className="p-4">Policy Intercept</th>
                <th className="p-4">Final Action</th>
                <th className="p-4">Execution Status</th>
                <th className="p-4">Recovered Amt</th>
                <th className="p-4">Outcome Justification</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40 text-sm">
              {decisions.map((d) => (
                <tr key={d.id} className="hover:bg-slate-900/10">
                  <td className="p-4 font-mono text-slate-300 font-semibold">{d.transaction_id}</td>
                  <td className="p-4 font-mono text-slate-400">{d.customer_id}</td>
                  <td className="p-4 font-mono text-xs text-indigo-400">{d.ai_recommended_action}</td>
                  <td className="p-4"><StatusBadge status={d.policy_decision} /></td>
                  <td className="p-4 font-mono text-xs text-slate-200 font-semibold">{d.final_action}</td>
                  <td className="p-4"><StatusBadge status={d.execution_status} /></td>
                  <td className="p-4 font-mono text-emerald-400 font-semibold">{formatCurrency(d.recovered_amount)}</td>
                  <td className="p-4 text-xs text-slate-400 max-w-sm truncate">{d.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
export default Decisions;
