export interface Agent {
  id: string;
  agent_id: string;
  display_name: string;
  description: string;
  priority: number;
  is_active: boolean;
}

export interface Customer {
  id: string;
  customer_id: string;
  name: string;
  email: string;
  customer_value: number;
  opt_out: boolean;
  previous_successful_payments: number;
  last_contact_at: string | null;
  created_at: string;
}

export interface Transaction {
  id: string;
  transaction_id: string;
  customer_id: string;
  amount: number;
  currency: string;
  status: 'FAILED' | 'PENDING' | 'RECOVERED' | 'STOPPED';
  retry_count: number;
  recovery_probability: number;
  intervention_cost: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  created_at: string;
}

export interface AgentRecommendation {
  id: string;
  agent_id: string;
  transaction_id: string;
  customer_id: string;
  proposed_action: string;
  confidence: number;
  reasoning: string;
  estimated_recovery: number;
  estimated_cost: number;
  created_at: string;
}

export interface Conflict {
  id: string;
  customer_id: string;
  transaction_id: string | null;
  conflicting_agent_ids: string[];
  conflicting_actions: string[];
  conflict_type: 'DUPLICATE_ACTION' | 'DUPLICATE_COMMUNICATION' | 'COMPETING_FINANCIAL' | 'PRIORITY_CLASH';
  resolution: 'RESOLVED' | 'ESCALATED' | 'BLOCKED';
  winning_agent_id: string | null;
  winning_action: string | null;
  blocked_actions: Array<{agent_id: string; action: string; reason: string}>;
  resolution_reason: string;
  simulation_run_id: string | null;
  created_at: string;
}

export interface Decision {
  id: string;
  customer_id: string;
  transaction_id: string;
  ai_recommended_action: string;
  ai_confidence: number;
  ai_risk_level: string;
  ai_reasoning: string;
  triggered_policies: string[];
  policy_decision: 'ALLOW' | 'REVIEW' | 'STOP';
  final_action: string;
  human_review_required: boolean;
  execution_status: string;
  execution_result: string | null;
  recovered_amount: number;
  reason: string;
  simulation_run_id: string | null;
  created_at: string;
}

export interface Policy {
  id: string;
  name: string;
  description: string;
  rule_type: 'HARD' | 'SOFT';
  parameter_key: string;
  parameter_value: string;
  action_on_trigger: string;
  is_active: boolean;
}

export interface HumanReview {
  id: string;
  decision_id: string;
  customer_id: string;
  transaction_id: string;
  review_reason: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'MODIFIED';
  reviewer_action: string | null;
  reviewer_notes: string | null;
  modified_action: string | null;
  reviewed_at: string | null;
  created_at: string;
}

export interface AuditLog {
  id: string;
  event_type: string;
  transaction_id: string | null;
  customer_id: string | null;
  agent_ids: string[] | null;
  conflict_detected: boolean;
  ai_recommendation: string | null;
  ai_confidence: number | null;
  policy_decision: string | null;
  triggered_policies: string[] | null;
  final_action: string | null;
  execution_result: string | null;
  recovered_amount: number | null;
  amount: number | null;
  risk_level: string | null;
  reason: string | null;
  simulation_run_id: string | null;
  created_at: string;
}

export interface DashboardKPIs {
  total_transactions: number;
  revenue_at_risk: number;
  decisions_total: number;
  actions_allowed: number;
  actions_reviewed: number;
  actions_stopped: number;
  gross_recovered: number;
  conflicts_detected: number;
  reviews_pending: number;
  total_customers: number;
  policy_override_rate: number;
  conflict_rate: number;
}
