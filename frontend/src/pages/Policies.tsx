import React, { useState, useEffect } from 'react';
import { ShieldAlert, Activity, CheckCircle, Ban } from 'lucide-react';
import api from '../services/api';
import { StatusBadge } from '../components/ui/StatusBadge';

export const Policies: React.FC = () => {
  const [policies, setPolicies] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchPolicies = async () => {
    try {
      const data = await api.getPolicies();
      setPolicies(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  const handleToggle = async (id: string) => {
    try {
      await api.togglePolicy(id);
      fetchPolicies(); // refresh list
    } catch (e) {
      console.error(e);
    }
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
        <h2 className="text-2xl font-bold tracking-tight text-slate-100">Deterministic Safety Guardrails</h2>
        <p className="text-sm text-slate-400">Manage rules governing autonomous recovery agent jurisdictions. LLMs advise, Policies decide.</p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {policies.map((p) => (
          <div key={p.id} className="glass-panel rounded-xl p-6 border border-slate-900 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div className="space-y-2 flex-1">
              <div className="flex items-center gap-3">
                <span className="font-semibold text-slate-200 text-sm">{p.name}</span>
                <span className={`text-[10px] px-2 py-0.5 rounded uppercase font-bold border ${
                  p.rule_type === 'HARD'
                    ? 'bg-red-500/10 border-red-500/20 text-red-400'
                    : 'bg-amber-500/10 border-amber-500/20 text-amber-400'
                }`}>
                  {p.rule_type} RULE
                </span>
                <span className="text-[10px] bg-slate-800 text-slate-500 px-2 py-0.5 rounded font-mono font-semibold">
                  TRIGGER: {p.action_on_trigger}
                </span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed font-medium">{p.description}</p>
              <div className="flex items-center gap-1.5 pt-2 text-[11px] font-mono text-slate-500">
                <span className="text-slate-600 font-semibold">Param Key:</span>
                <span className="text-slate-400">{p.parameter_key}</span>
                <span className="text-slate-600 ml-3 font-semibold">Param Value:</span>
                <span className="text-slate-400">{p.parameter_value}</span>
              </div>
            </div>

            <div className="flex items-center gap-4 border-l border-slate-900 pl-6 h-full min-w-[150px] justify-end">
              <button
                onClick={() => handleToggle(p.id)}
                className={`px-4 py-2 rounded-lg text-xs font-semibold border transition-all duration-200 cursor-pointer ${
                  p.is_active
                    ? 'bg-indigo-500/10 border-indigo-500/20 hover:bg-indigo-500/20 text-indigo-400'
                    : 'bg-slate-900 border-slate-800 text-slate-500'
                }`}
              >
                {p.is_active ? 'Active Guard' : 'Disabled Guard'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
export default Policies;
