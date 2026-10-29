# agno-optimistfi

[OptimistFi](https://optimistfi.com) data as tools for [Agno](https://github.com/agno-agi/agno) agents: perpetual futures across venues, prop firms that fund crypto and stock perps traders, and US company disclosures from SEC EDGAR and the US House Clerk.

The tools call OptimistFi's public endpoint, `https://mcp.optimistfi.com/mcp`. No API key is needed.

## Install

```bash
pip install agno-optimistfi
```

It needs Python 3.9 or later and Agno 2.3.23 or later.

## Quick start

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from agno_optimistfi import OptimistFiTools

agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[OptimistFiTools()],
    instructions=["Name the source and the date of each figure you quote."],
    markdown=True,
)

agent.print_response("Which House members traded NVDA this year, and have its insiders been selling?")
```

Any model Agno supports can drive the tools. A runnable version is in [`examples/research_agent.py`](examples/research_agent.py).

## Tools

| Tool | What it returns |
|---|---|
| `get_perp` | One perpetual futures market across venues now: price and premium to the index or stock, open interest, funding, maximum leverage, liquidation levels, large trades and positioning. Crypto, stock, index and commodity perps. |
| `get_perp_history` | One market over 1, 7, 30 or 90 days: price, open interest, funding, taker buying against selling, the net position of large accounts, and the latest order book depth. |
| `get_perps_market` | One view across markets and venues, such as funding, open interest, liquidations, liquidation levels, large-account lean, new listings, ETF flows, options and basis. 20 views. |
| `get_prop_firms` | Prop firms that fund crypto and stock perps traders, read from the firms' own pages: rules, challenge prices, live discount codes, country, platforms, assets and maximum allocation. |
| `get_insider_trades` | A US company's Form 4 filings from SEC EDGAR: who, role, what they did, shares and dollar value, with the trade date and the date it became public. |
| `get_congress_trades` | US House stock disclosures under the STOCK Act, by ticker or by member, with the account each trade was made in, linked to the filing. |
| `get_company_filings` | A company's 8-K events, earnings press releases, the text of its latest 8-Ks, or governance red flags such as late filings, auditor changes and clusters of insider selling. |
| `get_company_calendar` | What is ahead for a company: the next earnings date projected from its own filing cadence, labeled as an estimate with its basis, then clinical trial readouts from ClinicalTrials.gov, nearest first. |

Every tool has an async twin (`aget_perp`, `aget_insider_trades` and so on), which Agno uses when the agent runs with `arun`.

## Choosing tools

All eight are registered by default. Turn any off to keep a small model's tool list short:

```python
# US company disclosures only
OptimistFiTools(
    enable_get_perp=False,
    enable_get_perp_history=False,
    enable_get_perps_market=False,
    enable_get_prop_firms=False,
)
```

`timeout` (seconds, default 60) and `base_url` are also settable.

## What a tool returns

Each tool returns JSON. Records share one shape:

```json
{
  "entity": {"ticker": "NVDA", "name": "NVIDIA CORP", "cik": "0001045810"},
  "type": "gov_trade",
  "event_time": "2026-10-01",
  "as_of": "2026-10-22",
  "confidence": "confirmed",
  "source": {"name": "US House Clerk PTR", "url": "https://disclosures-clerk.house.gov/...", "license": "public"},
  "data": {"politician": "Cleo Fields", "txn_type": "buy", "amount_low": 1001, "amount_high": 15000, "account": "Morgan Stanley - E*TRADE IRA"}
}
```

- `event_time` is when the event happened or is expected.
- `as_of` is when it became public, or for a projected date or a trial readout, when its source was last read.
- `confidence` is `confirmed` for a filed fact and `estimated` for a projected date, such as a next earnings date, which also carries its basis.
- `source.url` links to the filing or page the record was read from.

A failed request returns `{"error": ...}` with the reason. When the server is restarting (HTTP 502, 503 or 504), the call is retried once after 5 seconds.

## Data and limits

- **Sources:** SEC EDGAR (Form 4, 8-K), the US House Clerk (periodic transaction reports), ClinicalTrials.gov, the prop firms' own pages, and exchange data across perps venues.
- **Coverage:** the House only for congressional trades; US-listed companies for SEC data.
- **Not advice:** the data is for research. It is not investment advice, and nothing here places an order.

## Development

```bash
pip install -e ".[test]"
pytest
```

The tests mock the endpoint, so they run offline.

## License

MIT. See [LICENSE](LICENSE).
