#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  LAPLACE VAULT — Cross-Chain Delta-Neutral Execution Engine     ║
║  Concurrent Polymarket Buy  ⟷  Hyperliquid Perp Short           ║
║  Anti-fragile MVP · Hackathon Edition                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timezone

import eth_account
from dotenv import load_dotenv
from eth_account.signers.local import LocalAccount

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants as hl_constants

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs
from py_clob_client.constants import POLYGON
from py_clob_client.order_builder.constants import BUY

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  §0  LOGGING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
log = logging.getLogger("laplace")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  §1  CONFIG — Environment + Hard-Coded MVP Parameters
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

load_dotenv()

# ┌──────────────────────────────────────────────────────────┐
# │  🛡️  ANTI-FRAGILE GLOBAL KILL-SWITCH                     │
# │  When True  → intercepts ALL order submissions           │
# │  When False → LIVE FIRE — real money on the line         │
# └──────────────────────────────────────────────────────────┘
DRY_RUN: bool = True

# — Polymarket credentials (Polygon chain) —
POLYGON_PRIVATE_KEY: str = os.getenv("POLYGON_PRIVATE_KEY", "")
POLY_WALLET_ADDRESS: str = os.getenv("POLY_WALLET_ADDRESS", "")
POLY_API_KEY: str = os.getenv("POLY_API_KEY", "")
POLY_API_SECRET: str = os.getenv("POLY_API_SECRET", "")
POLY_API_PASSPHRASE: str = os.getenv("POLY_API_PASSPHRASE", "")
POLY_HOST: str = os.getenv("POLY_HOST", "https://clob.polymarket.com")

# — Hyperliquid credentials —
HYPERLIQUID_PRIVATE_KEY: str = os.getenv("HYPERLIQUID_PRIVATE_KEY", "")
HL_WALLET_ADDRESS: str = os.getenv("HL_WALLET_ADDRESS", "")
# Toggle: hl_constants.MAINNET_API_URL  /  hl_constants.TESTNET_API_URL
HL_BASE_URL: str = os.getenv("HL_BASE_URL", hl_constants.MAINNET_API_URL)

# — MVP hard-coded trade parameters —
# Polymarket: target event token + buy params
POLY_TOKEN_ID: str = "73470541315377973562501025254719659796416871135081220986683321361000395461644"
POLY_BUY_PRICE: float = 0.50       # limit price per YES share
POLY_BUY_SIZE: float = 100.0       # number of YES shares

# Hyperliquid: hedge asset + short params
HL_HEDGE_COIN: str = "BTC"
HL_SHORT_SIZE: float = 0.001       # BTC perpetual short size
HL_SLIPPAGE: float = 0.01          # 1 % slippage tolerance


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  §2  POLYMARKET LEG — Client Init + Async Buy
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _init_polymarket_client() -> ClobClient:
    """Authenticate & return a ready-to-fire ClobClient."""
    creds = ApiCreds(
        api_key=POLY_API_KEY,
        api_secret=POLY_API_SECRET,
        api_passphrase=POLY_API_PASSPHRASE,
    )
    client = ClobClient(
        POLY_HOST,
        key=POLYGON_PRIVATE_KEY,
        chain_id=POLYGON,
        creds=creds,
    )
    log.info(">>> [Polymarket] ClobClient initialised  · chain_id=%s", POLYGON)
    return client


