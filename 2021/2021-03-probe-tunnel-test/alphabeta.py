import scipy.optimize
import math

def alpha_beta_to_az_el(alpha_beta):
    '''
    Given an alpha/beta probe on an altazimuth mount, the alpha/beta
    angles and the altazimuth angles (u, v) are approximately
    equal, but not exactly so. We define:
        a = alpha or angle of attack
        b = beta or angle of yaw
        u = azim*u*th
        v = ele*v*ation
    This function takes the desired values of (a, b), and returns a tuple
    (u, v) of the az-el angles to which the mount should be slewed to achieve
    them.
    '''

    alpha_beta_radians = [
        math.fabs(math.radians(alpha_beta[0])),
        math.fabs(math.radians(alpha_beta[1])),
    ]
    
    # The math works out such that, for the expected ranges, the
    # altitude angle 'v' is equal to the angle of attack, alpha
    v = alpha_beta_radians[0]

    # Next, we define the function that computes beta given (u, v),
    # where 'v' is already known.
    beta = lambda u: math.acos((math.cos(u) * math.cos(v)) / math.sqrt(1 + math.cos(u) ** 2 * (math.cos(v) ** 2 - 1)))

    # We now use root-finding to determine the azimuth angle 'u' that
    # gives us the value of beta that we want.
    results = scipy.optimize.root_scalar(
        lambda u: beta(u) - alpha_beta_radians[1],
        x0 = alpha_beta_radians[1],
        x1 = alpha_beta_radians[1] + 0.1)
    if not results.converged: raise 'Not converged: %s' % results
    return [
        math.copysign(math.degrees(results.root), alpha_beta[1]),
        math.copysign(math.degrees(v), alpha_beta[0]),
    ]
