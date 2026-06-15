/**
 * Argus AI — Mock Data
 * Realistic employee behavioral data for dashboard development.
 * Will be replaced by FastAPI backend in production.
 */

export type TrustLevel = 'CRITICAL' | 'HIGH_RISK' | 'MEDIUM_RISK' | 'LOW_RISK' | 'TRUSTED';

export interface Employee {
  id: string;
  name: string;
  department: string;
  role: string;
  branch: string;
  clearanceLevel: number;
  tenureMonths: number;
  trustScore: number;
  previousTrustScore: number;
  trustLevel: TrustLevel;
  avatarColor: string;
  isInsider: boolean;
  lastActive: string;
  twinDrift: number;
}

export interface RiskFactor {
  factor: string;
  detail: string;
  impact: number;
  icon: string;
}

export interface Alert {
  id: string;
  employeeId: string;
  employeeName: string;
  department: string;
  trustScore: number;
  previousTrustScore: number;
  trustLevel: TrustLevel;
  timestamp: string;
  riskFactors: RiskFactor[];
  intentChain: {
    pattern: string;
    confidence: number;
    matchedSteps: string[];
  } | null;
  status: 'active' | 'investigating' | 'resolved' | 'dismissed';
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface ActivityEvent {
  id: string;
  timestamp: string;
  employeeId: string;
  employeeName: string;
  actionType: string;
  system: string;
  detail: string;
  riskContribution: number;
  icon: string;
}

export interface TwinProfile {
  expectedLogin: string;
  actualLogin: string;
  expectedSystems: string[];
  actualSystems: string[];
  expectedRecords: number;
  actualRecords: number;
  expectedDataVolume: number;
  actualDataVolume: number;
  expectedDevices: number;
  actualDevices: number;
  dimensions: {
    label: string;
    expected: number;
    actual: number;
  }[];
}

export interface PrivilegeDecayPoint {
  time: string;
  trustScore: number;
  event: string | null;
}

export interface ModelMetrics {
  f1: number;
  precision: number;
  recall: number;
  aucRoc: number;
  falsePositiveRate: number;
  alertsToday: number;
  employeesMonitored: number;
  threatsDetected: number;
}

// ─── Color Helpers ───────────────────────────────────────────────

const AVATAR_COLORS = [
  '#06b6d4', '#8b5cf6', '#f59e0b', '#10b981', '#ef4444',
  '#ec4899', '#3b82f6', '#14b8a6', '#f97316', '#6366f1',
];

function getTrustLevel(score: number): TrustLevel {
  if (score < 20) return 'CRITICAL';
  if (score < 40) return 'HIGH_RISK';
  if (score < 60) return 'MEDIUM_RISK';
  if (score < 80) return 'LOW_RISK';
  return 'TRUSTED';
}

// ─── Employees ───────────────────────────────────────────────────

export const employees: Employee[] = [
  { id: 'EMP_001', name: 'Aarav Mehta', department: 'Retail Banking', role: 'Relationship Manager', branch: 'Mumbai Main', clearanceLevel: 3, tenureMonths: 36, trustScore: 94, previousTrustScore: 95, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[0], isInsider: false, lastActive: '2 min ago', twinDrift: 0.02 },
  { id: 'EMP_002', name: 'Priya Sharma', department: 'Treasury', role: 'Treasury Analyst', branch: 'Delhi NCR', clearanceLevel: 4, tenureMonths: 48, trustScore: 91, previousTrustScore: 93, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[1], isInsider: false, lastActive: '5 min ago', twinDrift: 0.03 },
  { id: 'EMP_003', name: 'Vikram Singh', department: 'IT Admin', role: 'System Admin', branch: 'Bangalore Tech', clearanceLevel: 5, tenureMonths: 60, trustScore: 88, previousTrustScore: 90, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[2], isInsider: false, lastActive: '1 min ago', twinDrift: 0.05 },
  { id: 'EMP_004', name: 'Ananya Patel', department: 'HR', role: 'HR Generalist', branch: 'Mumbai Main', clearanceLevel: 2, tenureMonths: 24, trustScore: 92, previousTrustScore: 91, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[3], isInsider: false, lastActive: '8 min ago', twinDrift: 0.01 },
  { id: 'EMP_005', name: 'Rohan Gupta', department: 'Compliance', role: 'AML Analyst', branch: 'Mumbai Main', clearanceLevel: 4, tenureMonths: 30, trustScore: 96, previousTrustScore: 95, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[4], isInsider: false, lastActive: '3 min ago', twinDrift: 0.01 },
  { id: 'EMP_006', name: 'Kavya Reddy', department: 'Retail Banking', role: 'Teller', branch: 'Chennai South', clearanceLevel: 1, tenureMonths: 12, trustScore: 87, previousTrustScore: 89, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[5], isInsider: false, lastActive: '12 min ago', twinDrift: 0.04 },
  { id: 'EMP_007', name: 'Amit Joshi', department: 'Retail Banking', role: 'Branch Manager', branch: 'Pune Central', clearanceLevel: 4, tenureMonths: 72, trustScore: 93, previousTrustScore: 94, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[6], isInsider: false, lastActive: '6 min ago', twinDrift: 0.02 },
  // ─── HIGH RISK / INSIDERS ───
  { id: 'EMP_047', name: 'Raj Malhotra', department: 'Retail Banking', role: 'Relationship Manager', branch: 'Delhi NCR', clearanceLevel: 3, tenureMonths: 42, trustScore: 23, previousTrustScore: 94, trustLevel: 'HIGH_RISK', avatarColor: AVATAR_COLORS[7], isInsider: true, lastActive: 'Now', twinDrift: 0.87 },
  { id: 'EMP_089', name: 'Suresh Nair', department: 'IT Admin', role: 'DBA Admin', branch: 'Bangalore Tech', clearanceLevel: 5, tenureMonths: 54, trustScore: 34, previousTrustScore: 88, trustLevel: 'HIGH_RISK', avatarColor: AVATAR_COLORS[8], isInsider: true, lastActive: '15 min ago', twinDrift: 0.72 },
  { id: 'EMP_112', name: 'Deepa Krishnan', department: 'HR', role: 'HR Generalist', branch: 'Mumbai Main', clearanceLevel: 2, tenureMonths: 18, trustScore: 41, previousTrustScore: 85, trustLevel: 'MEDIUM_RISK', avatarColor: AVATAR_COLORS[9], isInsider: true, lastActive: '22 min ago', twinDrift: 0.61 },
  { id: 'EMP_008', name: 'Neha Verma', department: 'Treasury', role: 'Trader', branch: 'Mumbai Main', clearanceLevel: 4, tenureMonths: 36, trustScore: 89, previousTrustScore: 90, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[0], isInsider: false, lastActive: '4 min ago', twinDrift: 0.03 },
  { id: 'EMP_009', name: 'Karthik Iyer', department: 'Compliance', role: 'Risk Officer', branch: 'Bangalore Tech', clearanceLevel: 4, tenureMonths: 48, trustScore: 97, previousTrustScore: 96, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[1], isInsider: false, lastActive: '7 min ago', twinDrift: 0.01 },
  { id: 'EMP_010', name: 'Meera Das', department: 'Retail Banking', role: 'Relationship Manager', branch: 'Kolkata Main', clearanceLevel: 3, tenureMonths: 28, trustScore: 82, previousTrustScore: 84, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[2], isInsider: false, lastActive: '9 min ago', twinDrift: 0.06 },
  { id: 'EMP_155', name: 'Arjun Kapoor', department: 'IT Admin', role: 'Help Desk', branch: 'Chennai South', clearanceLevel: 2, tenureMonths: 8, trustScore: 15, previousTrustScore: 78, trustLevel: 'CRITICAL', avatarColor: AVATAR_COLORS[3], isInsider: true, lastActive: '1 min ago', twinDrift: 0.93 },
  { id: 'EMP_011', name: 'Sneha Bose', department: 'Compliance', role: 'Auditor', branch: 'Delhi NCR', clearanceLevel: 3, tenureMonths: 40, trustScore: 90, previousTrustScore: 91, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[4], isInsider: false, lastActive: '11 min ago', twinDrift: 0.02 },
  { id: 'EMP_012', name: 'Rahul Menon', department: 'Treasury', role: 'Treasury Analyst', branch: 'Mumbai Main', clearanceLevel: 4, tenureMonths: 32, trustScore: 85, previousTrustScore: 87, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[5], isInsider: false, lastActive: '14 min ago', twinDrift: 0.04 },
  { id: 'EMP_013', name: 'Divya Agarwal', department: 'HR', role: 'Recruiter', branch: 'Pune Central', clearanceLevel: 2, tenureMonths: 20, trustScore: 91, previousTrustScore: 92, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[6], isInsider: false, lastActive: '16 min ago', twinDrift: 0.02 },
  { id: 'EMP_014', name: 'Sanjay Tiwari', department: 'Retail Banking', role: 'Teller', branch: 'Mumbai Main', clearanceLevel: 1, tenureMonths: 15, trustScore: 86, previousTrustScore: 88, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[7], isInsider: false, lastActive: '18 min ago', twinDrift: 0.03 },
  { id: 'EMP_015', name: 'Pooja Nanda', department: 'Compliance', role: 'AML Analyst', branch: 'Bangalore Tech', clearanceLevel: 4, tenureMonths: 44, trustScore: 95, previousTrustScore: 94, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[8], isInsider: false, lastActive: '20 min ago', twinDrift: 0.01 },
  { id: 'EMP_016', name: 'Varun Saxena', department: 'IT Admin', role: 'System Admin', branch: 'Delhi NCR', clearanceLevel: 5, tenureMonths: 56, trustScore: 83, previousTrustScore: 85, trustLevel: 'TRUSTED', avatarColor: AVATAR_COLORS[9], isInsider: false, lastActive: '25 min ago', twinDrift: 0.05 },
];

// ─── Alerts ──────────────────────────────────────────────────────

export const alerts: Alert[] = [
  {
    id: 'ALT_001',
    employeeId: 'EMP_155',
    employeeName: 'Arjun Kapoor',
    department: 'IT Admin',
    trustScore: 15,
    previousTrustScore: 78,
    trustLevel: 'CRITICAL',
    timestamp: '2025-06-15T22:51:00+05:30',
    severity: 'CRITICAL',
    status: 'active',
    riskFactors: [
      { factor: 'Privilege escalation', detail: 'Used superadmin credentials on production CBS — Help Desk role has no authorization', impact: -25, icon: '🔓' },
      { factor: 'Audit log access', detail: 'Queried audit_logs table — potential evidence tampering', impact: -18, icon: '📋' },
      { factor: 'New admin account created', detail: 'Created SYS_ADMIN_TEMP on production — persistence mechanism', impact: -15, icon: '👤' },
      { factor: 'After-hours access', detail: '22:51 IST — outside normal hours (09:00-17:30)', impact: -10, icon: '🕐' },
    ],
    intentChain: {
      pattern: 'Privilege Escalation Abuse',
      confidence: 0.94,
      matchedSteps: ['privilege_escalation', 'audit_log_access', 'admin_account_creation'],
    },
  },
  {
    id: 'ALT_002',
    employeeId: 'EMP_047',
    employeeName: 'Raj Malhotra',
    department: 'Retail Banking',
    trustScore: 23,
    previousTrustScore: 94,
    trustLevel: 'HIGH_RISK',
    timestamp: '2025-06-15T22:47:00+05:30',
    severity: 'CRITICAL',
    status: 'investigating',
    riskFactors: [
      { factor: 'Excessive data access', detail: '847 customer records — 15× daily average (56)', impact: -25, icon: '📊' },
      { factor: 'USB device connected', detail: 'No USB usage in 36-month history', impact: -15, icon: '💾' },
      { factor: 'New workstation', detail: 'WS_DEL_019 — first-time use', impact: -12, icon: '📍' },
      { factor: 'After-hours access', detail: '22:47 IST — outside normal hours (09:00-18:00)', impact: -10, icon: '🕐' },
      { factor: 'Cross-role access', detail: 'Treasury database — not in RM scope', impact: -20, icon: '🏦' },
    ],
    intentChain: {
      pattern: 'Data Exfiltration',
      confidence: 0.89,
      matchedSteps: ['access_sensitive_data', 'bulk_download', 'usb_connect', 'file_copy_to_usb'],
    },
  },
  {
    id: 'ALT_003',
    employeeId: 'EMP_089',
    employeeName: 'Suresh Nair',
    department: 'IT Admin',
    trustScore: 34,
    previousTrustScore: 88,
    trustLevel: 'HIGH_RISK',
    timestamp: '2025-06-15T21:30:00+05:30',
    severity: 'HIGH',
    status: 'active',
    riskFactors: [
      { factor: 'Production database access', detail: 'Direct query on prod CBS — should use staging', impact: -15, icon: '🗄️' },
      { factor: 'Bulk data export', detail: '12,400 records exported to CSV — 50× normal', impact: -20, icon: '📤' },
      { factor: 'After-hours access', detail: '21:30 IST — outside normal hours', impact: -8, icon: '🕐' },
      { factor: 'VPN from unusual location', detail: 'VPN login from Goa — employee based in Bangalore', impact: -12, icon: '🌐' },
    ],
    intentChain: {
      pattern: 'Data Exfiltration',
      confidence: 0.76,
      matchedSteps: ['access_sensitive_data', 'bulk_download'],
    },
  },
  {
    id: 'ALT_004',
    employeeId: 'EMP_112',
    employeeName: 'Deepa Krishnan',
    department: 'HR',
    trustScore: 41,
    previousTrustScore: 85,
    trustLevel: 'MEDIUM_RISK',
    timestamp: '2025-06-15T19:15:00+05:30',
    severity: 'MEDIUM',
    status: 'active',
    riskFactors: [
      { factor: 'Cross-role data access', detail: 'Accessed 23 customer financial records — HR has no authorization', impact: -18, icon: '🏦' },
      { factor: 'Gradual scope expansion', detail: '3rd week of increasing non-HR data access (2→8→23 records)', impact: -12, icon: '📈' },
      { factor: 'Job search detected', detail: 'LinkedIn and Indeed browsing during work hours', impact: -8, icon: '🔍' },
    ],
    intentChain: {
      pattern: 'Pre-Resignation Theft',
      confidence: 0.67,
      matchedSteps: ['job_search_browsing', 'increased_file_access', 'cross_role_data_access'],
    },
  },
];

// ─── Live Activity Feed ──────────────────────────────────────────

export const activityFeed: ActivityEvent[] = [
  { id: 'ACT_001', timestamp: '22:51:12', employeeId: 'EMP_155', employeeName: 'Arjun Kapoor', actionType: 'privilege_escalation', system: 'CBS Production', detail: 'Used superadmin credentials — unauthorized', riskContribution: 92, icon: '🔓' },
  { id: 'ACT_002', timestamp: '22:47:33', employeeId: 'EMP_047', employeeName: 'Raj Malhotra', actionType: 'usb_connect', system: 'WS_DEL_019', detail: 'USB device connected — first ever USB usage', riskContribution: 78, icon: '💾' },
  { id: 'ACT_003', timestamp: '22:45:18', employeeId: 'EMP_047', employeeName: 'Raj Malhotra', actionType: 'bulk_download', system: 'CBS', detail: '847 customer records accessed in 12 minutes', riskContribution: 85, icon: '📊' },
  { id: 'ACT_004', timestamp: '22:38:05', employeeId: 'EMP_003', employeeName: 'Vikram Singh', actionType: 'login', system: 'Admin Console', detail: 'Routine system check — within role scope', riskContribution: 5, icon: '🔑' },
  { id: 'ACT_005', timestamp: '22:30:41', employeeId: 'EMP_155', employeeName: 'Arjun Kapoor', actionType: 'audit_log_access', system: 'Audit System', detail: 'Queried audit logs — Help Desk has no authorization', riskContribution: 88, icon: '📋' },
  { id: 'ACT_006', timestamp: '22:22:19', employeeId: 'EMP_001', employeeName: 'Aarav Mehta', actionType: 'data_access', system: 'CRM', detail: 'Updated 3 customer records — normal pattern', riskContribution: 2, icon: '📝' },
  { id: 'ACT_007', timestamp: '22:15:50', employeeId: 'EMP_089', employeeName: 'Suresh Nair', actionType: 'data_export', system: 'CBS Production', detail: 'Exported 12,400 records to CSV via VPN', riskContribution: 82, icon: '📤' },
  { id: 'ACT_008', timestamp: '22:10:33', employeeId: 'EMP_005', employeeName: 'Rohan Gupta', actionType: 'login', system: 'AML Platform', detail: 'Routine login — compliance shift', riskContribution: 1, icon: '🔑' },
  { id: 'ACT_009', timestamp: '21:58:12', employeeId: 'EMP_112', employeeName: 'Deepa Krishnan', actionType: 'cross_role_access', system: 'CBS', detail: 'Accessed customer financial records — HR scope violation', riskContribution: 65, icon: '🏦' },
  { id: 'ACT_010', timestamp: '21:45:28', employeeId: 'EMP_008', employeeName: 'Neha Verma', actionType: 'data_access', system: 'Treasury Platform', detail: 'Bond portfolio review — normal for role', riskContribution: 3, icon: '📈' },
];

// ─── Model Metrics ───────────────────────────────────────────────

export const modelMetrics: ModelMetrics = {
  f1: 0.873,
  precision: 0.841,
  recall: 0.908,
  aucRoc: 0.961,
  falsePositiveRate: 0.017,
  alertsToday: 4,
  employeesMonitored: 200,
  threatsDetected: 4,
};

// ─── Trust Score History (for sparklines) ────────────────────────

export const trustScoreHistory: Record<string, number[]> = {
  'EMP_047': [94, 94, 93, 95, 94, 92, 88, 75, 52, 38, 29, 23],
  'EMP_155': [78, 80, 79, 78, 77, 76, 72, 58, 35, 22, 18, 15],
  'EMP_089': [88, 87, 89, 88, 86, 82, 74, 62, 48, 40, 36, 34],
  'EMP_112': [85, 86, 84, 83, 80, 76, 68, 58, 52, 47, 44, 41],
  'EMP_001': [93, 94, 93, 95, 94, 95, 94, 93, 94, 95, 94, 94],
  'EMP_003': [90, 89, 91, 90, 88, 89, 90, 88, 89, 90, 88, 88],
};

// ─── Privilege Decay Timeline ────────────────────────────────────

export const privilegeDecayTimeline: PrivilegeDecayPoint[] = [
  { time: '09:00', trustScore: 95, event: 'Login (normal)' },
  { time: '09:15', trustScore: 97, event: 'CRM access (routine)' },
  { time: '10:30', trustScore: 96, event: null },
  { time: '12:00', trustScore: 94, event: 'Lunch break (decay)' },
  { time: '14:00', trustScore: 93, event: null },
  { time: '14:30', trustScore: 95, event: 'CRM access (routine)' },
  { time: '17:00', trustScore: 94, event: null },
  { time: '18:00', trustScore: 90, event: 'Still logged in (decay)' },
  { time: '19:00', trustScore: 85, event: 'After-hours (accelerated decay)' },
  { time: '20:00', trustScore: 78, event: null },
  { time: '21:00', trustScore: 68, event: 'Treasury access (!role)' },
  { time: '22:00', trustScore: 42, event: 'Bulk download (15×)' },
  { time: '22:30', trustScore: 29, event: 'USB connected' },
  { time: '22:47', trustScore: 23, event: 'File copy → ALERT' },
];

// ─── Digital Twin Profile ────────────────────────────────────────

export const sampleTwinProfile: TwinProfile = {
  expectedLogin: '09:15',
  actualLogin: '22:12',
  expectedSystems: ['CRM', 'CBS', 'Email'],
  actualSystems: ['CRM', 'CBS', 'Treasury DB', 'Email'],
  expectedRecords: 56,
  actualRecords: 847,
  expectedDataVolume: 2.3,
  actualDataVolume: 34.7,
  expectedDevices: 1,
  actualDevices: 2,
  dimensions: [
    { label: 'Login Time', expected: 85, actual: 12 },
    { label: 'Data Volume', expected: 45, actual: 95 },
    { label: 'System Access', expected: 60, actual: 88 },
    { label: 'USB Activity', expected: 0, actual: 90 },
    { label: 'Email Pattern', expected: 55, actual: 72 },
    { label: 'After Hours', expected: 5, actual: 95 },
    { label: 'Peer Alignment', expected: 88, actual: 15 },
    { label: 'Role Boundary', expected: 10, actual: 82 },
  ],
};

// ─── Department Stats ────────────────────────────────────────────

export const departmentStats = [
  { name: 'Retail Banking', employees: 60, avgTrust: 87.2, alerts: 1, color: '#06b6d4' },
  { name: 'Treasury', employees: 25, avgTrust: 88.5, alerts: 0, color: '#8b5cf6' },
  { name: 'IT Admin', employees: 35, avgTrust: 72.1, alerts: 2, color: '#f59e0b' },
  { name: 'HR', employees: 30, avgTrust: 79.8, alerts: 1, color: '#10b981' },
  { name: 'Compliance', employees: 50, avgTrust: 93.4, alerts: 0, color: '#ec4899' },
];

// ─── Helper Functions ────────────────────────────────────────────

export function getEmployee(id: string): Employee | undefined {
  return employees.find(e => e.id === id);
}

export function getAlertsByEmployee(id: string): Alert[] {
  return alerts.filter(a => a.employeeId === id);
}

export function getTrustColor(score: number): string {
  if (score < 20) return '#ef4444';
  if (score < 40) return '#f97316';
  if (score < 60) return '#eab308';
  if (score < 80) return '#22c55e';
  return '#06b6d4';
}

export function getTrustGradient(score: number): string {
  if (score < 20) return 'linear-gradient(135deg, #ef4444, #dc2626)';
  if (score < 40) return 'linear-gradient(135deg, #f97316, #ea580c)';
  if (score < 60) return 'linear-gradient(135deg, #eab308, #ca8a04)';
  if (score < 80) return 'linear-gradient(135deg, #22c55e, #16a34a)';
  return 'linear-gradient(135deg, #06b6d4, #0891b2)';
}