def _polymarket_buy_sync(client: ClobClient) -> dict:
    """Synchronous Polymarket limit-buy — called inside asyncio.to_thread."""
    order_args = OrderArgs(
        price=POLY_BUY_PRICE,
        size=POLY_BUY_SIZE,
        side=BUY,
        token_id=POLY_TOKEN_ID,
    )
    log.info(
        ">>> [Polymarket] Building order  · side=BUY  price=%.4f  size=%.2f",
        POLY_BUY_PRICE,
        POLY_BUY_SIZE,
    )

    # — Sign the order (always real — costs nothing) —
    signed_order = client.create_order(order_args)
    log.info(">>> [Polymarket] ✅ Order SIGNED  · details=%s", signed_order)
    # ── DRY-RUN GATE ──────────────────────────────────────
    if DRY_RUN:
        log.warning(
            "╔══════════════════════════════════════════════════════╗\n"
            "             ║  🏜️  DRY-RUN · Polymarket post_order INTERCEPTED    ║\n"
            "             ║  SIDE   = BUY                                       ║\n"
            "             ║  PRICE  = %-10.4f                                 ║\n"
            "             ║  SIZE   = %-10.2f                                 ║\n"
            "             ║  TOKEN  = %s…  ║\n"
            "             ╚══════════════════════════════════════════════════════╝",
            POLY_BUY_PRICE,
            POLY_BUY_SIZE,
            POLY_TOKEN_ID[:24],
        )
        return {
            "status": "ok",
            "dry_run": True,
            "tx_hash": "Tx_Hash_Mocked_Polymarket",
            "detail": {
                "side": "BUY",
                "price": POLY_BUY_PRICE,
                "size": POLY_BUY_SIZE,
                "token_id": POLY_TOKEN_ID,
            },
        }
    # ── LIVE FIRE ─────────────────────────────────────────
    resp = client.post_order(signed_order)
    log.info(">>> [Polymarket] 🔥 Order POSTED  · response=%s", resp)
    return resp


async def execute_polymarket_buy() -> dict:
    """Async wrapper — spins up client, fires buy in a thread."""
    try:
        client = _init_polymarket_client()
        result = await asyncio.to_thread(_polymarket_buy_sync, client)
        return result
    except Exception as exc:
        log.error(">>> [Polymarket] ❌ EXECUTION FAILED  · %s: %s", type(exc).__name__, exc)
        raise


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  §3  HYPERLIQUID LEG — Client Init + Async Short
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _init_hyperliquid_exchange() -> tuple[Info, Exchange, str]:
    """Authenticate & return (info, exchange, address)."""
    account: LocalAccount = eth_account.Account.from_key(HYPERLIQUID_PRIVATE_KEY)
    address = HL_WALLET_ADDRESS if HL_WALLET_ADDRESS else account.address

    info = Info(HL_BASE_URL, skip_ws=True)
    exchange = Exchange(account, HL_BASE_URL, account_address=address)

    log.info(
        ">>> [Hyperliquid] Exchange initialised  · address=%s  url=%s",
        address[:10] + "…",
        HL_BASE_URL,
    )
    return info, exchange, address


def _hyperliquid_short_sync(exchange: Exchange) -> dict:
    """Synchronous Hyperliquid market-short — called inside asyncio.to_thread."""
    log.info(
        ">>> [Hyperliquid] Preparing SHORT  · coin=%s  size=%.6f  slippage=%.2f%%",
        HL_HEDGE_COIN,
        HL_SHORT_SIZE,
        HL_SLIPPAGE * 100,
    )

    # ── DRY-RUN GATE ──────────────────────────────────────
    if DRY_RUN:
        log.warning(
            "╔══════════════════════════════════════════════════════╗\n"
            "             ║  🏜️  DRY-RUN · Hyperliquid market_open INTERCEPTED  ║\n"
            "             ║  SIDE   = SHORT (is_buy=False)                      ║\n"
            "             ║  COIN   = %-10s                                   ║\n"
            "             ║  SIZE   = %-10.6f                                 ║\n"
            "             ║  SLIP   = %-6.2f%%                                  ║\n"
            "             ╚══════════════════════════════════════════════════════╝",
            HL_HEDGE_COIN,
            HL_SHORT_SIZE,
            HL_SLIPPAGE * 100,
        )
        return {
            "status": "ok",
            "dry_run": True,
            "tx_hash": "Tx_Hash_Mocked_Hyperliquid",
            "detail": {
                "side": "SHORT",
                "coin": HL_HEDGE_COIN,
                "size": HL_SHORT_SIZE,
                "slippage": HL_SLIPPAGE,
            },
        }
    # ── LIVE FIRE ─────────────────────────────────────────
    order_result = exchange.market_open(
        HL_HEDGE_COIN,
        is_buy=False,           # SHORT
        sz=HL_SHORT_SIZE,
        px=None,                # market order — SDK auto-prices
        slippage=HL_SLIPPAGE,
    )
    log.info(">>> [Hyperliquid] 🔥 Short Position OPENED  · result=%s", order_result)
    return order_result


