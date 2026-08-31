import React, { useState, useEffect } from 'react';
import { AlertTriangle, ShieldCheck, HelpCircle } from 'lucide-react';
import api from '../services/api';
import { AgentBadge } from '../components/ui/AgentBadge';
import { formatDateTime } from '../utils/formatters';

export const Conflicts: React.FC = () => {
  const [conflicts, setConflicts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const fetchConflicts = async () => {
    try {
      const data = await api.getConflicts();
      setConflicts(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConflicts();
  }, []);

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <AlertTriangle className="w-8 h-8 text-indigo-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-slate-100">Agent Conflicts</h2>
        <p className="text-sm text-slate-400">Governance log of competing agent recommendations intercepted and resolved by priority routing rules.</p>
      </div>

      <div className="glass-panel rounded-xl overflow-hidden border border-slate-900">
        <div className="p-6 border-b border-slate-900 bg-slate-900/20">
          <h3 className="text-base font-semibold text-slate-200">Collision Log</h3>
        </div>

        {conflicts.length === 0 ? (
          <div className="p-8 text-center text-slate-500 flex flex-col items-center gap-2">
            <ShieldCheck className="w-8 h-8 text-emerald-500" />
            <p>No conflicts detected yet. Run the simulation to trigger collisions.</p>
          </div>
        ) : (
          <div className="divide-y divide-slate-800/60">
            {conflicts.map((c) => {
              const isExpanded = expandedId === c.id;
              return (
                <div key={c.id} className="p-6 space-y-4 hover:bg-slate-900/10 transition-colors">
                  <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2.5">
                        <span className="font-mono text-slate-200 text-sm font-semibold">{c.customer_id}</span>
                        <span className="text-[10px] bg-red-500/10 border border-red-500/20 text-red-400 px-2 py-0.5 rounded uppercase font-semibold tracking-wider">
                          {c.conflict_type.replace('_', ' ')}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 font-medium">
                        Logged on {formatDateTime(c.created_at)}
                      </p>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="flex flex-wrap gap-1.5 items-center">
                        <span className="text-xs text-slate-500 mr-1">Contenders:</span>
                        {c.conflicting_agent_ids.map((agent: string, idx: number) => (
                          <AgentBadge key={idx} agentId={agent} />
                        ))}
                      </div>
                      <button
                        onClick={() => toggleExpand(c.id)}
                        className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold cursor-pointer"
                      >
                        {isExpanded ? 'Hide Details' : 'Resolve Details'}
                      </button>
                    </div>
                  </div>

                  {isExpanded && (
                    <div className="bg-slate-950/40 rounded-xl p-5 border border-slate-900 grid grid-cols-1 md:grid-cols-2 gap-6 animate-fadeIn">
                      <div className="space-y-3 border-r border-slate-900 pr-6">
                        <h4 className="text-xs font-semibold uppercase text-emerald-400 tracking-wider">Resolution Outcome</h4>
                        <div className="space-y-2">
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-slate-500">Winner:</span>
                            <AgentBadge agentId={c.winning_agent_id} />
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-slate-500">Action:</span>
                            <span className="text-xs font-mono text-emerald-400 font-semibold bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                              {c.winning_action}
                            </span>
                          </div>
                          <p className="text-xs text-slate-400 leading-relaxed font-medium">
                            {c.resolution_reason}
                          </p>
                        </div>
                      </div>

                      <div className="space-y-3">
                        <h4 className="text-xs font-semibold uppercase text-red-400 tracking-wider">Blocked Competitors</h4>
                        <div className="space-y-3">
                          {c.blocked_actions.map((blocked: any, idx: number) => (
                            <div key={idx} className="bg-slate-950/60 rounded-lg p-3 border border-slate-900 space-y-1">
                              <div className="flex justify-between items-center">
                                <AgentBadge agentId={blocked.agent_id} />
                                <span className="text-[10px] font-mono text-red-400 bg-red-500/10 px-1.5 py-0.5 rounded border border-red-500/20">
                                  {blocked.action}
                                </span>
                              </div>
                              <p className="text-[11px] text-slate-400 leading-normal">
                                {blocked.reason}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
export default Conflicts;
