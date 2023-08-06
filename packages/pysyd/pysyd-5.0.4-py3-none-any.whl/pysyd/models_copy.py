import numpy as np


class Model:

    def __init__(self, x, y, y_err=None):
        self.xobs = np.copy(x)
        self.yobs = np.copy(y)
        if y_err is not None:
            self.yobs_err = np.copy(y_err)
        self.yexp = np.zeros_like(x)
        self.n_free = 0
        self.results = {}

    def setup(self, input, harvey_basis=['a b 2 vvf', 'tau sigma 2 vvf', 'pgran tau 2 vvf'])
        self.params={}
        self.params['harvey']={}
        self.params['harvey']['params'] = input.split(' ')[:2]
        self.types = {
                      'P':self.power_law,
                      'H':self.harvey_law,
                      'G':self.gaussian,
                      'L':self.lorentzian,
                      'W':self.white_noise,
                      }

    def build(self, types, compare=True):
        if len(types) == 1:
            compare=False
        self.compare = compare
        for type in types:
            self.type = type
            self.results[type] = {}
            self.yexp += 
        

    def reset(self):
        self.yexp = np.zeros_like(self.xobs)

    def add(self, types):
        pass

    def power_law(self, alpha, beta):
        return alpha*(self.xobs**beta)

    def harvey_law(self, tau, sigma, exponent, mode=):
        if self.harvey_basis == 'a b':
        elif self.harvey_basis == 'tau sigma':
        elif self.harvey_basis == 'pgran tau':
        else:
        pass

    def white_noise(self, noise):
        return noise

    def gaussian(self, offset, amplitude, center, width):
        return (offset + amplitude*np.exp(-(center-self.xobs)**2.0/(2.0*width**2)))

    def lorentzian(self):
        pass

    def log_likelihood(self):
        return -0.5*(np.sum((self.yobs-self.yexp)**2.))

    def compute_metrics(self, n_parameters):
        LL = self.log_likelihood()
        N = len(self.yobs)
        # BIC
        bic = -2.*LL + np.log(N)*n_parameters
        # AIC
        aic = (-2.*LL)/N + (2.*n_parameters)/N
        return bic, aic

    def __add__(self, other):
        total_visits = self.yexp + other.yexp
        return Day(total_visits, total_contacts)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)


class Harvey(Model):

class Gaussian(Model):

class Power(Model):

class Lorentzian(Model):

class White(Model):



def harvey(frequency, guesses, mode='regular', total=False, ab=False):
    """
    The main model for the stellar background fitting

    Parameters
    ----------
    frequency : numpy.ndarray
        the frequency of the power spectrum
    guesses : list
        the parameters of the Harvey model
    mode : {'regular', 'second', 'fourth'}
        the mode of which Harvey model parametrization to use. Default mode is `regular`.
        The 'regular' mode is when both the second and fourth order terms are added in the denominator
        whereas, 'second' only adds the second order term and 'fourth' only adds the fourth order term.
    total : bool
        If `True`, returns the summed model over multiple components.

    Returns
    -------
    model : np.ndarray
        the stellar background model

    """
    nlaws = int((len(guesses)-1)/2)
    model = np.zeros_like(frequency)

    if mode == 'regular':
        for i in range(nlaws):
            if not ab:
                model += (4.*(guesses[(i*2)+1]**2.)*guesses[i*2])/(1.0+(2.*np.pi*guesses[i*2]*frequency)**2.0+(2.*np.pi*guesses[i*2]*frequency)**4.0)
            else:
                model += guesses[i*2]/(1.0+(guesses[(i*2)+1]*frequency)**2.0+(guesses[(i*2)+1]*frequency)**4.0)
    elif mode == 'second':
        for i in range(nlaws):
            if not ab:
                model += (4.*(guesses[(i*2)+1]**2.)*guesses[i*2])/(1.0+(2.*np.pi*guesses[i*2]*frequency)**2.0)
            else:
                model += guesses[i*2]/(1.0+(guesses[(i*2)+1]*frequency)**2.0)
    elif mode == 'fourth':
        for i in range(nlaws):
            if not ab:
                model += (4.*(guesses[(i*2)+1]**2.)*guesses[i*2])/(1.0+(2.*np.pi*guesses[i*2]*frequency)**4.0)
            else:
                model += guesses[i*2]/(1.0+(guesses[(i*2)+1]*frequency)**4.0)
    else:
        pass

    if total:
        model += guesses[-1]

    return model


