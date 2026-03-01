# Indicator catalog for FRED Dashboard V2
# Add / edit series here only; ingestion/UI should auto-adapt.
#
# Fields:
# - domain: simple domain name
# - tier: S / A / B (importance)
# - id: FRED series id
# - name: short display name
# - intent: what this series is meant to capture
# - frequency_hint: daily|weekly|monthly|quarterly (used for scheduling)
# - history_years: int or "all"
# - transforms: list of derived metrics to compute (lin, yoy, mom, diff, zscore, spread_to:<id>, ratio_to:<id>)
# - chart: preferred default visualization
# - notes: caveats, units, interpretation
# - fallback_ids: list of alternative FRED ids if primary errors or discontinued
# - vintage: true if we should store realtime_start/realtime_end vintages (ALFRED-like), else store latest only

series:

  # -------------------------
  # Liquidity
  # -------------------------
  - domain: Liquidity
    tier: S
    id: WALCL
    name: Fed Total Assets
    intent: Core USD liquidity driver (QE/QT balance sheet size)
    frequency_hint: weekly
    history_years: all
    transforms: [lin, yoy, zscore]
    chart: line
    notes: "Key liquidity proxy; compare with risk assets and reserves."
    fallback_ids: []
    vintage: false

  - domain: Liquidity
    tier: S
    id: WRESBAL
    name: Reserve Balances
    intent: Immediate banking system liquidity (reserves)
    frequency_hint: weekly
    history_years: all
    transforms: [lin, yoy, zscore]
    chart: line
    notes: "Use with WALCL and RRP to understand liquidity plumbing."
    fallback_ids: []
    vintage: false

  - domain: Liquidity
    tier: A
    id: RRPONTSYD
    name: ON RRP
    intent: Liquidity absorption via Fed overnight reverse repo
    frequency_hint: daily
    history_years: 10
    transforms: [lin, yoy]
    chart: line
    notes: "RRP drawdown often correlates with risk-on phases."
    fallback_ids: []
    vintage: false

  - domain: Liquidity
    tier: A
    id: M2SL
    name: M2 Money Stock
    intent: Broad money growth (longer-horizon inflation/liquidity context)
    frequency_hint: weekly
    history_years: all
    transforms: [lin, yoy]
    chart: line
    notes: "Use YoY; structural breaks exist."
    fallback_ids: []
    vintage: false

  # -------------------------
  # Financial Stress
  # -------------------------
  - domain: Stress
    tier: S
    id: NFCI
    name: Chicago Fed NFCI
    intent: Aggregate financial conditions / stress
    frequency_hint: weekly
    history_years: all
    transforms: [lin, zscore]
    chart: line_zero
    notes: "0 is a useful reference; rising indicates tightening."
    fallback_ids: [ANFCI]
    vintage: false

  - domain: Stress
    tier: A
    id: SOFR
    name: SOFR
    intent: Core secured funding rate (money market conditions)
    frequency_hint: daily
    history_years: 10
    transforms: [lin, diff]
    chart: line
    notes: "Pair with policy rate and spreads for funding stress."
    fallback_ids: []
    vintage: false

  # -------------------------
  # Rates & Expectations
  # -------------------------
  - domain: Rates
    tier: S
    id: DFII10
    name: 10Y TIPS Real Yield
    intent: Real-rate tightening; key equity discount rate driver
    frequency_hint: daily
    history_years: 20
    transforms: [lin, diff, zscore]
    chart: line
    notes: "Strong inverse link with long-duration assets."
    fallback_ids: []
    vintage: false

  - domain: Rates
    tier: S
    id: T5YIFR
    name: 5Y5Y Inflation Expectation
    intent: Long-run inflation expectations proxy
    frequency_hint: daily
    history_years: 20
    transforms: [lin, diff]
    chart: line
    notes: "Market-based; interpret with term premium and breakevens."
    fallback_ids: []
    vintage: false

  - domain: Rates
    tier: A
    id: ACMTP10
    name: 10Y Term Premium (ACM)
    intent: Decompose long rates into expectations vs risk premium
    frequency_hint: daily
    history_years: 20
    transforms: [lin, diff]
    chart: line_zero
    notes: "Term premium spikes often coincide with risk-off."
    fallback_ids: []
    vintage: false

  # -------------------------
  # Yield Curve
  # -------------------------
  - domain: Curve
    tier: S
    id: T10Y2Y
    name: 10Y-2Y Spread
    intent: Cycle / policy stance indicator; recession signal component
    frequency_hint: daily
    history_years: 40
    transforms: [lin, zscore]
    chart: line_zero
    notes: "Use zero line; inversion is key."
    fallback_ids: []
    vintage: false

  - domain: Curve
    tier: S
    id: T10Y3M
    name: 10Y-3M Spread
    intent: Stronger recession-signal variant (near-term vs long)
    frequency_hint: daily
    history_years: 40
    transforms: [lin, zscore]
    chart: line_zero
    notes: "Frequently used in academic recession probability models."
    fallback_ids: []
    vintage: false

  # -------------------------
  # Credit
  # -------------------------
  - domain: Credit
    tier: S
    id: BAMLH0A0HYM2
    name: HY OAS
    intent: Risk appetite / default risk proxy
    frequency_hint: daily
    history_years: 30
    transforms: [lin, zscore]
    chart: line
    notes: "One of the best risk-off indicators."
    fallback_ids: []
    vintage: false

  - domain: Credit
    tier: A
    id: BAA10YM
    name: Baa-10Y Spread
    intent: Investment-grade credit risk premium proxy
    frequency_hint: daily
    history_years: 40
    transforms: [lin, zscore]
    chart: line
    notes: "Use spread rather than level; confirm with HY."
    fallback_ids: [BAA10Y]
    vintage: false

  - domain: Credit
    tier: A
    id: DRTSCILM
    name: SLOOS - C&I Lending Standards (Tightening)
    intent: Bank credit supply tightening; forward-looking for growth
    frequency_hint: quarterly
    history_years: 30
    transforms: [lin, zscore]
    chart: line_zero
    notes: "Higher implies tighter standards."
    fallback_ids: []
    vintage: false

  # -------------------------
  # USD (Global) Liquidity
  # -------------------------
  - domain: USD
    tier: S
    id: DTWEXBGS
    name: Broad Trade-Weighted Dollar
    intent: Global USD tightening/loosening; EM and commodities sensitivity
    frequency_hint: daily
    history_years: 30
    transforms: [lin, yoy]
    chart: line
    notes: "Strong macro cross-asset driver."
    fallback_ids: []
    vintage: false

  - domain: USD
    tier: A
    id: SWPWL
    name: Central Bank Liquidity Swaps (Outstanding)
    intent: Dollar swap line usage; stress in global USD funding
    frequency_hint: weekly
    history_years: 20
    transforms: [lin]
    chart: line
    notes: "Spikes indicate global USD funding strain."
    fallback_ids: []
    vintage: false

  # -------------------------
  # Flows & Leverage (Z.1 / Flow of Funds)
  # -------------------------
  - domain: Flows
    tier: S
    id: FGTCMDODNS
    name: Foreign Holdings of UST (TIC / custody proxy)
    intent: External demand for UST; FX-reserve behavior proxy
    frequency_hint: weekly
    history_years: all
    transforms: [lin, yoy]
    chart: line
    notes: "Interpret alongside USD and term premium."
    fallback_ids: []
    vintage: false

  - domain: Flows
    tier: A
    id: TOTBKCR
    name: Commercial Bank Credit
    intent: Credit creation / lending impulse proxy
    frequency_hint: weekly
    history_years: all
    transforms: [lin, yoy]
    chart: line
    notes: "YoY deceleration can foreshadow slowdown."
    fallback_ids: []
    vintage: false

  - domain: Flows
    tier: A
    id: BOGZ1FL663067003Q
    name: Margin Debt (Z.1)
    intent: Equity leverage / speculative positioning proxy
    frequency_hint: quarterly
    history_years: all
    transforms: [lin, yoy]
    chart: line
    notes: "Use with equity proxies; beware revisions."
    fallback_ids: []
    vintage: false

  # -------------------------
  # Labor Market
  # -------------------------
  - domain: Labor
    tier: S
    id: PAYEMS
    name: Nonfarm Payrolls
    intent: Employment growth; core cycle gauge
    frequency_hint: monthly
    history_years: 40
    transforms: [lin, mom, yoy]
    chart: line_bar_combo
    notes: "Show level + MoM change bar."
    fallback_ids: []
    vintage: true

  - domain: Labor
    tier: S
    id: UNRATE
    name: Unemployment Rate (U-3)
    intent: Labor slack; recession confirmation
    frequency_hint: monthly
    history_years: 60
    transforms: [lin, diff]
    chart: line
    notes: "Consider Sahm-like signals in composites."
    fallback_ids: []
    vintage: true

  - domain: Labor
    tier: A
    id: JTSJOL
    name: JOLTS Job Openings
    intent: Labor demand; wage pressure driver
    frequency_hint: monthly
    history_years: 25
    transforms: [lin, yoy]
    chart: line
    notes: "Pair with UNRATE for Beveridge curve."
    fallback_ids: []
    vintage: true

  - domain: Labor
    tier: A
    id: CIVPART
    name: Labor Force Participation
    intent: Labor supply; structural wage pressure component
    frequency_hint: monthly
    history_years: 60
    transforms: [lin, diff]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: true

  - domain: Labor
    tier: S
    id: CES0500000003
    name: Avg Hourly Earnings
    intent: Wage inflation; inflation driver
    frequency_hint: monthly
    history_years: 40
    transforms: [lin, yoy]
    chart: line
    notes: "Use YoY; compare with core inflation."
    fallback_ids: []
    vintage: true

  - domain: Labor
    tier: A
    id: ICSA
    name: Initial Jobless Claims
    intent: High-frequency labor deterioration signal
    frequency_hint: weekly
    history_years: 40
    transforms: [lin, zscore]
    chart: line
    notes: "Consider 4-week moving average in UI."
    fallback_ids: []
    vintage: false

  # -------------------------
  # Inflation (headline + core + sticky)
  # -------------------------
  - domain: Inflation
    tier: S
    id: PCEPILFE
    name: Core PCE Price Index
    intent: Fed’s preferred core inflation gauge
    frequency_hint: monthly
    history_years: 40
    transforms: [lin, yoy, mom]
    chart: line
    notes: "Show YoY + annualized 3m/6m in UI."
    fallback_ids: []
    vintage: true

  - domain: Inflation
    tier: A
    id: CPIAUCSL
    name: CPI (All Items)
    intent: Headline inflation; consumer-facing measure
    frequency_hint: monthly
    history_years: 60
    transforms: [lin, yoy, mom]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: true

  - domain: Inflation
    tier: A
    id: CPILFESL
    name: Core CPI
    intent: Underlying inflation excluding food/energy
    frequency_hint: monthly
    history_years: 60
    transforms: [lin, yoy, mom]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: true

  - domain: Inflation
    tier: A
    id: CORESTICKM159SFRBATL
    name: Sticky CPI (Atlanta Fed)
    intent: Persistence of inflation (stickiness)
    frequency_hint: monthly
    history_years: 40
    transforms: [lin, yoy]
    chart: line
    notes: "Good for inflation persistence regime."
    fallback_ids: []
    vintage: false

  # -------------------------
  # Consumption
  # -------------------------
  - domain: Consumption
    tier: S
    id: RSAFS
    name: Retail Sales (Advance)
    intent: High-impact demand pulse
    frequency_hint: monthly
    history_years: 40
    transforms: [lin, mom, yoy]
    chart: line_bar_combo
    notes: "Show MoM bar + YoY line."
    fallback_ids: []
    vintage: true

  - domain: Consumption
    tier: A
    id: PCEC96
    name: Real PCE
    intent: Real consumption volume (GDP core)
    frequency_hint: monthly
    history_years: 60
    transforms: [lin, yoy]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: true

  - domain: Consumption
    tier: A
    id: DSPIC96
    name: Real Disposable Personal Income
    intent: Consumer capacity / income support
    frequency_hint: monthly
    history_years: 60
    transforms: [lin, yoy]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: true

  # -------------------------
  # Business Activity
  # -------------------------
  - domain: Business
    tier: S
    id: INDPRO
    name: Industrial Production
    intent: Real activity; cycle confirmation
    frequency_hint: monthly
    history_years: 60
    transforms: [lin, yoy]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: true

  - domain: Business
    tier: S
    id: NAPM
    name: ISM Manufacturing PMI
    intent: Key forward-looking survey
    frequency_hint: monthly
    history_years: 40
    transforms: [lin]
    chart: line_50
    notes: "Do NOT delete if temporary errors. Implement retry + validate."
    fallback_ids: []
    vintage: false

  - domain: Business
    tier: S
    id: NAPMNOI
    name: ISM Services PMI (Business Activity / NMI)
    intent: Services activity; dominant in US economy
    frequency_hint: monthly
    history_years: 40
    transforms: [lin]
    chart: line_50
    notes: "If API quirks occur, keep as primary and add robust ingestion."
    fallback_ids: []
    vintage: false

  # -------------------------
  # Housing
  # -------------------------
  - domain: Housing
    tier: S
    id: HOUST
    name: Housing Starts
    intent: Highly cyclical leading indicator
    frequency_hint: monthly
    history_years: 60
    transforms: [lin, yoy]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: true

  - domain: Housing
    tier: A
    id: PERMIT
    name: Building Permits
    intent: Starts lead; forward-looking pipeline
    frequency_hint: monthly
    history_years: 60
    transforms: [lin, yoy]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: true

  - domain: Housing
    tier: A
    id: CSUSHPISA
    name: Case-Shiller Home Price Index
    intent: Home price inflation; wealth effects
    frequency_hint: monthly
    history_years: 40
    transforms: [lin, yoy]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: true

  - domain: Housing
    tier: A
    id: MORTGAGE30US
    name: 30Y Mortgage Rate
    intent: Housing affordability / rate transmission
    frequency_hint: weekly
    history_years: 40
    transforms: [lin, diff]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: false

  # -------------------------
  # Fiscal
  # -------------------------
  - domain: Fiscal
    tier: A
    id: FYFSD
    name: Federal Surplus/Deficit
    intent: Fiscal impulse; issuance pressure context
    frequency_hint: monthly
    history_years: 40
    transforms: [lin, yoy]
    chart: line
    notes: "Pair with term premium & supply effects."
    fallback_ids: []
    vintage: true

  - domain: Fiscal
    tier: A
    id: GFDEBTN
    name: Federal Debt Total Public Debt
    intent: Debt stock; longer-horizon supply/credibility context
    frequency_hint: quarterly
    history_years: all
    transforms: [lin, yoy]
    chart: line
    notes: ""
    fallback_ids: []
    vintage: false

  # -------------------------
  # Market Internals
  # -------------------------
  - domain: Markets
    tier: A
    id: VIXCLS
    name: VIX
    intent: Equity vol / risk aversion proxy
    frequency_hint: daily
    history_years: 30
    transforms: [lin, zscore]
    chart: line
    notes: "Use with credit spreads and NFCI."
    fallback_ids: []
    vintage: false


composites:
  # Composite definitions are computed server-side from series/derived values.
  # Each composite has: id, name, intent, inputs, method, chart.

  - id: RISK_REGIME
    name: Risk-On / Risk-Off Regime
    intent: Composite analysis (cross-asset risk appetite)
    inputs: [NFCI, BAMLH0A0HYM2, VIXCLS, ACMTP10]
    method: "zscore_mean(invert=[NFCI,BAMLH0A0HYM2,VIXCLS,ACMTP10?]) with sign conventions documented"
    chart: line_zero

  - id: RECESSION_RISK
    name: Recession Risk Composite
    intent: Composite analysis (cycle turning points)
    inputs: [T10Y3M, DRTSCILM, ICSA, UNRATE]
    method: "weighted_zscore + threshold bands"
    chart: heatmap_band

  - id: INFLATION_DRIVERS
    name: Inflation Drivers Panel
    intent: Composite analysis (drivers vs persistence)
    inputs: [PCEPILFE, CES0500000003, CORESTICKM159SFRBATL, T5YIFR]
    method: "multi-panel with yoy + rolling annualized rates"
    chart: multi_panel
