import { useState, useEffect, useCallback, useRef } from 'react';

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   LAPLACE VAULT — KiraKira Porcelain Dashboard
   Cyber-Cute × Premium Glossy White × Delta-Neutral
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */

// ── Sparkle particle component ─────────────────────────────────

function SparkleField() {
  const [sparkles, setSparkles] = useState([]);

  useEffect(() => {
    const particles = Array.from({ length: 30 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      delay: Math.random() * 12,
      duration: 8 + Math.random() * 10,
      size: 3 + Math.random() * 6,
      type: Math.random() > 0.5 ? 'star' : 'circle',
    }));
    setSparkles(particles);
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {sparkles.map((s) => (
        <div
          key={s.id}
          className="absolute"
          style={{
            left: `${s.left}%`,
            bottom: '-10px',
            width: s.size,
            height: s.size,
            borderRadius: s.type === 'circle' ? '50%' : '2px',
            background:
              s.type === 'circle'
                ? 'radial-gradient(circle, rgba(255,182,193,0.6) 0%, rgba(216,191,216,0.3) 100%)'
                : 'linear-gradient(45deg, rgba(255,182,193,0.5), rgba(216,191,216,0.5))',
            transform: s.type === 'star' ? 'rotate(45deg)' : 'none',
            animation: `sparkle-float ${s.duration}s ease-in-out ${s.delay}s infinite`,
          }}
        />
      ))}

      {/* Static twinkle dots */}
      {Array.from({ length: 20 }, (_, i) => (
        <div
          key={`twinkle-${i}`}
          className="absolute rounded-full"
          style={{
            left: `${5 + Math.random() * 90}%`,
            top: `${5 + Math.random() * 90}%`,
            width: 2 + Math.random() * 3,
            height: 2 + Math.random() * 3,
            background: `rgba(255, 182, 193, ${0.15 + Math.random() * 0.25})`,
            animation: `sparkle-twinkle ${2 + Math.random() * 3}s ease-in-out ${Math.random() * 4}s infinite`,
          }}
        />
      ))}
    </div>
  );
}

// ── Cute icon components (no external libs) ────────────────────

function HeartIcon({ className = '' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
    </svg>
  );
}

function SparkleIcon({ className = '' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
      <path d="M12 2l2.4 7.2H22l-6 4.8 2.4 7.2L12 16.4l-6.4 4.8L8 14 2 9.2h7.6z"/>
    </svg>
  );
}

function ShieldIcon({ className = '' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
      <path d="M12 2L4 5v6.09c0 5.05 3.41 9.76 8 10.91 4.59-1.15 8-5.86 8-10.91V5l-8-3zm-1 15l-4-4 1.41-1.41L11 14.17l6.59-6.59L19 9l-8 8z"/>
    </svg>
  );
}

function BalancerIcon({ className = '' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
      <path d="M12 3v18M4 9h16M4 15h16M7 6l5-3 5 3M7 18l5 3 5-3"/>
      <circle cx="12" cy="12" r="2"/>
      <path d="M4 9c0-1 1-2 2-2h12c1 0 2 1 2 2M4 15c0 1 1 2 2 2h12c1 0 2-1 2-2" fill="none" stroke="currentColor" strokeWidth="1.5"/>
    </svg>
  );
}

function DiamondIcon({ className = '' }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
      <path d="M12 2l10 10-10 10L2 12z" opacity="0.8"/>
    </svg>
  );
}

// ── Metric Card ────────────────────────────────────────────────

function MetricCard({ icon, label, value, subValue, delay = 0 }) {
  return (
    <div
      className="porcelain-card p-5 flex flex-col gap-2 relative z-10"
      style={{
        animation: `slide-in-up 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${delay}s both`,
      }}
    >
      <div className="flex items-center gap-2">
        <span className="text-sakura opacity-70">{icon}</span>
        <span className="text-[0.7rem] font-medium tracking-wider uppercase text-rose-gray-light">
          {label}
        </span>
      </div>
      <div className="text-2xl font-bold tracking-tight text-rose-gray" style={{ fontVariantNumeric: 'tabular-nums' }}>
        {value}
      </div>
      {subValue && (
        <span className="text-[0.72rem] text-sakura-deep font-medium">{subValue}</span>
      )}
    </div>
  );
}

// ── Engine Log Feed ────────────────────────────────────────────

