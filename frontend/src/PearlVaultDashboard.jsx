import { useState, useEffect, useCallback, useRef } from 'react';

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   PEARL VAULT — Premium Porcelain Dashboard  v5
   Hackathon Presentation Scale · Maximum Readability
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */

// ── Particles (module-scope) ────────────────────────────────────

const SPARKLE_PARTICLES = (() => {
  const drifters = Array.from({ length: 14 }, (_, i) => ({
    id: `d-${i}`,
    left: 3 + Math.random() * 94,
    delay: Math.random() * 20,
    duration: 16 + Math.random() * 18,
    size: 1.5 + Math.random() * 2.5,
    opacity: 0.08 + Math.random() * 0.14,
  }));
  const twinklers = Array.from({ length: 10 }, (_, i) => ({
    id: `t-${i}`,
    left: 5 + Math.random() * 90,
    top: 5 + Math.random() * 90,
    delay: Math.random() * 6,
    duration: 3 + Math.random() * 5,
    size: 1 + Math.random() * 1.5,
  }));
  return { drifters, twinklers };
})();

function AmbientSparkles() {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0" aria-hidden="true">
      {SPARKLE_PARTICLES.drifters.map((p) => (
        <div
          key={p.id}
          className="absolute rounded-full"
          style={{
            left: `${p.left}%`,
            bottom: '-8px',
            width: p.size,
            height: p.size,
            background: `radial-gradient(circle, rgba(255,195,210,${p.opacity}) 0%, rgba(216,191,216,${p.opacity * 0.4}) 100%)`,
            animation: `sparkle-drift ${p.duration}s linear ${p.delay}s infinite`,
          }}
        />
      ))}
      {SPARKLE_PARTICLES.twinklers.map((p) => (
        <div
          key={p.id}
          className="absolute rounded-full"
          style={{
            left: `${p.left}%`,
            top: `${p.top}%`,
            width: p.size,
            height: p.size,
            background: 'rgba(255, 200, 215, 0.2)',
            animation: `gem-twinkle ${p.duration}s ease-in-out ${p.delay}s infinite`,
          }}
        />
      ))}
    </div>
  );
}

// ── NekoClaw ────────────────────────────────────────────────────

function NekoClaw({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <ellipse cx="12" cy="15" rx="5.5" ry="4.5" fill="#FFB6C1" opacity="0.7"/>
      <circle cx="8" cy="10.5" r="2" fill="#FFD0D9"/>
      <circle cx="16" cy="10.5" r="2" fill="#FFD0D9"/>
      <circle cx="5.5" cy="13" r="1.5" fill="#FFD0D9"/>
      <circle cx="18.5" cy="13" r="1.5" fill="#FFD0D9"/>
      <path d="M7 8.5L8 10.5" stroke="#D8BFD8" strokeWidth="1.2" strokeLinecap="round"/>
      <path d="M17 8.5L16 10.5" stroke="#D8BFD8" strokeWidth="1.2" strokeLinecap="round"/>
      <path d="M4.5 11L5.5 13" stroke="#D8BFD8" strokeWidth="1.2" strokeLinecap="round"/>
      <path d="M19.5 11L18.5 13" stroke="#D8BFD8" strokeWidth="1.2" strokeLinecap="round"/>
      <ellipse cx="12" cy="16" rx="2" ry="1.5" fill="#FFDCE4"/>
    </svg>
  );
}

// ── Engine log feed ─────────────────────────────────────────────

