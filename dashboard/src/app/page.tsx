'use client';

import { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';
import {
  employees, alerts, activityFeed, modelMetrics,
  departmentStats, getTrustColor, trustScoreHistory,
  type Employee, type Alert, type ActivityEvent
} from '@/lib/mockData';
import {
  Shield, AlertTriangle, Users, TrendingDown,
  ArrowDownRight, ArrowUpRight, Zap, Eye,
  ChevronRight, Activity, Clock
} from 'lucide-react';
import {
  Chart as ChartJS,
  ArcElement, Tooltip, Legend,
  CategoryScale, LinearScale, PointElement, LineElement, Filler,
} from 'chart.js';
import { Doughnut, Line } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Filler);

// ─── Animated Counter ────────────────────────────────────────────

function AnimatedCounter({ value, decimals = 0, suffix = '' }: { value: number; decimals?: number; suffix?: string }) {
  const [display, setDisplay] = useState(0);
  useEffect(() => {
    const duration = 1200;
    const steps = 40;
    const increment = value / steps;
    let current = 0;
    const timer = setInterval(() => {
      current += increment;
      if (current >= value) {
        setDisplay(value);
        clearInterval(timer);
      } else {
        setDisplay(current);
      }
    }, duration / steps);
    return () => clearInterval(timer);
  }, [value]);
  return <>{display.toFixed(decimals)}{suffix}</>;
}

// ─── Mini Sparkline ──────────────────────────────────────────────

function Sparkline({ data, color }: { data: number[]; color: string }) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const h = 28;
  const w = 80;
  const points = data.map((v, i) => {
    const x = (i / (data.length - 1)) * w;
    const y = h - ((v - min) / range) * h;
    return `${x},${y}`;
  }).join(' ');

  return (
    <svg width={w} height={h} className="sparkline-container">
      <defs>
        <linearGradient id={`grad-${color.replace('#','')}`} x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor={color} stopOpacity="0.3" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      <polyline fill="none" stroke={color} strokeWidth="1.5" points={points} />
      <polygon
        fill={`url(#grad-${color.replace('#','')})`}
        points={`0,${h} ${points} ${w},${h}`}
      />
    </svg>
  );
}

// ─── Trust Level Distribution Donut ──────────────────────────────

function TrustDistribution() {
  const levels = [
    { label: 'Trusted', count: employees.filter(e => e.trustScore >= 80).length, color: '#06b6d4' },
    { label: 'Low Risk', count: employees.filter(e => e.trustScore >= 60 && e.trustScore < 80).length, color: '#22c55e' },
    { label: 'Medium', count: employees.filter(e => e.trustScore >= 40 && e.trustScore < 60).length, color: '#eab308' },
    { label: 'High Risk', count: employees.filter(e => e.trustScore >= 20 && e.trustScore < 40).length, color: '#f97316' },
    { label: 'Critical', count: employees.filter(e => e.trustScore < 20).length, color: '#ef4444' },
  ];

  const data = {
    labels: levels.map(l => l.label),
    datasets: [{
      data: levels.map(l => l.count),
      backgroundColor: levels.map(l => l.color),
      borderWidth: 0,
      hoverOffset: 4,
    }],
  };

  return (
    <div style={{ width: 180, height: 180, margin: '0 auto' }}>
      <Doughnut
        data={data}
        options={{
          cutout: '72%',
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.9)',
              titleFont: { family: 'Inter', size: 12 },
              bodyFont: { family: 'Inter', size: 11 },
              borderColor: 'rgba(148, 163, 184, 0.1)',
              borderWidth: 1,
              padding: 10,
              cornerRadius: 8,
            },
          },
        }}
      />
    </div>
  );
}

// ─── Main Dashboard Page ─────────────────────────────────────────