const LOG_FEED = [
  { delay: 300,  icon: '🔮', text: 'Laplace Vault v0.1.0 · KiraKira Mode · DRY-RUN active',       type: 'dim' },
  { delay: 500,  icon: '🧠', text: 'AI Oracle ingesting on-chain feature matrix…',                 type: 'info' },
  { delay: 800,  icon: '🧠', text: 'Bayesian posterior updated · P_true(BTC>75k) = 0.652',          type: 'success' },
  { delay: 500,  icon: '🧠', text: 'Polymarket implied = 0.450 · Edge = +20.2%',                    type: 'accent' },
  { delay: 400,  icon: '✨', text: 'EDGE EXCEEDS THRESHOLD — TRIGGERING EXECUTION',                 type: 'success' },
  { delay: 600,  icon: '💫', text: '────────────────────────────────────────',                       type: 'dim' },
  { delay: 500,  icon: '🦄', text: 'Initiating cross-chain atomic hedge…',                          type: 'info' },
  { delay: 300,  icon: '🦄', text: 'asyncio.gather() → 2 concurrent legs dispatched',               type: 'dim' },
  { delay: 700,  icon: '💫', text: '────────────────────────────────────────',                       type: 'dim' },
  { delay: 400,  icon: '🌸', text: '[POLY-L2] ClobClient initialized · chain_id=137',               type: 'info' },
  { delay: 500,  icon: '🌸', text: '[POLY-L2] Building order · side=BUY price=0.50 size=100',       type: 'info' },
  { delay: 600,  icon: '🌸', text: '[POLY-L2] ✓ Order SIGNED · EIP-712',                            type: 'success' },
  { delay: 400,  icon: '🌸', text: '[POLY-L2] DRY-RUN · post_order() INTERCEPTED',                  type: 'accent' },
  { delay: 300,  icon: '🌸', text: '[POLY-L2] → tx = Tx_Hash_Mocked_Polymarket',                    type: 'accent' },
  { delay: 700,  icon: '💫', text: '────────────────────────────────────────',                       type: 'dim' },
  { delay: 400,  icon: '💎', text: '[HL-L1] Exchange initialized · mainnet',                        type: 'info' },
  { delay: 500,  icon: '💎', text: '[HL-L1] Preparing SHORT · BTC · size=0.001',                    type: 'info' },
  { delay: 600,  icon: '💎', text: '[HL-L1] DRY-RUN · market_open() INTERCEPTED',                   type: 'accent' },
  { delay: 300,  icon: '💎', text: '[HL-L1] → tx = Tx_Hash_Mocked_Hyperliquid',                     type: 'accent' },
  { delay: 700,  icon: '💫', text: '────────────────────────────────────────',                       type: 'dim' },
  { delay: 500,  icon: '✅', text: 'BOTH LEGS EXECUTED SUCCESSFULLY · Δt=2,158ms',                   type: 'success' },
  { delay: 400,  icon: '🛡️', text: 'Leg-Break check: PASSED · No naked exposure',                   type: 'success' },
  { delay: 400,  icon: '⚖️',  text: 'Net Δ = 0.000 · Position is MARKET-NEUTRAL',                   type: 'success' },
  { delay: 500,  icon: '💖', text: 'HEDGE COMPLETE — ANTI-FRAGILE POSITION LOCKED',                  type: 'final' },
  { delay: 300,  icon: '🌟', text: 'Engine shutdown · 0 errors · 0 warnings · kirakira ♪',          type: 'dim' },
];

const LOG_COLORS = {
  dim:     'text-rose-gray-faint',
  info:    'text-rose-gray',
  success: 'text-sakura-deep',
  accent:  'text-unicorn-deep',
  final:   'text-sakura font-bold',
};

// ── Main Dashboard ─────────────────────────────────────────────

