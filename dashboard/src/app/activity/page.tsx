'use client';

import { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';
import { activityFeed, getTrustColor, type ActivityEvent } from '@/lib/mockData';
import { Activity, Filter, Pause, Play } from 'lucide-react';

export default function ActivityPage() {
  const [isPaused, setIsPaused] = useState(false);
  const [filter, setFilter] = useState<string>('all');
  const [events, setEvents] = useState(activityFeed);
  const [newEventFlash, setNewEventFlash] = useState<string | null>(null);

  // Simulated live events
  useEffect(() => {
    if (isPaused) return;
    const syntheticEvents: ActivityEvent[] = [
      { id: 'LIVE_01', timestamp: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }), employeeId: 'EMP_003', employeeName: 'Vikram Singh', actionType: 'login', system: 'Admin Console', detail: 'Routine admin check — within scope', riskContribution: 4, icon: '🔑' },
      { id: 'LIVE_02', timestamp: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }), employeeId: 'EMP_005', employeeName: 'Rohan Gupta', actionType: 'data_access', system: 'AML Platform', detail: 'SAR filing — compliance routine', riskContribution: 2, icon: '📋' },
      { id: 'LIVE_03', timestamp: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }), employeeId: 'EMP_155', employeeName: 'Arjun Kapoor', actionType: 'system_command', system: 'Production Server', detail: 'Executed DROP TABLE — CRITICAL unauthorized command', riskContribution: 98, icon: '💀' },
    ];

    let idx = 0;
    const interval = setInterval(() => {
      if (idx < syntheticEvents.length) {
        const newEvent = { ...syntheticEvents[idx], id: `LIVE_${Date.now()}`, timestamp: new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }) };
        setEvents(prev => [newEvent, ...prev].slice(0, 50));
        setNewEventFlash(newEvent.id);
        setTimeout(() => setNewEventFlash(null), 2000);
        idx++;
      }
    }, 4000);

    return () => clearInterval(interval);
  }, [isPaused]);

  const riskLevels = ['all', 'critical', 'high', 'medium', 'low'];
  const filtered = filter === 'all'
    ? events
    : events.filter(e => {
        if (filter === 'critical') return e.riskContribution > 85;
        if (filter === 'high') return e.riskContribution > 60 && e.riskContribution <= 85;
        if (filter === 'medium') return e.riskContribution > 20 && e.riskContribution <= 60;
        return e.riskContribution <= 20;
      });

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <div className="page-header">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="page-title">Live Activity Feed</h1>
              <p className="page-subtitle">Real-time behavioral event stream across all departments</p>
            </div>
            <div className="flex items-center gap-12">
              <button
                onClick={() => setIsPaused(!isPaused)}
                className="nav-item"
                style={{
                  padding: '6px 14px', borderRadius: 'var(--radius-md)', width: 'auto',
                  background: isPaused ? 'rgba(34,197,94,0.1)' : 'rgba(239,68,68,0.1)',
                  border: `1px solid ${isPaused ? 'rgba(34,197,94,0.2)' : 'rgba(239,68,68,0.2)'}`,
                  color: isPaused ? '#22c55e' : '#ef4444',
                }}
              >
                {isPaused ? <Play size={14} /> : <Pause size={14} />}
                <span className="text-xs font-semibold">{isPaused ? 'Resume' : 'Pause'}</span>
              </button>
              <div className="filter-tabs">
                {riskLevels.map(l => (
                  <button key={l} className={`filter-tab ${filter === l ? 'active' : ''}`} onClick={() => setFilter(l)}>
                    {l.charAt(0).toUpperCase() + l.slice(1)}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
        <div className="page-content">
          {/* Live indicator */}
          <div className="flex items-center gap-8 mb-16">
            <span style={{
              width: 8, height: 8, borderRadius: '50%',
              background: isPaused ? '#eab308' : '#22c55e',
              boxShadow: isPaused ? '0 0 8px rgba(234,179,8,0.4)' : '0 0 8px rgba(34,197,94,0.4)',
              animation: isPaused ? 'none' : 'pulse-dot 2s ease-in-out infinite',
            }} />
            <span className="text-xs text-mono" style={{ color: isPaused ? '#eab308' : '#22c55e' }}>
              {isPaused ? 'PAUSED' : 'STREAMING'} — {filtered.length} events
            </span>
          </div>

          <div className="card">
            <div className="card-body" style={{ padding: '8px 20px 20px' }}>
              {filtered.map((event) => {
                const riskLevel = event.riskContribution > 70 ? 'high' : event.riskContribution > 30 ? 'medium' : 'low';
                const isNew = newEventFlash === event.id;
                return (
                  <div
                    key={event.id}
                    className="feed-item"
                    style={{
                      background: isNew ? 'rgba(6, 182, 212, 0.06)' : undefined,
                      borderRadius: isNew ? 'var(--radius-md)' : undefined,
                      transition: 'background 0.8s ease',
                    }}
                  >
                    <span className="feed-time">{event.timestamp}</span>
                    <span className="feed-icon" style={{ fontSize: 16 }}>{event.icon}</span>
                    <div className="feed-content">
                      <span className="feed-employee">{event.employeeName}</span>
                      <span className="text-xs text-mono text-muted" style={{ marginLeft: 6 }}>({event.employeeId})</span>
                      <br />
                      <span className="feed-detail">{event.detail}</span>
                      <span className="text-xs text-muted" style={{ marginLeft: 8 }}>on {event.system}</span>
                    </div>
                    <div style={{ textAlign: 'right', flexShrink: 0 }}>
                      <span className={`feed-risk ${riskLevel}`}>{event.riskContribution}</span>
                      <div className="text-xs text-muted mt-4">{event.actionType.replace(/_/g, ' ')}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
