import React from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  MarkerType
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

interface FlowProps {
  conflicts?: any[];
}

export const AgentFlowDiagram: React.FC<FlowProps> = ({ conflicts = [] }) => {
  // Let's check if there is an active conflict
  const hasConflict = conflicts.length > 0;
  
  const initialNodes = [
    {
      id: 'cust',
      data: { label: 'Customer Transaction' },
      position: { x: 50, y: 150 },
      style: {
        background: 'rgba(59, 130, 246, 0.1)',
        color: '#60a5fa',
        border: '1px solid rgba(59, 130, 246, 0.3)',
        borderRadius: '8px',
        padding: '12px',
        fontSize: '12px',
        fontWeight: 'bold',
        width: 150,
        textAlign: 'center' as const
      }
    },
    {
      id: 'agent1',
      data: { label: 'Subscription Agent' },
      position: { x: 280, y: 30 },
      style: {
        background: 'rgba(99, 102, 241, 0.1)',
        color: '#818cf8',
        border: '1px solid rgba(99, 102, 241, 0.3)',
        borderRadius: '8px',
        padding: '12px',
        fontSize: '12px',
        fontWeight: 'bold',
        width: 150,
        textAlign: 'center' as const,
        boxShadow: hasConflict ? '0 0 15px rgba(239, 68, 68, 0.4)' : 'none'
      }
    },
    {
      id: 'agent2',
      data: { label: 'Payment Recovery' },
      position: { x: 280, y: 110 },
      style: {
        background: 'rgba(16, 185, 129, 0.1)',
        color: '#34d399',
        border: '1px solid rgba(16, 185, 129, 0.3)',
        borderRadius: '8px',
        padding: '12px',
        fontSize: '12px',
        fontWeight: 'bold',
        width: 150,
        textAlign: 'center' as const,
        boxShadow: hasConflict ? '0 0 15px rgba(239, 68, 68, 0.4)' : 'none'
      }
    },
    {
      id: 'agent3',
      data: { label: 'Checkout Recovery' },
      position: { x: 280, y: 190 },
      style: {
        background: 'rgba(14, 165, 233, 0.1)',
        color: '#38bdf8',
        border: '1px solid rgba(14, 165, 233, 0.3)',
        borderRadius: '8px',
        padding: '12px',
        fontSize: '12px',
        fontWeight: 'bold',
        width: 150,
        textAlign: 'center' as const
      }
    },
    {
      id: 'agent4',
      data: { label: 'Receivables Agent' },
      position: { x: 280, y: 270 },
      style: {
        background: 'rgba(139, 92, 246, 0.1)',
        color: '#a78bfa',
        border: '1px solid rgba(139, 92, 246, 0.3)',
        borderRadius: '8px',
        padding: '12px',
        fontSize: '12px',
        fontWeight: 'bold',
        width: 150,
        textAlign: 'center' as const
      }
    },
    {
      id: 'guard',
      data: { label: '🛡️ AgentGuard Router' },
      position: { x: 520, y: 150 },
      style: {
        background: 'rgba(79, 70, 229, 0.2)',
        color: '#e0e7ff',
        border: '1px solid rgba(99, 102, 241, 0.5)',
        borderRadius: '10px',
        padding: '16px',
        fontSize: '13px',
        fontWeight: 'bold',
        width: 180,
        textAlign: 'center' as const,
        boxShadow: '0 0 20px rgba(99, 102, 241, 0.3)'
      }
    },
    {
      id: 'policy',
      data: { label: 'Policy Engine\n(Hard & Soft Rules)' },
      position: { x: 780, y: 150 },
      style: {
        background: 'rgba(245, 158, 11, 0.15)',
        color: '#fbbf24',
        border: '1px solid rgba(245, 158, 11, 0.4)',
        borderRadius: '8px',
        padding: '12px',
        fontSize: '12px',
        fontWeight: 'bold',
        width: 160,
        textAlign: 'center' as const
      }
    },
    {
      id: 'out',
      data: { label: 'ALLOW / REVIEW / STOP' },
      position: { x: 1020, y: 150 },
      style: {
        background: 'rgba(16, 185, 129, 0.15)',
        color: '#34d399',
        border: '1px solid rgba(16, 185, 129, 0.4)',
        borderRadius: '8px',
        padding: '12px',
        fontSize: '12px',
        fontWeight: 'bold',
        width: 180,
        textAlign: 'center' as const
      }
    }
  ];

  const initialEdges = [
    { id: 'c-a1', source: 'cust', target: 'agent1', animated: true },
    { id: 'c-a2', source: 'cust', target: 'agent2', animated: true },
    { id: 'c-a3', source: 'cust', target: 'agent3', animated: true },
    { id: 'c-a4', source: 'cust', target: 'agent4', animated: true },

    {
      id: 'a1-g',
      source: 'agent1',
      target: 'guard',
      animated: true,
      style: { stroke: hasConflict ? '#ef4444' : '#6366f1' }
    },
    {
      id: 'a2-g',
      source: 'agent2',
      target: 'guard',
      animated: true,
      style: { stroke: hasConflict ? '#ef4444' : '#10b981' }
    },
    { id: 'a3-g', source: 'agent3', target: 'guard', animated: true, style: { stroke: '#0ea5e9' } },
    { id: 'a4-g', source: 'agent4', target: 'guard', animated: true, style: { stroke: '#8b5cf6' } },

    {
      id: 'g-p',
      source: 'guard',
      target: 'policy',
      animated: true,
      style: { stroke: '#6366f1' },
      markerEnd: { type: MarkerType.ArrowClosed }
    },
    {
      id: 'p-o',
      source: 'policy',
      target: 'out',
      animated: true,
      style: { stroke: '#f59e0b' },
      markerEnd: { type: MarkerType.ArrowClosed }
    }
  ];

  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  return (
    <div className="w-full h-96 border border-slate-900 rounded-xl overflow-hidden bg-slate-950/40">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
      >
        <Background color="#1e293b" gap={16} />
        <Controls className="bg-slate-900 border border-slate-800 text-slate-100" />
      </ReactFlow>
    </div>
  );
};
export default AgentFlowDiagram;
