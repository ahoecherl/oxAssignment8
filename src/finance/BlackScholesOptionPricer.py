import math
from scipy.stats import norm

parameterCount = 5

def BSPrice(St, sigma, K, tau, r, isCall):
    omega = 1 if isCall else -1
    sigmahat = sigma*math.sqrt(tau)
    d1 = 1/sigmahat*(math.log(St/K)+(r+sigma**2/2)*tau)
    d2 = d1-sigmahat
    n1 = norm.cdf(omega*d1)
    n2 = norm.cdf(omega*d2)
    rhat = math.exp(-r*tau)
    price = omega*(n1*St - n2*K*rhat)
    return price

def BSPrice_Analytical(St, sigma, K, tau, r, isCall):
    omega = 1 if isCall else -1
    sigmahat = sigma * math.sqrt(tau)
    d1 = 1 / sigmahat * (math.log(St / K) + (r + sigma ** 2 / 2) * tau)
    d2 = d1 - sigmahat
    n1 = norm.cdf(omega * d1)
    n2 = norm.cdf(omega * d2)
    rhat = math.exp(-r * tau)
    price = omega * (n1 * St - n2 * K * rhat)

    derivatives = [0] * parameterCount
    if isCall:
        derivatives[0] = n1
        derivatives[1] = St*norm.pdf(d1)*math.sqrt(tau)
        derivatives[3] = -St*norm.pdf(d1)*sigma/(2*math.sqrt(tau))-r*K*math.exp(-r*tau)*n2
        derivatives[4] = K*tau*math.exp(-r*tau)*n2

    else:
        derivatives[0] = -n1
        derivatives[1] = St*norm.pdf(d1)*math.sqrt(tau)
        derivatives[3] = -St*norm.pdf(d1)*sigma/(2*math.sqrt(tau))+r*K*math.exp(-r*tau)*n2
        derivatives[4] = -K*tau*math.exp(-r*tau)*n2

    return {'price': price, 'derivatives': derivatives}

def BSPrice_SAD(St, sigma, K, tau, r, isCall):
    omega = 1 if isCall else -1
    sigmahat = sigma*math.sqrt(tau)
    d1 = 1/sigmahat*(math.log(St/K)+(r+sigma**2/2)*tau)
    d2 = d1-sigmahat
    n1 = norm.cdf(omega*d1)
    n2 = norm.cdf(omega*d2)
    rhat = math.exp(-r*tau)
    price = omega*(n1*St - n2*K*rhat)

    sigmahatdot = [0]*parameterCount
    sigmahatdot[1] += math.sqrt(tau)
    sigmahatdot[3] += 1/2 * sigma / math.sqrt(tau)

    d1dot = [0]*parameterCount
    for i in range(0, parameterCount):
        d1dot[i] += (-1/sigmahat**2 * (math.log(St/K) + (r+sigma**2)*tau)) * sigmahatdot[i]
    d1dot[0] += 1/(St*sigmahat)
    d1dot[1] += 1/sigmahat*sigma*tau
    d1dot[2] += -1 / (K*sigmahat)
    d1dot[3] += sigma**2/sigmahat
    d1dot[4] += tau/sigmahat

    d2dot = [0]*parameterCount
    for i in range(0, parameterCount):
        d2dot[i] += -1 * sigmahatdot[i]
    for i in range(0, parameterCount):
        d2dot[i] += 1 * d1dot[i]

    n1dot = [0]*parameterCount
    for i in range(0, parameterCount):
        n1dot[i] += omega*norm.pdf(omega*d1) * d1dot[i]

    n2dot = [0]*parameterCount
    for i in range(0, parameterCount):
        n2dot[i] += omega*norm.pdf(omega*d2) * d2dot[i]

    rhatdot = [0]*parameterCount
    rhatdot[3] += -r * rhat
    rhatdot[4] += -tau * rhat

    pricedot = [0]*parameterCount
    for i in range(0, parameterCount):
        pricedot[i] += omega*St * n1dot[i]
    for i in range(0, parameterCount):
        pricedot[i] += -omega*K*rhat * n2dot[i]
    for i in range(0, parameterCount):
        pricedot[i] += -omega*n2*K * rhatdot[i]
    pricedot[0] += omega*n1
    pricedot[2] += -omega*n2*rhat

    return {'price': price, 'derivatives': pricedot}
#Assignment count for derivative calculation: 57

def BSPrice_AAD(St, sigma, K, tau, r, isCall):
    omega = 1 if isCall else -1
    sigmahat = sigma * math.sqrt(tau)
    d1 = 1 / sigmahat * (math.log(St / K) + (r + sigma ** 2 / 2) * tau)
    d2 = d1 - sigmahat
    n1 = norm.cdf(omega * d1)
    n2 = norm.cdf(omega * d2)
    rhat = math.exp(-r * tau)
    price = omega * (n1 * St - n2 * K * rhat)

    Pbar = 1

    rhatbar = -n2*K*omega * Pbar

    n2bar = -K*rhat*omega * Pbar

    n1bar = omega*St * Pbar

    d2bar = norm.pdf(omega*d2)*omega * n2bar

    d1bar = norm.pdf(omega*d1)*omega * n1bar
    d1bar += 1 * d2bar

    sigmahatbar = -1 *d2bar
    sigmahatbar += -1/(sigmahat**2)*(math.log(St/K)+(r+(sigma**2)/2)*tau) * d1bar

    rbar = -tau*rhat * rhatbar
    rbar += sigmahat*tau * d1bar

    taubar = -r*rhat * rhatbar
    taubar += (1/sigmahat*r + sigma**2/(sigmahat*2)) * d1bar
    taubar += 1/2*sigma/math.sqrt(tau) * sigmahatbar

    Kbar = -omega*n2*rhat * Pbar
    Kbar += -1/(sigmahat*K) * d1bar

    sigmabar = sigmahat*sigma*tau * d1bar
    sigmabar += math.sqrt(tau) * sigmahatbar

    Stbar = omega*n1 * Pbar
    Stbar += 1/(sigmahat*St) * d1bar

    derivatives = [Stbar, sigmabar, Kbar, taubar, rbar]

    return {'price': price, 'derivatives': derivatives}
#Assignment count for derivative calculation: 20

def BSPrice_AAAD(St, sigma, K, tau, r, isCall):
    omega = 1 if isCall else -1
    sigmahat = sigma*tau.sqrt()
    d1 = 1/sigmahat*((St/K).log()+(r+sigma**2/2)*tau)
    d2 = d1-sigmahat
    n1 = (omega*d1).normalcdf()
    n2 = (omega*d2).normalcdf()
    rhat = (-r*tau).exp()
    price = omega*(n1*St - n2*K*rhat)
    return price