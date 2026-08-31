import React, { useState, useEffect } from 'react';
import { Shield, Activity, Users, FileText } from 'lucide-react';
import api from '../services/api';
import { AgentBadge } from '../components/ui/AgentBadge';
import { StatusBadge } from '../components/ui/StatusBadge';
import { AgentFlowDiagram } from '../components/flow/AgentFlowDiagram';
import { formatCurrency, formatDateTime } from '../utils/formatters';

export const LiveActivity: React.FC = () => {
  const [agents, setAgents] = useState<any[]>([]);
  const [feed, setFeed] = useState<any[]>([]);
  const [conflicts, setConflicts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [agentRes, feedRes, confRes] = await Promise.all([
        api.getAgents(),
        api.getRecentActivity(),
        api.getConflicts()
      ]);
      setAgents(agentRes);
      setFeed(feedRes.slice(0, 15));
      setConflicts(confRes);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 8000);
    return () => clearInterval(interval);
  }, []);

  if (loading && agents.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <Activity className="w-8 h-8 text-indigo-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-slate-100">Live Agent Activity</h2>
        <p className="text-sm text-slate-400">Real-time supervision of active payment agent recommendations and policies.</p>
      </div>

      {/* Agents Strip */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {agents.map((agent) => (
          <div key={agent.id} className="glass-panel rounded-xl p-5 border border-slate-900 flex flex-col justify-between">
            <div className="flex justify-between items-start mb-3">
              <AgentBadge agentId={agent.agent_id} />
              <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded font-mono font-semibold">
                PRIORITY {agent.priority}
              </span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed mb-4">{agent.description}</p>
            <div className="flex justify-between items-center text-xs text-slate-500 border-t border-slate-900 pt-3">
              <span>Status</span>
              <span className="flex items-center gap-1.5 font-semibold text-emerald-400">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping"></span>
                ACTIVE
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Visual Centerpiece and Activity Feed Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* React Flow Visual Canvas */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold text-slate-200">Autonomous Governance Topology</h3>
            <span className="text-xs text-slate-400">Visual Left-to-Right Decision Stream</span>
          </div>
          <AgentFlowDiagram conflicts={conflicts} />
        </div>

        {/* Live Feed Sidebar */}
        <div className="glass-panel rounded-xl p-6 border border-slate-900 flex flex-col h-[450px]">
          <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-900">
            <FileText className="w-4 h-4 text-slate-400" />
            <h3 className="text-sm font-semibold text-slate-200">Real-time Control Log</h3>
          </div>
          <div className="flex-1 overflow-y-auto space-y-4 pr-2">
            {feed.map((event) => (
              <div key={event.id} className="border-b border-slate-900/60 pb-3 last:border-b-0 space-y-1.5">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-mono text-slate-400">{event.transaction_id || 'SYSTEM'}</span>
                  <span className="text-[10px] text-slate-500">{formatDateTime(event.created_at)}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold text-slate-300">
                    {event.event_type === 'CONFLICT' ? 'COLLISION' : 'DECISION'}
                  </span>
                  {event.policy_decision && (
                    <StatusBadge status={event.policy_decision} />
                  )}
                </div>
                <p className="text-xs text-slate-400 font-medium leading-relaxed">
                  {event.reason}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
export default LiveActivity;
