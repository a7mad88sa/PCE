from dataclasses import dataclass

@dataclass
class TaylorParams:
    r_star: float = 0.5
    pi_star: float = 2.0
    u_star: float = 4.2

def taylor_rate(pi: float, u: float, params: TaylorParams | None = None) -> float:
    """حساب معدل تايلور مبسط.

    الصيغة: r = r_star + pi + 0.5*(pi - pi_star) + 0.5*(u_star - u)
    """
    if params is None:
        params = TaylorParams()
    return params.r_star + pi + 0.5 * (pi - params.pi_star) + 0.5 * (params.u_star - u)

def rate_fan(*args, **kwargs):
    # placeholder for tests
    return taylor_rate(*args, **kwargs)

def rate_neutral(*args, **kwargs):
    # placeholder for tests
    return taylor_rate(*args, **kwargs)