export default function KiraKiraDashboard() {
  const [engineRunning, setEngineRunning] = useState(false);
  const [logs, setLogs] = useState([]);
  const [engineComplete, setEngineComplete] = useState(false);
  const logEndRef = useRef(null);

  const scrollToBottom = useCallback(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [logs, scrollToBottom]);

  const runEngine = useCallback(async () => {
    setEngineRunning(true);
    setLogs([]);
    setEngineComplete(false);

    for (const entry of LOG_FEED) {
      await new Promise((r) => setTimeout(r, entry.delay));
      setLogs((prev) => [...prev, entry]);
    }

    setEngineRunning(false);
    setEngineComplete(true);
  }, []);

  return (
    <div className="relative min-h-screen">
      <SparkleField />

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-8">
        {/* ── Navbar ──────────────────────────────────── */}
        <nav
          className="flex items-center justify-between mb-10"
          style={{ animation: 'slide-in-up 0.5s cubic-bezier(0.4,0,0.2,1) both' }}
        >
          <div className="flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-2xl flex items-center justify-center text-white text-lg font-bold"
              style={{
                background: 'linear-gradient(135deg, #FFB6C1, #D8BFD8)',
                boxShadow: '0 4px 16px rgba(255,182,193,0.3)',
              }}
            >
              ◈
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-rose-gray">
                Laplace Vault
              </h1>
              <p className="text-[0.65rem] text-rose-gray-light tracking-widest uppercase">
                Cross-Chain Yield · Delta-Neutral · Anti-Fragile
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="px-3 py-1 rounded-full text-[0.68rem] font-semibold tracking-wider border"
              style={{
                color: '#FFB6C1',
                borderColor: 'rgba(255,182,193,0.3)',
                background: 'rgba(255,182,193,0.06)',
              }}
            >
              DRY-RUN 🏜️
            </span>
            <span className="px-3 py-1 rounded-full text-[0.68rem] font-semibold tracking-wider border"
              style={{
                color: '#D8BFD8',
                borderColor: 'rgba(216,191,216,0.3)',
                background: 'rgba(216,191,216,0.06)',
              }}
            >
              ENGINE ONLINE ✧
            </span>
          </div>
        </nav>

        {/* ── Metrics Row ─────────────────────────────── */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
          <MetricCard
            icon={<SparkleIcon />}
            label="Target Event"
            value="BTC > $75K"
            subValue="Jun 2026"
            delay={0.1}
          />
          <MetricCard
            icon={<DiamondIcon />}
            label="Polymarket Implied"
            value="45.0 ¢"
            subValue="−2.3 ¢"
            delay={0.2}
          />
          <MetricCard
            icon={<HeartIcon />}
            label="AI True Probability"
            value="65.2 %"
            subValue="+4.1 %"
            delay={0.3}
          />
          <MetricCard
            icon={<SparkleIcon />}
            label="Estimated Sparkle Margin ✨"
            value="20.2 %"
            subValue="+6.4 %"
            delay={0.4}
          />
          <MetricCard
            icon={<BalancerIcon />}
            label="Total Equity Balancer 💖"
            value="0.00 Δ"
            subValue="Neutral ✓"
            delay={0.5}
          />
        </div>

        {/* ── Strategy + Risk Cards ───────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-8">
          <div
            className="porcelain-card p-6 relative z-10"
            style={{ animation: 'slide-in-up 0.6s cubic-bezier(0.4,0,0.2,1) 0.3s both' }}
          >
            <h3 className="text-[0.7rem] font-semibold tracking-[0.15em] uppercase text-rose-gray-light mb-4 flex items-center gap-2">
              <span className="text-sakura">◈</span> Position Architecture
            </h3>
            <div className="space-y-2.5">
              {[
                ['LEG A · LONG', 'Polymarket YES Shares'],
                ['Chain', 'Polygon L2'],
                ['Size', '100 shares @ 0.50'],
                ['LEG B · SHORT', 'Hyperliquid BTC-PERP'],
                ['Chain', 'Hyperliquid L1'],
                ['Size', '0.001 BTC @ Market'],
                ['Net Delta', '≈ 0.00  (Hedged) 💖'],
              ].map(([k, v], i) => (
                <div key={i} className="flex justify-between items-center py-1.5 border-b border-sakura-pale/40 last:border-0">
                  <span className="text-[0.75rem] text-rose-gray-faint">{k}</span>
                  <span className={`text-[0.78rem] font-medium ${v.includes('Hedged') ? 'text-sakura-deep' : 'text-rose-gray'}`}>
                    {v}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div
            className="porcelain-card p-6 relative z-10"
            style={{ animation: 'slide-in-up 0.6s cubic-bezier(0.4,0,0.2,1) 0.4s both' }}
          >
            <h3 className="text-[0.7rem] font-semibold tracking-[0.15em] uppercase text-rose-gray-light mb-4 flex items-center gap-2">
              <span className="text-unicorn">◈</span> Risk Parameters
            </h3>
            <div className="space-y-2.5">
              {[
                ['Strategy', 'Delta-Neutral Basis'],
                ['Kelly Fraction', 'c = 0.25 (Conservative)'],
                ['Max Drawdown', '0.5 % (capped)'],
                ['Slippage Tolerance', '1.00 %'],
                ['Leg-Break Protection', 'ACTIVE ✧'],
                ['Concurrency', 'asyncio.gather (2 legs)'],
                ['Kill Switch', 'DRY_RUN = True 🛡️'],
              ].map(([k, v], i) => (
                <div key={i} className="flex justify-between items-center py-1.5 border-b border-unicorn-pale/40 last:border-0">
                  <span className="text-[0.75rem] text-rose-gray-faint">{k}</span>
                  <span className={`text-[0.78rem] font-medium ${v.includes('ACTIVE') || v.includes('True') ? 'text-sakura-deep' : 'text-rose-gray'}`}>
                    {v}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── Ignition Button ─────────────────────────── */}
        <div
          className="flex justify-center mb-8"
          style={{ animation: 'slide-in-up 0.6s cubic-bezier(0.4,0,0.2,1) 0.5s both' }}
        >
          <button
            className="macaron-btn px-12 py-4 text-base disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={runEngine}
            disabled={engineRunning}
          >
            {engineRunning ? (
              <span className="flex items-center gap-2">
                <span className="inline-block w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
                Engine Working…
              </span>
            ) : (
              '🔥 Ignite Magical Hedge Engine'
            )}
          </button>
        </div>

        {/* ── Terminal Log Box ────────────────────────── */}
        <div
          className="relative z-10"
          style={{ animation: 'slide-in-up 0.6s cubic-bezier(0.4,0,0.2,1) 0.6s both' }}
        >
          <div className="unicorn-border">
            <div className="unicorn-border-inner p-6">
              {/* Window dots */}
              <div className="flex items-center gap-1.5 mb-4 pb-3 border-b border-sakura-pale/30">
                <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#FFB6C1' }} />
                <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#D8BFD8' }} />
                <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#FFE4E9' }} />
                <span className="ml-3 text-[0.62rem] text-rose-gray-faint tracking-widest uppercase">
                  Execution Terminal
                </span>
              </div>

              {/* Log lines */}
              <div className="h-80 overflow-y-auto font-mono text-[0.78rem] leading-relaxed space-y-0.5">
                {logs.length === 0 && !engineRunning && !engineComplete && (
                  <p className="text-rose-gray-faint italic">
                    awaiting ignition… ✧
                  </p>
                )}

                {logs.map((entry, i) => (
                  <div
                    key={i}
                    className={`flex items-start gap-2 ${LOG_COLORS[entry.type] || 'text-rose-gray'}`}
                    style={{
                      animation: `text-appear 0.3s ease-out both`,
                    }}
                  >
                    <span className="shrink-0 w-5 text-center">{entry.icon}</span>
                    <span>{entry.text}</span>
                  </div>
                ))}

                {engineRunning && (
                  <div className="flex items-center gap-2 text-sakura mt-1">
                    <span className="inline-block w-1.5 h-4 bg-sakura animate-pulse rounded-sm" />
                  </div>
                )}
                <div ref={logEndRef} />
              </div>
            </div>
          </div>
        </div>

        {/* ── Result Badges ───────────────────────────── */}
        {engineComplete && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
            {[
              { icon: '🌸', text: 'Polymarket Leg — Signed & Intercepted' },
              { icon: '💎', text: 'Hyperliquid Leg — Signed & Intercepted' },
              { icon: '💖', text: 'Delta = 0.00 · Anti-Fragile' },
            ].map((badge, i) => (
              <div
                key={i}
                className="porcelain-card px-5 py-3 text-center text-[0.78rem] font-medium text-rose-gray relative z-10"
                style={{
                  animation: `slide-in-up 0.5s cubic-bezier(0.4,0,0.2,1) ${i * 0.15}s both`,
                  borderColor: 'rgba(255,182,193,0.25)',
                }}
              >
                <span className="mr-2">{badge.icon}</span>
                {badge.text}
              </div>
            ))}
          </div>
        )}

        {/* ── Footer ──────────────────────────────────── */}
        <footer className="mt-12 pb-8 text-center">
          <p className="text-[0.62rem] text-rose-gray-faint tracking-[0.18em] uppercase">
            Laplace Vault · 48H Hackathon · Cross-Chain Delta-Neutral · Anti-Fragile by Design · KiraKira ✧
          </p>
        </footer>
      </div>
    </div>
  );
}