def gaussian(frequency, offset, amplitude, center, width):
    """
    The Gaussian function.

    Parameters
    ----------
    frequency : numpy.ndarray
        the frequency array
    offset : float
        the vertical offset
    amplitude : float
        amplitude of the Gaussian
    center : float
        center of the Gaussian
    width : float
        the width of the Gaussian

    Returns
    -------
    result : np.ndarray
        the Gaussian function

    """

    model = np.zeros_like(frequency)
    model += amplitude*np.exp(-(center-frequency)**2.0/(2.0*width**2))
    model += offset

    return model


def harvey_none(frequency, white_noise, ab=False):
    """
    No Harvey model

    Parameters
    ----------
    frequency : numpy.ndarray
        the frequency array
    white_noise : float
        the white noise component

    Returns
    -------
    model : numpy.ndarray
        the no-Harvey (white noise) model

    """

    model = np.zeros_like(frequency)
    model += white_noise

    return model


def harvey_one(frequency, tau_1, sigma_1, white_noise, ab=False):
    """
    One Harvey model

    Parameters
    ----------
    frequency : numpy.ndarray
        the frequency array
    tau_1 : float
        timescale of the first harvey component [Ms]
    sigma_1 : float
        amplitude of the first harvey component
    white_noise : float
        the white noise component

    Returns
    -------
    model : numpy.ndarray
        the one-Harvey model

    """

    model = np.zeros_like(frequency)
    if not ab:
        model += (4.*(sigma_1**2.)*tau_1)/(1.0+(2.*np.pi*tau_1*frequency)**2.0+(2.*np.pi*tau_1*frequency)**4.0)
    else:
        model += tau_1/(1.0+(sigma_1*frequency)**2.0+(sigma_1*frequency)**4.0)
    model += white_noise

    return model


def harvey_two(frequency, tau_1, sigma_1, tau_2, sigma_2, white_noise, ab=False):
    """
    Two Harvey model

    Parameters
    ----------
    frequency : numpy.ndarray
        the frequency array
    tau_1 : float
        timescale of the first harvey component
    sigma_1 : float
        amplitude of the first harvey component
    tau_2 : float
        timescale of the second harvey component
    sigma_2 : float
        amplitude of the second harvey component
    white_noise : float
        the white noise component

    Returns
    -------
    model : numpy.ndarray
        the two-Harvey model

    """

    model = np.zeros_like(frequency)
    if not ab:
        model += (4.*(sigma_1**2.)*tau_1)/(1.0+(2.*np.pi*tau_1*frequency)**2.0+(2.*np.pi*tau_1*frequency)**4.0)
        model += (4.*(sigma_2**2.)*tau_2)/(1.0+(2.*np.pi*tau_2*frequency)**2.0+(2.*np.pi*tau_2*frequency)**4.0)
    else:
        model += tau_1/(1.0+(sigma_1*frequency)**2.0+(sigma_1*frequency)**4.0)
        model += tau_2/(1.0+(sigma_2*frequency)**2.0+(sigma_2*frequency)**4.0)
    model += white_noise

    return model


def harvey_three(frequency, tau_1, sigma_1, tau_2, sigma_2, tau_3, sigma_3, white_noise, ab=False):
    """
    Three Harvey model

    Parameters
    ----------
    frequency : numpy.ndarray
        the frequency array
    tau_1 : float
        timescale of the first harvey component
    sigma_1 : float
        amplitude of the first harvey component
    tau_2 : float
        timescale of the second harvey component
    sigma_2 : float
        amplitude of the second harvey component
    tau_3 : float
        timescale of the third harvey component
    sigma_3 : float
        amplitude of the third harvey component
    white_noise : float
        the white noise component

    Returns
    -------
    model : numpy.ndarray
        the three-Harvey model
    """

    model = np.zeros_like(frequency)
    if not ab:
        model += (4.*(sigma_1**2.)*tau_1)/(1.0+(2.*np.pi*tau_1*frequency)**2.0+(2.*np.pi*tau_1*frequency)**4.0)
        model += (4.*(sigma_2**2.)*tau_2)/(1.0+(2.*np.pi*tau_2*frequency)**2.0+(2.*np.pi*tau_2*frequency)**4.0)
        model += (4.*(sigma_3**2.)*tau_3)/(1.0+(2.*np.pi*tau_3*frequency)**2.0+(2.*np.pi*tau_3*frequency)**4.0)
    else:
        model += tau_1/(1.0+(sigma_1*frequency)**2.0+(sigma_1*frequency)**4.0)
        model += tau_2/(1.0+(sigma_2*frequency)**2.0+(sigma_2*frequency)**4.0)
        model += tau_3/(1.0+(sigma_3*frequency)**2.0+(sigma_3*frequency)**4.0)
    model += white_noise

    return model