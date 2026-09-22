import re

def parse_signal(text):
    text = text.upper()
    coin_match = re.search(r'\b([A-Z0-9]{2,10}USDT)\b', text)
    if not coin_match:
        return None
    symbol = coin_match.group(1)
    
    direction = None
    if 'LONG' in text:
        direction = 'LONG'
    elif 'SHORT' in text:
        direction = 'SHORT'
    if not direction:
        return None
    
    leverage_match = re.search(r'(?:X|ПЛЕЧО[^\d]*)\s*(\d{1,3})', text)
    leverage = int(leverage_match.group(1)) if leverage_match else 10
    
    entry_match = re.search(r'ВХОД[^\d]*([\d.]+)', text)
    entry = float(entry_match.group(1)) if entry_match else None
    
    stop_match = re.search(r'СТОП[^\d]*([\d.]+)', text)
    stop = float(stop_match.group(1)) if stop_match else None
    
    targets = []
    goals_match = re.search(r'ЦЕЛИ[^\d]*((?:[\d.]+,?\s*)+)', text)
    if goals_match:
        target_str = goals_match.group(1)
        targets = [float(t) for t in re.findall(r'[\d.]+', target_str)]
    
    return {
        'symbol': symbol,
        'direction': direction,
        'leverage': leverage,
        'entry': entry,
        'stop': stop,
        'targets': targets
    }

if __name__ == '__main__':
    test_signal = """
    APTUSDT
    Направление - LONG
    ІСО Плечо - Х40
    Вход по рынку - 0.7690
    Наши цели - 0.7815,
    0.7930, 0.8046, ,0.8200
    Стоп - 0.7185
    """
    result = parse_signal(test_signal)
    print(result)