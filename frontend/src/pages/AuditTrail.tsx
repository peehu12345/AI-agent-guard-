import React, { useState, useEffect } from 'react';
import { Activity, Shield, HelpCircle, ArrowRight } from 'lucide-react';
import api from '../services/api';
import { AgentBadge } from '../components/ui/AgentBadge';
import { StatusBadge } from '../components/ui/StatusBadge';
import { RiskBadge } from '../components/ui/RiskBadge';
import { formatCurrency, formatDateTime, formatConfidence } from '../utils/formatters';

export const AuditTrail: React.FC = () => {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    api.getRecentActivity()
      .then(data => setLogs(data))
      .catch(e => console.error(e))
      .finally(() => setLoading(false));
  }, []);

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

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
        <h2 className="text-2xl font-bold tracking-tight text-slate-100">Audit Trail Registry</h2>
        <p className="text-sm text-slate-400">Append-only compliance log tracing agent recommendations, AI advice and deterministic policy overrides.</p>
      </div>

      <div className="space-y-4">
        {logs.map((log) => {
          const isExpanded = expandedId === log.id;
          return (
            <div key={log.id} className="glass-panel rounded-xl overflow-hidden border border-slate-900 transition-all duration-300">
              <div
                onClick={() => toggleExpand(log.id)}
                className="p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 cursor-pointer hover:bg-slate-900/10 transition-colors select-none"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold font-mono text-xs">
                    {log.event_type === 'CONFLICT' ? 'CONF' : 'DEC'}
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-sm text-slate-200 font-semibold">{log.transaction_id || 'SYSTEM_RUN'}</span>
                      <span className="text-[10px] text-slate-500">{formatDateTime(log.created_at)}</span>
                    </div>
                    <p className="text-xs text-slate-400 leading-normal font-medium max-w-lg truncate">
                      {log.reason}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {log.policy_decision && <StatusBadge status={log.policy_decision} />}
                  <button className="text-xs font-semibold text-indigo-400">
                    {isExpanded ? 'Hide Trace' : 'Trace Pipeline'}
                  </button>
                </div>
              </div>

              {isExpanded && log.event_type !== 'CONFLICT' && (
                <div className="px-6 pb-6 pt-2 border-t border-slate-900/80 bg-slate-950/20 animate-fadeIn space-y-6">
                  <h4 className="text-xs font-bold uppercase text-slate-500 tracking-wider">Decision Chain Timeline</h4>

                  <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">
                    {/* Node 1: Recommendation */}
                    <div className="glass-panel bg-slate-950 rounded-xl p-4 border border-slate-900 space-y-2 relative">
                      <div className="flex justify-between items-center text-xs">
                        <span className="text-slate-500 font-semibold uppercase">1. Proposal</span>
                        {log.agent_ids && <AgentBadge agentId={log.agent_ids[0]} />}
                      </div>
                      <div className="space-y-1">
                        <span className="text-xs text-slate-500">Proposed Action:</span>
                        <p className="font-mono text-xs text-indigo-400 font-bold">{log.ai_recommendation}</p>
                      </div>
                      <div className="space-y-1">
                        <span className="text-xs text-slate-500">Alert Value:</span>
                        <p className="font-mono text-xs text-slate-200 font-semibold">{formatCurrency(log.amount || 0)}</p>
                      </div>
                    </div>

                    {/* Node 2: AI Supervisor */}
                    <div className="glass-panel bg-slate-950 rounded-xl p-4 border border-slate-900 space-y-2">
                      <span className="text-xs text-slate-500 font-semibold uppercase block">2. AI Advisor</span>
                      <div className="space-y-1">
                        <span className="text-xs text-slate-500">Confidence:</span>
                        <p className="font-mono text-xs text-slate-200 font-bold">{formatConfidence(log.ai_confidence || 0.85)}</p>
                      </div>
                      <div className="space-y-1">
                        <span className="text-xs text-slate-500">Risk Assessment:</span>
                        <div><RiskBadge risk={log.risk_level || 'MEDIUM'} /></div>
                      </div>
                    </div>

                    {/* Node 3: Policy Filter */}
                    <div className="glass-panel bg-slate-950 rounded-xl p-4 border border-slate-900 space-y-2">
                      <span className="text-xs text-slate-500 font-semibold uppercase block">3. Policy Engine</span>
                      <div className="space-y-1">
                        <span className="text-xs text-slate-500">Intercept:</span>
                        <div><StatusBadge status={log.policy_decision} /></div>
                      </div>
                      <div className="space-y-1">
                        <span className="text-xs text-slate-500">Triggers:</span>
                        <p className="text-xs text-slate-400 font-medium">{log.triggered_policies?.join(', ') || 'None'}</p>
                      </div>
                    </div>

                    {/* Node 4: Execution */}
                    <div className="glass-panel bg-slate-950 rounded-xl p-4 border border-slate-900 space-y-2">
                      <span className="text-xs text-slate-500 font-semibold uppercase block">4. Execution</span>
                      <div className="space-y-1">
                        <span className="text-xs text-slate-500">Final Action:</span>
                        <p className="font-mono text-xs text-indigo-400 font-bold">{log.final_action}</p>
                      </div>
                      <div className="space-y-1">
                        <span className="text-xs text-slate-500">Sim Result:</span>
                        <p className="font-mono text-xs text-emerald-400 font-bold">{log.execution_result || 'PENDING_REVIEW'}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
export default AuditTrail;
