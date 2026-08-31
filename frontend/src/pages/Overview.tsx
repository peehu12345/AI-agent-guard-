import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  AlertOctagon,
  Users,
  ShieldCheck,
  Ban,
  Activity,
  ArrowRight
} from 'lucide-react';
import { Link } from 'react-router-dom';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import api from '../services/api';
import { MetricCard } from '../components/ui/MetricCard';
import { StatusBadge } from '../components/ui/StatusBadge';
import { RiskBadge } from '../components/ui/RiskBadge';
import { formatCurrency, formatPercent } from '../utils/formatters';
import { DashboardKPIs } from '../types';

export const Overview: React.FC = () => {
  const [kpis, setKpis] = useState<DashboardKPIs | null>(null);
  const [decisions, setDecisions] = useState<any[]>([]);
  const [conflicts, setConflicts] = useState<any[]>([]);
  const [pieData, setPieData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [kpiRes, decRes, confRes, pieRes] = await Promise.all([
        api.getDashboardKPIs(),
        api.getDecisions(),
        api.getConflicts(),
        api.getDecisionBreakdown()
      ]);
      setKpis(kpiRes);
      setDecisions(decRes.slice(0, 5));
      setConflicts(confRes.slice(0, 3));

      // Handle pie chart styling
      const formattedPie = pieRes.map(item => {
        let color = '#10b981';
        if (item.name === 'REVIEW') color = '#f59e0b';
        if (item.name === 'STOP') color = '#ef4444';
        return { ...item, color };
      });
      setPieData(formattedPie);
    } catch (e) {
      console.error("Error loading dashboard data:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading && !kpis) {
    return (
      <div className="flex justify-center items-center h-64">
        <Activity className="w-8 h-8 text-indigo-500 animate-spin" />
      </div>
    );
  }

  // Sample recovery chart history data matching seed
  const historyData = [
    { name: 'Hour 1', AtRisk: 120000, Recovered: 45000 },
    { name: 'Hour 2', AtRisk: 340000, Recovered: 135000 },
    { name: 'Hour 3', AtRisk: 510000, Recovered: 240000 },
    { name: 'Hour 4', AtRisk: 2790960, Recovered: 135320 },
  ];

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-slate-100">Governance Dashboard</h2>
          <p className="text-sm text-slate-400">AI payment supervisor logs, conflict resolutions and hard policy compliance.</p>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard
          icon={AlertOctagon}
          label="Revenue At Risk"
          value={formatCurrency(kpis?.revenue_at_risk || 0)}
          glowColor="danger"
          description="Total value of outstanding failed transaction alerts."
        />
        <MetricCard
          icon={TrendingUp}
          label="Gross Revenue Recovered"
          value={formatCurrency(kpis?.gross_recovered || 0)}
          glowColor="success"
          description="Simulated recovery revenue through approved agent actions."
        />
        <MetricCard
          icon={ShieldCheck}
          label="Conflicts Prevented"
          value={kpis?.conflicts_detected || 0}
          glowColor="primary"
          description={`${kpis?.conflict_rate || 0}% of all transactions faced competing agent interventions.`}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
        <MetricCard
          icon={Ban}
          label="Unsafe Actions Blocked"
          value={kpis?.actions_stopped || 0}
          glowColor="danger"
          description={`${kpis?.policy_override_rate || 0}% of agent actions stopped by policy overrides.`}
        />
        <MetricCard
          icon={Users}
          label="Human Review Escorted"
          value={kpis?.reviews_pending || 0}
          glowColor="warning"
          description="Pending human override or approval in the review queue."
        />
        <MetricCard
          icon={Activity}
          label="Managed Customers"
          value={kpis?.total_customers || 0}
          glowColor="info"
          description="Total database synthetic client segments protected."
        />
      </div>

      {/* Charts section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recovery area chart */}
        <div className="lg:col-span-2 glass-panel rounded-xl p-6 border border-slate-900">
          <h3 className="text-lg font-semibold text-slate-200 mb-6">Recovery Pipeline Progress</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={historyData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorAtRisk" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorRecovered" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip contentStyle={{ backgroundColor: '#111827', borderColor: '#1e293b', color: '#f1f5f9' }} />
                <Area type="monotone" dataKey="AtRisk" stroke="#ef4444" fillOpacity={1} fill="url(#colorAtRisk)" name="At Risk" />
                <Area type="monotone" dataKey="Recovered" stroke="#10b981" fillOpacity={1} fill="url(#colorRecovered)" name="Recovered" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pie Breakdown */}
        <div className="glass-panel rounded-xl p-6 border border-slate-900 flex flex-col justify-between">
          <div>
            <h3 className="text-lg font-semibold text-slate-200 mb-2">Decision Outcomes</h3>
            <p className="text-xs text-slate-400 mb-6">Split of AgentGuard policy interventions.</p>
          </div>
          <div className="h-48 flex justify-center items-center">
            {pieData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#111827', borderColor: '#1e293b', color: '#f1f5f9' }} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-slate-500 text-sm">No decisions logged.</div>
            )}
          </div>
          <div className="space-y-2 mt-4">
            {pieData.map((entry, index) => (
              <div key={index} className="flex justify-between text-sm">
                <span className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.color }}></span>
                  <span className="text-slate-400 uppercase font-medium">{entry.name}</span>
                </span>
                <span className="font-mono text-slate-200">{entry.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Tables section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Conflicts */}
        <div className="glass-panel rounded-xl p-6 border border-slate-900">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg font-semibold text-slate-200">Recent Inter-Agent Collisions</h3>
            <Link to="/conflicts" className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1">
              <span>View All</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs text-slate-400 uppercase font-semibold">
                  <th className="pb-3">Customer ID</th>
                  <th className="pb-3">Type</th>
                  <th className="pb-3">Resolution Decision</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40 text-sm">
                {conflicts.map((c) => (
                  <tr key={c.id} className="hover:bg-slate-900/10">
                    <td className="py-3 font-mono text-slate-300">{c.customer_id}</td>
                    <td className="py-3 text-slate-400 text-xs font-semibold">{c.conflict_type.replace('_', ' ')}</td>
                    <td className="py-3 text-slate-400 max-w-xs truncate">{c.resolution_reason}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent Decisions */}
        <div className="glass-panel rounded-xl p-6 border border-slate-900">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg font-semibold text-slate-200">Recent Decision Outcomes</h3>
            <Link to="/decisions" className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1">
              <span>View All</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-xs text-slate-400 uppercase font-semibold">
                  <th className="pb-3">Tx ID</th>
                  <th className="pb-3">AI Action</th>
                  <th className="pb-3">Policy Intercept</th>
                  <th className="pb-3">Amount</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40 text-sm">
                {decisions.map((d) => (
                  <tr key={d.id} className="hover:bg-slate-900/10">
                    <td className="py-3 font-mono text-slate-300">{d.transaction_id}</td>
                    <td className="py-3 font-mono text-xs text-indigo-400">{d.ai_recommended_action}</td>
                    <td className="py-3"><StatusBadge status={d.policy_decision} /></td>
                    <td className="py-3 font-mono text-slate-300">{formatCurrency(d.recovered_amount || 0)}</td>
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
export default Overview;
