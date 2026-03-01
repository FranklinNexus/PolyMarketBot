"""
╔══════════════════════════════════════════════════════════════════╗
║  LAPLACE VAULT — Quantitative Decision Engine                   ║
║  Fractional Kelly Sizing  ·  Binary Option Delta Hedging        ║
║  The Alpha Math · Production-Grade                              ║
╚══════════════════════════════════════════════════════════════════╝
"""

import math
from dataclasses import dataclass

from scipy.stats import norm


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DATA STRUCTURES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@dataclass
class MarketState:
    """实时市场状态的数据容器"""

    current_price: float  # 标的资产当前价格 (S)
    target_price: float  # 预测事件目标价 (K)
    time_to_expiry_years: float  # 距离结算的剩余时间(年) (τ)
    implied_volatility: float  # 标的资产隐含波动率 (σ)
    risk_free_rate: float  # 无风险利率 (r)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  QUANT ENGINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class LaplaceQuantEngine:
    """
    Laplace Vault 量化决策核心大脑

    Responsibilities:
        1. Fractional Kelly → How much capital to deploy
        2. Binary Option Δ → How much to short on Hyperliquid
    """

    def __init__(self, kelly_fraction: float = 0.25) -> None:
        # 激进透明：硬编码安全限制，防止极端计算错误导致满仓
        self.kelly_fraction: float = kelly_fraction
        self.max_position_limit: float = 0.10  # 单次最高动用资金 ≤ 10%

    # ── §1  Position Sizing (Kelly) ────────────────────────

    def calculate_optimal_buy_size(
        self,
        capital: float,
        p_true: float,
        p_market: float,
    ) -> float:
        """
        基于分数凯利判据计算 Polymarket 最佳下注金额.

        f* = c · (P_true − P_market) / (1 − P_market)

        Args:
            capital:  总可用资金 (USDC)
            p_true:   AI 预言机输出的真实概率
            p_market: Polymarket 盘面隐含概率

        Returns:
            optimal_investment: 应投入的 USDC 金额
        """
        if p_true <= p_market:
            return 0.0  # 没有 Edge → 拒绝下注

        # 凯利公式核心
        full_kelly: float = (p_true - p_market) / (1.0 - p_market)

        # 分数凯利 + 最大仓位熔断
        fractional_kelly: float = full_kelly * self.kelly_fraction
        safe_kelly: float = min(fractional_kelly, self.max_position_limit)

        optimal_investment: float = capital * safe_kelly
        return optimal_investment

    # ── §2  Binary Option Delta (Black-Scholes) ───────────

    def calculate_binary_delta(self, state: MarketState) -> float:
        """
        基于 Black-Scholes 计算 Cash-or-Nothing 二元看涨期权的动态 Delta.

        Δ_binary = e^{-rτ} · φ(d₂) / (S · σ · √τ)

        where d₂ = [ln(S/K) + (r − σ²/2)·τ] / (σ·√τ)

        Args:
            state: 当前市场状态快照

        Returns:
            delta: 单份二元期权对标的资产价格的敏感度
        """
        S: float = state.current_price
        K: float = state.target_price
        T: float = state.time_to_expiry_years
        sigma: float = state.implied_volatility
        r: float = state.risk_free_rate

        # 极端情况防爆：到期或零波动率
        if T <= 0 or sigma <= 0:
            return 0.0

        sqrt_T: float = math.sqrt(T)

        # d₂ 计算
        d2: float = (math.log(S / K) + (r - (sigma**2) / 2) * T) / (
            sigma * sqrt_T
        )

        # φ(d₂) — 标准正态 PDF
        pdf_d2: float = norm.pdf(d2)

        # Δ_binary
        delta: float = (math.exp(-r * T) * pdf_d2) / (S * sigma * sqrt_T)

        return delta

    # ── §3  Hedge Size Computation ─────────────────────────

    def get_hedge_order_size(
        self,
        pm_shares: float,
        market_state: MarketState,
    ) -> float:
        """
        输出 Hyperliquid 应做空的永续合约精确数量.

        hedge_size = Δ_binary × pm_shares

        Args:
            pm_shares:    Polymarket 持有的 YES 份额数量
            market_state: 当前市场状态

        Returns:
            hedge_size: 需在 Hyperliquid 做空的 BTC 数量
        """
        unit_delta: float = self.calculate_binary_delta(market_state)

        # 总 Delta 敞口 = 单份 Δ × 份数 → 开等额空单中和
        hedge_size: float = unit_delta * pm_shares

        return hedge_size


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LOCAL UNIT TEST / DRY RUN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    engine = LaplaceQuantEngine(kelly_fraction=0.30)

    # ── Scenario: 10,000 USDC vault capital ──
    vault_capital: float = 10_000.0

    # AI 输出 P_true = 65%, 盘面 P_market = 45%
    investment = engine.calculate_optimal_buy_size(
        vault_capital, p_true=0.65, p_market=0.45
    )
    pm_shares_bought: float = investment / 0.45

    print(
        f"💼 凯利资金管理 → 建议投入资金: {investment:.2f} USDC "
        f"(买入 {pm_shares_bought:.2f} 份 YES)"
    )

    # ── Simulated macro state ──
    current_state = MarketState(
        current_price=73_000.0,  # BTC 现价 73k
        target_price=75_000.0,  # 预测目标 75k
        time_to_expiry_years=0.08,  # ≈ 1 month to settlement
        implied_volatility=0.60,  # BTC IV 60%
        risk_free_rate=0.05,  # risk-free 5%
    )

    # ── Compute hedge ──
    unit_delta = engine.calculate_binary_delta(current_state)
    short_size = engine.get_hedge_order_size(pm_shares_bought, current_state)

    print(f"⚖️  动态期权参数 → 单份合约 Delta: {unit_delta:.6f}")
    print(f"🛡️ 跨链对冲指令 → 需在 Hyperliquid 做空 BTC 数量: {short_size:.4f} 枚")