const ENGINE_FEED = [
  { ms: 250,  icon: '🐚', text: 'Pearl Vault v0.1.0 · Porcelain Mode · DRY-RUN',              tone: 'muted' },
  { ms: 600,  icon: '🧠', text: 'AI Oracle ingesting on-chain + off-chain feature matrix…',    tone: 'base' },
  { ms: 900,  icon: '🧠', text: 'Bayesian posterior updated · P_true(BTC>75k) = 0.652',         tone: 'good' },
  { ms: 500,  icon: '🧠', text: 'Polymarket implied = 0.450 · Edge = +20.2%',                   tone: 'accent' },
  { ms: 400,  icon: '✨', text: 'EDGE EXCEEDS THRESHOLD — TRIGGERING EXECUTION',                tone: 'good' },
  { ms: 550,  icon: ' ',  text: '────────────────────────────────────────────────',              tone: 'muted' },
  { ms: 450,  icon: '🦄', text: 'Cross-chain atomic hedge initiated…',                          tone: 'base' },
  { ms: 300,  icon: '🦄', text: 'asyncio.gather() → 2 concurrent legs dispatched',              tone: 'muted' },
  { ms: 550,  icon: ' ',  text: '────────────────────────────────────────────────',              tone: 'muted' },
  { ms: 400,  icon: '🌸', text: '[POLY-L2] ClobClient initialized · chain_id=137 (Polygon)',    tone: 'base' },
  { ms: 500,  icon: '🌸', text: '[POLY-L2] Building order · side=BUY price=0.50 size=100',      tone: 'base' },
  { ms: 350,  icon: '🌸', text: '[POLY-L2] GET /tick-size → 200 OK',                            tone: 'muted' },
  { ms: 250,  icon: '🌸', text: '[POLY-L2] GET /neg-risk → 200 OK',                             tone: 'muted' },
  { ms: 250,  icon: '🌸', text: '[POLY-L2] GET /fee-rate → 200 OK',                             tone: 'muted' },
  { ms: 650,  icon: '🌸', text: '[POLY-L2] ✓ Order SIGNED · EIP-712 · sig=0xf774…1b',           tone: 'good' },
  { ms: 400,  icon: '🌸', text: '[POLY-L2] DRY-RUN · post_order() INTERCEPTED',                 tone: 'accent' },
  { ms: 300,  icon: '🌸', text: '[POLY-L2] → tx = Tx_Hash_Mocked_Polymarket',                   tone: 'accent' },
  { ms: 550,  icon: ' ',  text: '────────────────────────────────────────────────',              tone: 'muted' },
  { ms: 400,  icon: '💎', text: '[HL-L1] Exchange initialized · addr=0x4728… (mainnet)',        tone: 'base' },
  { ms: 500,  icon: '💎', text: '[HL-L1] Preparing SHORT · coin=BTC · size=0.001 · slip=1%',   tone: 'base' },
  { ms: 600,  icon: '💎', text: '[HL-L1] DRY-RUN · market_open() INTERCEPTED',                  tone: 'accent' },
  { ms: 300,  icon: '💎', text: '[HL-L1] → tx = Tx_Hash_Mocked_Hyperliquid',                    tone: 'accent' },
  { ms: 550,  icon: ' ',  text: '────────────────────────────────────────────────',              tone: 'muted' },
  { ms: 500,  icon: '✅', text: 'BOTH LEGS EXECUTED SUCCESSFULLY · Δt=2,158ms',                  tone: 'good' },
  { ms: 400,  icon: '🛡️', text: 'Leg-Break check: PASSED · No naked exposure',                  tone: 'good' },
  { ms: 400,  icon: '⚖️',  text: 'Net Δ computed: 0.000 · MARKET-NEUTRAL',                      tone: 'good' },
  { ms: 500,  icon: '🐚', text: 'PEARL VAULT — HEDGE COMPLETE — ANTI-FRAGILE ✧',                tone: 'final' },
  { ms: 300,  icon: '🌟', text: 'Engine shutdown · 0 errors · kirakira ♪',                      tone: 'muted' },
];

const TONE = {
  muted:  'text-[#B8B8B8]',
  base:   'text-[#555555]',
  good:   'text-[#D4878F]',
  accent: 'text-[#B594C0]',
  final:  'text-[#E8879B] font-semibold',
};

// ── Metric data ─────────────────────────────────────────────────

const METRICS = [
  { label: 'Target Event',            value: 'BTC > $75K',   sub: 'Jun 2026' },
  { label: 'Polymarket Implied',      value: '45.0 ¢',       sub: '−2.3 ¢' },
  { label: 'AI True Probability',     value: '65.2 %',       sub: '+4.1 %' },
  { label: 'Sparkle Margin ✨',       value: '20.2 %',       sub: '+6.4 %' },
  { label: 'Equity Balancer 💖',      value: '0.00 Δ',       sub: 'Neutral' },
];

// ── Main Dashboard ──────────────────────────────────────────────

