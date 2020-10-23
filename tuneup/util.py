
import decimal



def dilate(u,scale):
    if isinstance(u,list):
        return [u_*scale for u_ in u]
    else:
        return u*scale


def chop(x):
    d = decimal.Decimal(x)
    if x>100:
        return str(round(x))
    else:
        return str(d.quantize(decimal.Decimal(".1"), decimal.ROUND_DOWN))

def escape_bs_and_ff(s):
    return s.replace("\b", "\\b").replace("\f", "\\f")


def solver_name(solver):
    return solver.__name__.replace('_cube','').replace('_skew',' (skew) ').replace('_scaled',' (scaled) ')


def comma_and(l:list):
    """ blah, blah and blah """
    return ', '.join([str(itm) for itm in l[:-1]])+' and '+str(l[-1]) if len(l)>=2 else str(l[0])