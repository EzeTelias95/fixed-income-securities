import math

def newton_raphson_cont(price_obs, cf_df, y0=0.08, tol=1e-10, maxit=100):
    """
        cf_df: DataFrame with columns ['Tau', 'Payment'] of future cashflows.
    """
    y = y0
    for _ in range(maxit):
        disc = cf_df['Tau'].rsub(0).mul(y).apply(math.exp)  # e^{-y * Tau}
        # f(y) = PV - P
        f  = (cf_df['Payment'] * disc).sum() - price_obs
        # f'(y) = -sum(Tau * CF * e^{-y*Tau})
        fp = -(cf_df['Tau'] * cf_df['Payment'] * disc).sum()
        step = f / fp
        y_new = y - step
        if abs(step) < tol:
            return y_new
        y = y_new
    raise RuntimeError("Newton does not converge (Tau-cont)")

def newton_raphson_disc(price_obs, cf_df, y0=0.08, tol=1e-10, maxit=100):
    """
    P(y) = sum( CF / (1+y)^{Tau} ), f'(y) = -sum( Tau * CF / (1+y)^{Tau+1} )
    """
    y = y0
    for _ in range(maxit):
        den = (1 + y)
        f  = (cf_df['Payment'] / (den ** cf_df['Tau'])).sum() - price_obs
        fp = - ( (cf_df['Tau'] * cf_df['Payment']) / (den ** (cf_df['Tau'] + 1)) ).sum()
        step = f / fp
        y_new = y - step
        if abs(step) < tol:
            return y_new
        y = y_new
    raise RuntimeError("Newton does not converge (Tau-disc)")