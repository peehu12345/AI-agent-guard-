export const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(amount);
};

export const formatPercent = (value: number) => {
  return `${(value * 100).toFixed(1)}%`;
};

export const formatDateTime = (dt: string | null) => {
  if (!dt) return 'N/A';
  return new Date(dt).toLocaleString('en-IN', {
    dateStyle: 'short',
    timeStyle: 'medium'
  });
};

export const formatConfidence = (c: number) => {
  return `${(c * 100).toFixed(0)}%`;
};
