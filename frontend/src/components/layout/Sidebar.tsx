import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Shield,
  LayoutDashboard,
  Activity,
  AlertTriangle,
  Users,
  CreditCard,
  CheckCircle,
  FileText,
  ShieldCheck
} from 'lucide-react';
import clsx from 'clsx';

export const Sidebar: React.FC = () => {
  const menuItems = [
    { label: 'Overview', path: '/', icon: LayoutDashboard },
    { label: 'Live Activity', path: '/activity', icon: Activity },
    { label: 'Agent Conflicts', path: '/conflicts', icon: AlertTriangle },
    { label: 'Human Review', path: '/reviews', icon: Users },
    { label: 'Transactions', path: '/transactions', icon: CreditCard },
    { label: 'Decisions', path: '/decisions', icon: CheckCircle },
    { label: 'Audit Trail', path: '/audit', icon: FileText },
    { label: 'Policies', path: '/policies', icon: ShieldCheck },
  ];

  return (
    <div className="w-64 bg-slate-950 border-r border-slate-900 flex flex-col h-screen sticky top-0">
      <div className="p-6 border-b border-slate-900 flex items-center gap-3">
        <div className="p-2 bg-indigo-500/10 rounded-lg border border-indigo-500/20 text-indigo-400">
          <Shield className="w-6 h-6 animate-pulse" />
        </div>
        <div>
          <h1 className="font-bold text-lg text-slate-100 tracking-tight leading-none">AgentGuard</h1>
          <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest mt-1 block">Control Tower</span>
        </div>
      </div>
      <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => clsx(
              "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200",
              isActive
                ? "bg-indigo-500/10 border-l-2 border-indigo-500 text-indigo-400"
                : "text-slate-400 hover:bg-slate-900/60 hover:text-slate-200"
            )}
          >
            <item.icon className="w-5 h-5" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-slate-900 text-center">
        <p className="text-[10px] text-slate-600 font-semibold tracking-wider uppercase">AgentGuard v1.0.0</p>
      </div>
    </div>
  );
};
export default Sidebar;