export default function Dashboard() {
  const [currentTime, setCurrentTime] = useState('');
  const [feedHighlight, setFeedHighlight] = useState<string | null>(null);

  useEffect(() => {
    const updateTime = () => {
      setCurrentTime(new Date().toLocaleTimeString('en-IN', {
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false,
      }));
    };
    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  // Pulse the latest feed item
  useEffect(() => {
    setFeedHighlight(activityFeed[0]?.id);
    const timer = setTimeout(() => setFeedHighlight(null), 3000);
    return () => clearTimeout(timer);
  }, []);

  const sortedEmployees = [...employees].sort((a, b) => a.trustScore - b.trustScore);
  const criticalAlerts = alerts.filter(a => a.severity === 'CRITICAL');

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <div className="page-header">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="page-title">Command Center</h1>
              <p className="page-subtitle">Real-time insider threat monitoring across all departments</p>
            </div>
            <div className="flex items-center gap-16">
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 14px', background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)' }}>
                <Clock size={14} style={{ color: 'var(--cyan-500)' }} />
                <span className="text-mono text-sm" style={{ color: 'var(--text-secondary)' }}>{currentTime} IST</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 14px', background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.15)', borderRadius: 'var(--radius-md)' }}>
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#ef4444', animation: 'pulse-badge 1.5s infinite' }} />
                <span className="text-sm font-semibold" style={{ color: '#ef4444' }}>{criticalAlerts.length} Critical</span>
              </div>
            </div>
          </div>
        </div>

        <div className="page-content">
          {/* ─── Metric Cards ─── */}
          <div className="metrics-grid">
            <div className="metric-card" style={{ '--metric-accent': '#06b6d4' } as React.CSSProperties}>
              <div className="flex items-center justify-between mb-8">
                <span className="metric-label">Employees Monitored</span>
                <Users size={18} style={{ color: 'var(--cyan-500)', opacity: 0.6 }} />
              </div>
              <div className="metric-value accent-cyan"><AnimatedCounter value={modelMetrics.employeesMonitored} /></div>
              <div className="metric-change positive">
                <ArrowUpRight size={14} />
                All departments active
              </div>
            </div>

            <div className="metric-card" style={{ '--metric-accent': '#ef4444' } as React.CSSProperties}>
              <div className="flex items-center justify-between mb-8">
                <span className="metric-label">Active Threats</span>
                <AlertTriangle size={18} style={{ color: '#ef4444', opacity: 0.6 }} />
              </div>
              <div className="metric-value" style={{ background: 'linear-gradient(135deg, #ef4444, #f97316)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                <AnimatedCounter value={modelMetrics.threatsDetected} />
              </div>
              <div className="metric-change negative">
                <ArrowDownRight size={14} />
                2 critical, 1 high, 1 medium
              </div>
            </div>

            <div className="metric-card" style={{ '--metric-accent': '#8b5cf6' } as React.CSSProperties}>
              <div className="flex items-center justify-between mb-8">
                <span className="metric-label">Model F1 Score</span>
                <Zap size={18} style={{ color: '#8b5cf6', opacity: 0.6 }} />
              </div>
              <div className="metric-value"><AnimatedCounter value={modelMetrics.f1 * 100} decimals={1} suffix="%" /></div>
              <div className="metric-change positive">
                <ArrowUpRight size={14} />
                AUC-ROC: {(modelMetrics.aucRoc * 100).toFixed(1)}%
              </div>
            </div>

            <div className="metric-card" style={{ '--metric-accent': '#22c55e' } as React.CSSProperties}>
              <div className="flex items-center justify-between mb-8">
                <span className="metric-label">False Positive Rate</span>
                <Shield size={18} style={{ color: '#22c55e', opacity: 0.6 }} />
              </div>
              <div className="metric-value"><AnimatedCounter value={modelMetrics.falsePositiveRate * 100} decimals={1} suffix="%" /></div>
              <div className="metric-change positive">
                <ArrowUpRight size={14} />
                Below 2% target
              </div>
            </div>
          </div>

          {/* ─── Main Grid ─── */}
          <div className="dashboard-grid">
            {/* Left Column */}
            <div className="flex flex-col gap-20">
              {/* Trust Heatmap */}
              <div className="card">
                <div className="card-header">
                  <div className="card-title">
                    <Eye size={16} style={{ color: 'var(--cyan-500)' }} />
                    Employee Trust Heatmap
                  </div>
                  <span className="text-xs text-muted">{employees.length} employees</span>
                </div>
                <div className="card-body">
                  <div className="heatmap-grid">
                    {sortedEmployees.map((emp) => {
                      const bg = getTrustColor(emp.trustScore);
                      const initials = emp.name.split(' ').map(n => n[0]).join('');
                      const isPulsing = emp.trustScore < 30;
                      return (
                        <div
                          key={emp.id}
                          className={`heatmap-cell ${isPulsing ? 'pulse-alert' : ''}`}
                          style={{
                            background: `${bg}22`,
                            border: `1px solid ${bg}40`,
                          }}
                          title={`${emp.name} — Trust: ${emp.trustScore}`}
                        >
                          <span className="heatmap-cell-initials">{initials}</span>
                          <span className="heatmap-cell-score" style={{ color: bg }}>{emp.trustScore}</span>
                        </div>
                      );
                    })}
                  </div>
                  <div className="flex items-center justify-between mt-16" style={{ padding: '0 4px' }}>
                    <div className="flex items-center gap-12">
                      {[
                        { label: 'Critical', color: '#ef4444' },
                        { label: 'High', color: '#f97316' },
                        { label: 'Medium', color: '#eab308' },
                        { label: 'Low', color: '#22c55e' },
                        { label: 'Trusted', color: '#06b6d4' },
                      ].map(l => (
                        <div key={l.label} className="flex items-center gap-4">
                          <span style={{ width: 8, height: 8, borderRadius: 2, background: l.color }} />
                          <span className="text-xs text-muted">{l.label}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Live Activity Feed */}
              <div className="card">
                <div className="card-header">
                  <div className="card-title">
                    <Activity size={16} style={{ color: 'var(--cyan-500)' }} />
                    Live Activity Feed
                  </div>
                  <span className="text-xs text-mono" style={{ color: 'var(--trust-low)' }}>● STREAMING</span>
                </div>
                <div className="card-body" style={{ padding: '8px 20px 20px' }}>
                  <div className="feed-container">
                    {activityFeed.map((event) => {
                      const riskLevel = event.riskContribution > 70 ? 'high' : event.riskContribution > 30 ? 'medium' : 'low';
                      return (
                        <div
                          key={event.id}
                          className="feed-item"
                          style={{
                            background: feedHighlight === event.id ? 'rgba(6, 182, 212, 0.05)' : undefined,
                            transition: 'background 0.5s ease',
                          }}
                        >
                          <span className="feed-time">{event.timestamp}</span>
                          <span className="feed-icon">{event.icon}</span>
                          <div className="feed-content">
                            <span className="feed-employee">{event.employeeName}</span>{' '}
                            <span className="feed-detail">{event.detail}</span>
                          </div>
                          <span className={`feed-risk ${riskLevel}`}>{event.riskContribution}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column */}
            <div className="flex flex-col gap-20">
              {/* Alert Queue */}
              <div className="card card-glow-red">
                <div className="card-header">
                  <div className="card-title">
                    <AlertTriangle size={16} style={{ color: '#ef4444' }} />
                    Active Alerts
                  </div>
                  <span className="alert-severity-badge CRITICAL">{alerts.length} active</span>
                </div>
                <div className="card-body" style={{ padding: '8px 12px 12px' }}>
                  {alerts.map((alert) => (
                    <div key={alert.id} className={`alert-item severity-${alert.severity}`}>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div className="flex items-center gap-8">
                          <span className={`alert-severity-badge ${alert.severity}`}>{alert.severity}</span>
                          <span className="alert-name">{alert.employeeName}</span>
                        </div>
                        <div className="alert-meta">{alert.department} • {alert.riskFactors[0]?.factor}</div>
                        {alert.intentChain && (
                          <div className="alert-intent">
                            ⛓ {alert.intentChain.pattern} ({(alert.intentChain.confidence * 100).toFixed(0)}%)
                          </div>
                        )}
                      </div>
                      <div className="alert-trust-change" style={{ color: getTrustColor(alert.trustScore) }}>
                        {alert.trustScore}
                        <div className="text-xs text-muted" style={{ fontWeight: 400 }}>
                          was {alert.previousTrustScore}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Trust Distribution */}
              <div className="card">
                <div className="card-header">
                  <div className="card-title">
                    <Shield size={16} style={{ color: 'var(--cyan-500)' }} />
                    Trust Distribution
                  </div>
                </div>
                <div className="card-body">
                  <TrustDistribution />
                  <div className="mt-16">
                    {departmentStats.map((dept) => (
                      <div key={dept.name} className="flex items-center justify-between" style={{ padding: '8px 0', borderBottom: '1px solid var(--border-subtle)' }}>
                        <div className="flex items-center gap-8">
                          <span style={{ width: 8, height: 8, borderRadius: 2, background: dept.color }} />
                          <span className="text-sm">{dept.name}</span>
                        </div>
                        <div className="flex items-center gap-12">
                          <span className="text-xs text-muted">{dept.employees} emp</span>
                          <span className="text-sm font-semibold text-mono" style={{ color: getTrustColor(dept.avgTrust), minWidth: 40, textAlign: 'right' }}>
                            {dept.avgTrust.toFixed(0)}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Top Risk Employees */}
              <div className="card">
                <div className="card-header">
                  <div className="card-title">
                    <TrendingDown size={16} style={{ color: '#f97316' }} />
                    Highest Risk
                  </div>
                </div>
                <div className="card-body" style={{ padding: '8px 20px 20px' }}>
                  {sortedEmployees.slice(0, 5).map((emp) => (
                    <div key={emp.id} className="flex items-center gap-12" style={{ padding: '10px 0', borderBottom: '1px solid var(--border-subtle)' }}>
                      <div className="avatar avatar-sm" style={{ background: emp.avatarColor }}>
                        {emp.name.split(' ').map(n => n[0]).join('')}
                      </div>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div className="text-sm font-semibold truncate">{emp.name}</div>
                        <div className="text-xs text-muted">{emp.department}</div>
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 2 }}>
                        <span className="text-mono font-bold text-sm" style={{ color: getTrustColor(emp.trustScore) }}>
                          {emp.trustScore}
                        </span>
                        {trustScoreHistory[emp.id] && (
                          <Sparkline data={trustScoreHistory[emp.id]} color={getTrustColor(emp.trustScore)} />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
