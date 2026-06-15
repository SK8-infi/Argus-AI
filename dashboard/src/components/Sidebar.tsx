'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard, Users, ShieldAlert, BarChart3,
  Activity, Eye, Settings, Zap,
} from 'lucide-react';

const navItems = [
  { href: '/', label: 'Overview', icon: LayoutDashboard },
  { href: '/employees', label: 'Employees', icon: Users },
  { href: '/alerts', label: 'Alerts', icon: ShieldAlert, badge: 4 },
  { href: '/analytics', label: 'Analytics', icon: BarChart3 },
];

const navItems2 = [
  { href: '/twin', label: 'Digital Twin', icon: Eye },
  { href: '/activity', label: 'Live Feed', icon: Activity },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <div className="sidebar-logo">🔱</div>
          <div>
            <div className="sidebar-title">Argus AI</div>
            <div className="sidebar-subtitle">Insider Threat Intel</div>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Main</div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon className="nav-item-icon" size={18} />
              {item.label}
              {item.badge && <span className="nav-badge">{item.badge}</span>}
            </Link>
          );
        })}

        <div className="nav-section-label" style={{ marginTop: 8 }}>Intelligence</div>
        {navItems2.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon className="nav-item-icon" size={18} />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-status">
          <span className="status-dot" />
          <span>System Active — 200 employees monitored</span>
        </div>
      </div>
    </aside>
  );
}
