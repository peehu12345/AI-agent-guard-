import React, { useState, useEffect } from 'react';
import { Users, Check, X, Edit3, MessageSquare } from 'lucide-react';
import api from '../services/api';
import { StatusBadge } from '../components/ui/StatusBadge';
import { formatCurrency, formatDateTime } from '../utils/formatters';

export const HumanReview: React.FC = () => {
  const [reviews, setReviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [notesMap, setNotesMap] = useState<Record<string, string>>({});
  const [modifiedActionMap, setModifiedActionMap] = useState<Record<string, string>>({});

  const fetchReviews = async () => {
    try {
      const data = await api.getReviews();
      setReviews(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  const handleAction = async (id: string, action: 'APPROVE' | 'REJECT' | 'MODIFY') => {
    try {
      const notes = notesMap[id] || '';
      const modifiedAction = modifiedActionMap[id] || undefined;
      await api.processReview(id, action, notes, modifiedAction);
      fetchReviews(); // reload list
    } catch (e) {
      console.error(e);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Users className="w-8 h-8 text-indigo-500 animate-spin" />
      </div>
    );
  }

  const pendingReviews = reviews.filter(r => r.status === 'PENDING');
  const completedReviews = reviews.filter(r => r.status !== 'PENDING');

  const availableActions = ["RETRY_PAYMENT", "SEND_REMINDER", "SEND_MESSAGE", "OFFER_INCENTIVE", "ESCALATE_HUMAN", "STOP"];

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-slate-100">Human Review Queue</h2>
        <p className="text-sm text-slate-400">Manual verification queue for high-value risk alerts or low confidence advisor decisions.</p>
      </div>

      {/* Pending Reviews Queue */}
      <div className="space-y-6">
        <h3 className="text-lg font-semibold text-slate-200 flex items-center gap-2">
          <span>Pending Approvals</span>
          <span className="text-xs bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 px-2 py-0.5 rounded-full font-bold">
            {pendingReviews.length}
          </span>
        </h3>

        {pendingReviews.length === 0 ? (
          <div className="glass-panel rounded-xl p-8 text-center text-slate-500 border border-slate-900">
            All reviews processed. System is operating autonomously.
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {pendingReviews.map((r) => (
              <div key={r.id} className="glass-panel rounded-xl p-6 border border-slate-900 flex flex-col justify-between space-y-6">
                <div className="space-y-4">
                  <div className="flex justify-between items-start">
                    <div className="space-y-1">
                      <span className="text-xs text-slate-500 font-medium">Customer</span>
                      <p className="font-mono text-slate-200 text-sm font-semibold">{r.customer_id}</p>
                    </div>
                    <div className="space-y-1 text-right">
                      <span className="text-xs text-slate-500 font-medium">Tx ID</span>
                      <p className="font-mono text-slate-200 text-sm font-semibold">{r.transaction_id}</p>
                    </div>
                  </div>

                  <div className="bg-amber-500/5 border border-amber-500/10 rounded-lg p-3 text-xs text-amber-400 leading-relaxed font-medium">
                    Reason: {r.review_reason}
                  </div>

                  {/* Modify Selector */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs text-slate-400 font-medium">Override Action:</label>
                    <select
                      value={modifiedActionMap[r.id] || ''}
                      onChange={(e) => setModifiedActionMap({ ...modifiedActionMap, [r.id]: e.target.value })}
                      className="bg-slate-950 border border-slate-900 rounded px-3 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
                    >
                      <option value="">Choose modified action...</option>
                      {availableActions.map((act) => (
                        <option key={act} value={act}>{act}</option>
                      ))}
                    </select>
                  </div>

                  {/* Notes Area */}
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs text-slate-400 font-medium">Reviewer Justification Notes:</label>
                    <textarea
                      placeholder="Input decision reasons here..."
                      value={notesMap[r.id] || ''}
                      onChange={(e) => setNotesMap({ ...notesMap, [r.id]: e.target.value })}
                      rows={2}
                      className="bg-slate-950 border border-slate-900 rounded p-3 text-xs text-slate-300 focus:outline-none focus:border-indigo-500 resize-none"
                    />
                  </div>
                </div>

                <div className="flex items-center gap-3 border-t border-slate-900 pt-4">
                  <button
                    onClick={() => handleAction(r.id, 'APPROVE')}
                    className="flex-1 flex justify-center items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/20 hover:bg-emerald-500/20 text-emerald-400 py-2 rounded-lg text-xs font-semibold cursor-pointer"
                  >
                    <Check className="w-3.5 h-3.5" />
                    <span>Approve AI Recommendation</span>
                  </button>
                  <button
                    onClick={() => handleAction(r.id, 'REJECT')}
                    className="flex-1 flex justify-center items-center gap-1.5 bg-red-500/10 border border-red-500/20 hover:bg-red-500/20 text-red-400 py-2 rounded-lg text-xs font-semibold cursor-pointer"
                  >
                    <X className="w-3.5 h-3.5" />
                    <span>Block & Stop</span>
                  </button>
                  {modifiedActionMap[r.id] && (
                    <button
                      onClick={() => handleAction(r.id, 'MODIFY')}
                      className="flex-1 flex justify-center items-center gap-1.5 bg-indigo-500/10 border border-indigo-500/20 hover:bg-indigo-500/20 text-indigo-400 py-2 rounded-lg text-xs font-semibold cursor-pointer"
                    >
                      <Edit3 className="w-3.5 h-3.5" />
                      <span>Execute Modified</span>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* History Log */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-slate-200">Processed Reviews</h3>
        <div className="glass-panel rounded-xl overflow-hidden border border-slate-900">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-900 bg-slate-900/10 text-xs text-slate-400 uppercase font-semibold">
                  <th className="p-4">Customer</th>
                  <th className="p-4">Tx ID</th>
                  <th className="p-4">Decision Status</th>
                  <th className="p-4">Justification Notes</th>
                  <th className="p-4">Reviewed At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40 text-sm">
                {completedReviews.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-900/10">
                    <td className="p-4 font-mono text-slate-300">{r.customer_id}</td>
                    <td className="p-4 font-mono text-slate-300">{r.transaction_id}</td>
                    <td className="p-4"><StatusBadge status={r.status} /></td>
                    <td className="p-4 text-xs text-slate-400 max-w-xs truncate">{r.reviewer_notes || 'N/A'}</td>
                    <td className="p-4 text-xs text-slate-500">{formatDateTime(r.reviewed_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
export default HumanReview;
