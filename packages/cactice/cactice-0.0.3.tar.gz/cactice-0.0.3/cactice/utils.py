

def unit_scale(d):
    values = d.values()
    mn = min(values)
    mx = max(values)
    return {k: ((v - mn) / (mx - mn)) for (k, v) in d.items()}
