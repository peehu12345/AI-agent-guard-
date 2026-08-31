import axios from 'axios';
import type {
  Agent,
  Conflict,
  Decision,
  Policy,
  HumanReview,
  DashboardKPIs
} from '../types';

const client = axios.create({
  baseURL: '', // Proxied via Vite config to localhost:8000
});

export const api = {
  // Analytics
  getDashboardKPIs: () => client.get<DashboardKPIs>('/api/analytics/dashboard').then(res => res.data),
  getDecisionBreakdown: () => client.get<Array<{ name: string; value: number }>>('/api/analytics/decision-breakdown').then(res => res.data),
  getAgentPerformance: () => client.get<any[]>('/api/analytics/agent-performance').then(res => res.data),
  getPolicyTriggers: () => client.get<any[]>('/api/analytics/policy-triggers').then(res => res.data),
  getRiskDistribution: () => client.get<any[]>('/api/analytics/risk-distribution').then(res => res.data),
  getRecentActivity: () => client.get<any[]>('/api/analytics/recent-activity').then(res => res.data),

  // Simulation
  runSimulation: () => client.post<{ message: string; status: string }>('/api/simulation/run').then(res => res.data),
  getSimulationStatus: () => client.get<any>('/api/simulation/status').then(res => res.data),

  // Agents & Policies
  getAgents: () => client.get<Agent[]>('/api/agents').then(res => res.data),
  getPolicies: () => client.get<Policy[]>('/api/policies').then(res => res.data),
  togglePolicy: (id: string) => client.patch<any>(`/api/policies/${id}/toggle`).then(res => res.data),

  // Decisions & Conflicts
  getDecisions: (policyDecision?: string) => {
    const params = policyDecision ? { policy_decision: policyDecision } : {};
    return client.get<Decision[]>('/api/decisions', { params }).then(res => res.data);
  },
  getConflicts: () => client.get<Conflict[]>('/api/conflicts').then(res => res.data),

  // Human Reviews
  getReviews: () => client.get<HumanReview[]>('/api/reviews').then(res => res.data),
  processReview: (id: string, action: 'APPROVE' | 'REJECT' | 'MODIFY', notes?: string, modifiedAction?: string) => {
    return client.post<any>(`/api/reviews/${id}/action`, {
      action,
      notes,
      modified_action: modifiedAction
    }).then(res => res.data);
  }
};
export default api;