async def execute_hyperliquid_short() -> dict:
    """Async wrapper — spins up exchange, fires short in a thread."""
    try:
        info, exchange, address = _init_hyperliquid_exchange()
        result = await asyncio.to_thread(_hyperliquid_short_sync, exchange)
        return result
    except Exception as exc:
        log.error(">>> [Hyperliquid] ❌ EXECUTION FAILED  · %s: %s", type(exc).__name__, exc)
        raise


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  §4  THE ROUTER — Cross-Chain Concurrent Controller
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def cross_chain_atomic_hedge() -> tuple[dict | Exception, dict | Exception]:
    """
    Fires both legs in parallel.
    Returns (poly_result, hl_result) — either dicts or Exception objects.
    """
    banner = (
        "\n"
        "╔══════════════════════════════════════════════════════════════╗\n"
        "║        LAPLACE VAULT — INITIATING CROSS-CHAIN HEDGE        ║\n"
        "║        mode = {mode:<10s}                                   ║\n"
        "║        ts   = {ts}                               ║\n"
        "╚══════════════════════════════════════════════════════════════╝"
    )
    log.info(
        banner.format(
            mode="DRY-RUN 🏜️" if DRY_RUN else "LIVE 🔥",
            ts=datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3],
        )
    )

    t0 = time.perf_counter()

    # — Concurrent execution via asyncio.gather —
    poly_result, hl_result = await asyncio.gather(
        execute_polymarket_buy(),
        execute_hyperliquid_short(),
        return_exceptions=True,
    )

    elapsed_ms = (time.perf_counter() - t0) * 1000

    # — Leg-break analysis —
    poly_ok = not isinstance(poly_result, Exception)
    hl_ok = not isinstance(hl_result, Exception)

    if poly_ok and hl_ok:
        log.info(
            ">>> [Router] ✅ BOTH LEGS EXECUTED SUCCESSFULLY  · Δt=%.1fms\n"
            "    Polymarket → %s\n"
            "    Hyperliquid → %s",
            elapsed_ms,
            poly_result.get("tx_hash", poly_result.get("status", "ok")),
            hl_result.get("tx_hash", hl_result.get("status", "ok")),
        )
    else:
        log.critical(
            "╔══════════════════════════════════════════════════════════════╗\n"
            "             ║  🚨🚨🚨  LEG-BREAK DETECTED — RISK ALERT  🚨🚨🚨       ║\n"
            "             ╠══════════════════════════════════════════════════════════════╣\n"
            "             ║  Polymarket leg : %-42s ║\n"
            "             ║  Hyperliquid leg: %-42s ║\n"
            "             ╠══════════════════════════════════════════════════════════════╣\n"
            "             ║  ACTION REQUIRED: Manually unwind the surviving leg to      ║\n"
            "             ║  avoid naked directional exposure.                          ║\n"
            "             ╚══════════════════════════════════════════════════════════════╝",
            "OK" if poly_ok else f"FAILED ({poly_result})",
            "OK" if hl_ok else f"FAILED ({hl_result})",
        )

    return poly_result, hl_result


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  §5  ENTRYPOINT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main() -> None:
    log.info("Laplace Vault engine starting  · DRY_RUN=%s  · Python %s", DRY_RUN, sys.version.split()[0])
    asyncio.run(cross_chain_atomic_hedge())
    log.info("Laplace Vault engine shutdown.")


if __name__ == "__main__":
    main()
