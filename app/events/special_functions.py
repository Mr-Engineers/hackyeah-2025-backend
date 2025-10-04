import json, csv, io
import math, random


def to_str_list(val):
    if val is None: 
        return []
    if isinstance(val, list):
        return [str(x) for x in val]
    if isinstance(val, str):
        v = val.strip()
        if not v:
            return []
        # JSON lista?
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                return [str(x) for x in parsed]
        except Exception:
            pass
        # Literał Postgresa: {a,b}
        if v.startswith('{') and v.endswith('}'):
            inside = v[1:-1]
            tokens = next(csv.reader(io.StringIO(inside)))
            return [t.strip().strip('"') for t in tokens if t.strip().strip('"')]
        # Zwykły CSV: "a, b"
        return [x.strip() for x in v.split(',') if x.strip()]
    # cokolwiek innego
    return [str(val)]


def to_num_list(val):
    if val is None:
        return []
    if isinstance(val, list):
        return [float(x) for x in val]
    if isinstance(val, str):
        v = val.strip()
        if not v:
            return []
        # JSON lista liczb?
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                return [float(x) for x in parsed]
        except Exception:
            pass
        # Literał Postgresa: {10,20.5}
        if v.startswith('{') and v.endswith('}'):
            inside = v[1:-1]
            tokens = next(csv.reader(io.StringIO(inside)))
            return [float(t.strip()) for t in tokens if t.strip()]
        # Zwykły CSV: "10, 20.5"
        return [float(x.strip()) for x in v.split(',') if x.strip()]
    # cokolwiek innego (pojedyncza liczba)
    return [float(val)]


def should_trigger(x: float, max_x: float) -> bool:
    """
    Zwraca True z prawdopodobieństwem zgodnym z rozkładem normalnym,
    gdzie x=0 -> 100%, a x=max_x -> 0%.
    """
    # Ustal środek i odchylenie standardowe proporcjonalnie do max_x
    mean = max_x / 2
    std_dev = max_x / 4  # reguluj stromość (1/4 dobrze działa w zakresie 0–30)
    
    # Dystrybuanta rozkładu normalnego (CDF)
    cdf = 0.5 * (1 + math.erf((x - mean) / (std_dev * math.sqrt(2))))
    
    # Odwrócenie (x=0 → 1, x=max_x → 0)
    probability_true = 1 - cdf

    # Ograniczenie do przedziału [0, 1]
    probability_true = max(0.0, min(1.0, probability_true))

    # Losowanie wyniku
    return random.random() < probability_true