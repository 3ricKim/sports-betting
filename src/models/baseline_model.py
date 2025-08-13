#used as benchmark
def american_to_probability(odds):
    if odds < 0:
        return -odds / (-odds + 100)
    else:
        return 100 / (odds + 100)

def de_vig(p_over, p_under):
    return p_over / (p_over + p_under), p_under / (p_over + p_under)

# american odds to payout
def calculate_payout(odds):
    if odds > 0:
        return 1 + odds / 100
    else:
        return 1 + 100 / (-odds)

def calculate_ev(fair_odds, odds):
    p = american_to_probability(fair_odds)
    m = calculate_payout(odds)
    return p * (m - 1) - (1 - p)

print(calculate_ev(133, 129))
