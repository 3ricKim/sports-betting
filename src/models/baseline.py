#used as benchmark
def american_to_decimal(odd):
    if odd < 0:
        return -odd / (-odd + 100)
    else:
        return 100 / (odd + 100)

def de_vig(p_over, p_under):
    return p_over / (p_over + p_under), p_under / (p_over + p_under)


print(american_to_decimal(-120))