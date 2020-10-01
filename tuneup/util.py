
import decimal



def dilate(u,scale):
    if isinstance(u,list):
        return [u_*scale for u_ in u]
    else:
        return u*scale


def chop(x):
    d = decimal.Decimal(x)
    return str(d.quantize(decimal.Decimal(".1"), decimal.ROUND_DOWN))

def escape_bs_and_ff(s):
    return s.replace("\b", "\\b").replace("\f", "\\f")