export default function PearlVaultDashboard() {
  const [running, setRunning] = useState(false);
  const [logs, setLogs] = useState([]);
  const [done, setDone] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const ignite = useCallback(async () => {
    setRunning(true);
    setLogs([]);
    setDone(false);
    for (const entry of ENGINE_FEED) {
      await new Promise((r) => setTimeout(r, entry.ms));
      setLogs((prev) => [...prev, entry]);
    }
    setRunning(false);
    setDone(true);
  }, []);

  return (
    <div className="min-h-screen w-full bg-[#FFFFFF] bg-gradient-to-b from-[#FFFFFF] via-[#FDFDFF] to-[#FFF9FA] text-[#4A4A4A] font-sans px-12 py-10 flex flex-col gap-10 relative">

      <AmbientSparkles />

      {/* ━━ Header ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */}
      <header
        className="flex justify-between items-end border-b border-[#ECECEC] pb-6 relative z-10"
        style={{ animation: 'glide-up 0.5s cubic-bezier(0.25,0.46,0.45,0.94) both' }}
      >
        <div className="flex items-baseline gap-5">
          <div className="flex items-center gap-3">
            <NekoClaw size={36} />
            <h1 className="text-5xl font-light tracking-tighter text-[#2D2D2D]">Pearl Vault</h1>
          </div>
          <span className="text-sm tracking-[0.25em] text-[#FFB6C1] font-bold uppercase">Anti-Fragile</span>
        </div>
        <div className="flex items-center gap-5">
          <span className="text-xs tracking-[0.15em] text-[#A0A0A0] uppercase font-medium">
            System Status: Optimal
          </span>
          <span className="text-xs tracking-[0.15em] text-[#B0B0B0] uppercase font-medium px-3 py-1.5 rounded-full border border-[#E8E8E8]">
            DRY-RUN
          </span>
        </div>
      </header>

      {/* ━━ Metrics — 5 large cards ━━━━━━━━━━━━━━━ */}
      <div
        className="grid grid-cols-1 md:grid-cols-5 gap-6 relative z-10"
        style={{ animation: 'glide-up 0.55s cubic-bezier(0.25,0.46,0.45,0.94) 0.1s both' }}
      >
        {METRICS.map((item, i) => (
          <div
            key={i}
            className="bg-white border border-[#F0F0F0] rounded-[24px] p-7 shadow-[0_8px_30px_-12px_rgba(0,0,0,0.04)] hover:border-[#FFC0CB]/30 transition-all duration-700 group"
          >
            <p className="text-xs uppercase tracking-[0.15em] text-[#B0B0B0] mb-3 group-hover:text-[#FFB6C1] transition-colors duration-500 font-semibold">
              {item.label}
            </p>
            <p className="text-4xl font-light tracking-tight text-[#2D2D2D]">
              {item.value}
            </p>
            <p className="text-sm text-[#C0C0C0] mt-2 font-medium">{item.sub}</p>
          </div>
        ))}
      </div>

      {/* ━━ Risk Parameters ━━━━━━━━━━━━━━━━━━━━━━━ */}
      <div
        className="w-full bg-white border border-[#F0F0F0] rounded-[20px] px-10 py-7 relative z-10 shadow-[0_4px_20px_-10px_rgba(0,0,0,0.02)]"
        style={{ animation: 'glide-up 0.55s cubic-bezier(0.25,0.46,0.45,0.94) 0.2s both' }}
      >
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-8">
          {[
            ['Strategy',     'Delta-Neutral',   false],
            ['Kelly c',      '0.25',            false],
            ['Max Position', '≤ 10%',           false],
            ['Slippage',     '1.00 %',          false],
            ['Leg-Break',    'ACTIVE',           true],
            ['Concurrency',  'asyncio.gather',  false],
            ['Kill Switch',  'DRY_RUN',          true],
          ].map(([label, value, accent], i) => (
            <div key={i} className="flex flex-col gap-1.5">
              <span className="text-xs uppercase tracking-[0.15em] text-[#B0B0B0] font-semibold">{label}</span>
              <span className={`text-base font-semibold ${accent ? 'text-[#D4878F]' : 'text-[#3D3D3D]'}`}>{value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ━━ Terminal ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */}
      <div
        className="flex-1 flex flex-col min-h-[360px] relative z-10"
        style={{ animation: 'glide-up 0.55s cubic-bezier(0.25,0.46,0.45,0.94) 0.3s both' }}
      >
        <div className="flex-1 bg-white border border-[#ECECEC] rounded-[32px] shadow-[inset_0_2px_10px_rgba(0,0,0,0.01)] p-10 flex flex-col relative overflow-hidden">

          {/* Terminal header */}
          <div className="flex items-center gap-3 mb-6">
            {running && <div className="w-2 h-2 rounded-full bg-[#FFB6C1] animate-pulse" />}
            {!running && !done && <div className="w-2 h-2 rounded-full bg-[#DCDCDC]" />}
            {done && <div className="w-2 h-2 rounded-full bg-[#B8D8BA]" />}
            <span className="text-sm font-bold tracking-[0.2em] text-[#C8C8C8] uppercase">
              Deep-Sea Execution
            </span>
          </div>

          {/* Log content */}
          <div className="flex-1 font-mono text-[15px] leading-[2] overflow-y-auto pr-4">
            {logs.length === 0 && !running && !done && (
              <p className="text-[#CCCCCC] italic font-sans text-base">awaiting ignition… ✧</p>
            )}

            {logs.map((entry, i) => (
              <div
                key={i}
                className={`flex items-start gap-3 ${TONE[entry.tone]}`}
                style={{ animation: 'text-fade-in 0.25s ease-out both' }}
              >
                <span className="shrink-0 w-7 text-center text-lg leading-[2]">
                  {entry.icon.trim() || ''}
                </span>
                <span>{entry.text}</span>
              </div>
            ))}

            {running && (
              <div className="mt-2">
                <span
                  className="inline-block w-[6px] h-[16px] rounded-sm bg-[#FFB6C1]/50"
                  style={{ animation: 'soft-pulse 0.8s ease-in-out infinite' }}
                />
              </div>
            )}
            <div ref={scrollRef} />
          </div>
        </div>
      </div>

      {/* ━━ Success badges ━━━━━━━━━━━━━━━━━━━━━━━━ */}
      {done && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 relative z-10 mb-28">
          {[
            { icon: '🌸', text: 'Polymarket — Signed & Intercepted' },
            { icon: '💎', text: 'Hyperliquid — Signed & Intercepted' },
            { icon: '💖', text: 'Δ = 0.00 · Anti-Fragile' },
          ].map((b, i) => (
            <div
              key={i}
              className="bg-white border border-[#F0F0F0] rounded-[18px] px-6 py-5 text-center text-base font-medium text-[#555555] shadow-[0_4px_20px_-10px_rgba(0,0,0,0.03)]"
              style={{ animation: `glide-up 0.45s cubic-bezier(0.25,0.46,0.45,0.94) ${i * 0.12}s both` }}
            >
              <span className="mr-2 text-lg">{b.icon}</span>{b.text}
            </div>
          ))}
        </div>
      )}

      {/* ━━ Fixed floating button — LARGE ━━━━━━━━━ */}
      <div className="fixed bottom-10 left-1/2 -translate-x-1/2 z-50">
        <button
          className="whitespace-nowrap px-20 py-6 bg-[#FFB6C1] text-white rounded-full text-xl font-semibold tracking-wide shadow-[0_15px_40px_-8px_rgba(255,182,193,0.45)] hover:shadow-[0_20px_50px_-8px_rgba(255,182,193,0.55)] transform hover:-translate-y-1 transition-all duration-500 active:scale-95 flex items-center justify-center gap-5 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:translate-y-0"
          onClick={ignite}
          disabled={running}
        >
          {running ? (
            <>
              <span className="inline-block w-6 h-6 border-[3px] border-white/30 border-t-white rounded-full animate-spin" />
              <span>Working…</span>
            </>
          ) : (
            <>
              <span className="text-2xl">🌸</span>
              <span>Ignite Magical Hedge Engine</span>
            </>
          )}
        </button>
      </div>

      {/* ━━ Footer ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */}
      <footer className="text-center pb-20 relative z-10">
        <p className="text-xs tracking-[0.2em] text-[#C8C8C8] uppercase font-medium">
          Pearl Vault · Cross-Chain Delta-Neutral · Anti-Fragile by Design
        </p>
      </footer>
    </div>
  );
}
