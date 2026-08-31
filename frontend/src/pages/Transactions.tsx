import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { CreditCard, Activity } from 'lucide-react';
import { StatusBadge } from '../components/ui/StatusBadge';
import { RiskBadge } from '../components/ui/RiskBadge';
import { formatCurrency, formatDateTime, formatPercent } from '../utils/formatters';

export const Transactions: React.FC = () => {
  const [txns, setTxns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/transactions')
      .then(res => setTxns(res.data || []))
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
        <h2 className="text-2xl font-bold tracking-tight text-slate-100">Failed Transactions Registry</h2>
        <p className="text-sm text-slate-400">Ledger of all payment failures imported into AgentGuard simulation pipeline.</p>
      </div>

      <div className="glass-panel rounded-xl overflow-hidden border border-slate-900">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-900 bg-slate-900/10 text-xs text-slate-400 uppercase font-semibold">
                <th className="p-4">Tx ID</th>
                <th className="p-4">Customer</th>
                <th className="p-4">Amount</th>
                <th className="p-4">Status</th>
                <th className="p-4">Retry Index</th>
                <th className="p-4">Recovery Prob.</th>
                <th className="p-4">Risk Category</th>
                <th className="p-4">Failed Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40 text-sm">
              {txns.map((t) => (
                <tr key={t.id} className="hover:bg-slate-900/10">
                  <td className="p-4 font-mono text-slate-300 font-semibold">{t.transaction_id}</td>
                  <td className="p-4 font-mono text-slate-400">{t.customer_id}</td>
                  <td className="p-4 font-mono text-slate-200">{formatCurrency(t.amount)}</td>
                  <td className="p-4"><StatusBadge status={t.status} /></td>
                  <td className="p-4 font-mono text-slate-400">{t.retry_count} / 2</td>
                  <td className="p-4 font-mono text-indigo-400 font-semibold">{formatPercent(t.recovery_probability)}</td>
                  <td className="p-4"><RiskBadge risk={t.risk_level} /></td>
                  <td className="p-4 text-xs text-slate-500">{formatDateTime(t.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
export default Transactions;
