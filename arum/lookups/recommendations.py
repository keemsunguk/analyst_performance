"""
Strong BUY
Trading BUY, BUY, 매수, Outperform
보유, HOLD, 중립, Marketperform, Neutral
없음,NR
비중축소/REDUCE
Underperform/Sell
"""


recommendation_lookup = {
    'STRONG BUY': 'STRONG_BUY',
    'Strong Buy': 'STRONG_BUY',
    'Trading Buy': 'BUY',
    'BUY': 'BUY',
    '매수': 'BUY',
    'Outperform': 'BUY',
    '보유': 'HOLD',
    'NEUTRAL': 'HOLD',
    'HOLD': 'HOLD',
    '중립': 'HOLD',
    'MarketPerform': 'HOLD',
    'Neutral': 'HOLD',
    '없음': 'NR',
    'NR': 'NR',
    '비중축소': 'REDUCE',
    'REDUCE': 'REDUCE',
    'Underperform': 'SELL',
    'Sell': 'SELL',
}

