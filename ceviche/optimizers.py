import numpy as np
from tqdm import tqdm
from functools import partial
import time
from autograd.numpy.numpy_boxes import ArrayBox

def adam_optimize(objective, state, jacobian, step_size=1e-2, Nsteps=100, bounds=None, direction='min', beta1=0.9, beta2=0.999, callback=None, verbose=False):
    """Performs Nsteps steps of ADAM minimization of function `objective` with gradient `jac`.
    The `bounds` are set abruptly by rejecting an update step out of bounds."""
    of_list = []

    np.set_printoptions(formatter={'float': '{: 1.4f}'.format})

    for iteration in tqdm(range(Nsteps)):

        if callback:
            rho, params = callback(iteration, of_list, state)

        obj = partial(objective, params=params)
        jac = jacobian(obj)

        t_start = time.time()
        if jacobian==True:
            of, grad = obj(rho)
        else:
            of = obj(rho)
            grad = jac(rho)
        t_elapsed = time.time() - t_start

        of_list.append(of._value if type(of) is ArrayBox else of)

        if verbose:
            print("Epoch: %3d/%3d | Duration: %.2f secs | Value: %5e" %(iteration+1, Nsteps, t_elapsed, of_list[-1]))

        if iteration == 0:
            mopt = np.zeros(grad.shape)
            vopt = np.zeros(grad.shape)

        (grad_adam, mopt, vopt) = step_adam(grad, mopt, vopt, iteration, beta1, beta2)

        if direction == 'min':
            rho = rho - step_size*grad_adam
        elif direction == 'max':
            rho = rho + step_size*grad_adam
        else:
            raise ValueError("The 'direction' parameter should be either 'min' or 'max'")

        if bounds:
            rho[rho < bounds[0]] = bounds[0]
            rho[rho > bounds[1]] = bounds[1]

    return (rho, of_list)


def step_adam(gradient, mopt_old, vopt_old, iteration, beta1, beta2, epsilon=1e-8):
    """ Performs one step of adam optimization"""

    mopt = beta1 * mopt_old + (1 - beta1) * gradient
    mopt_t = mopt / (1 - beta1**(iteration + 1))
    vopt = beta2 * vopt_old + (1 - beta2) * (np.square(gradient))
    vopt_t = vopt / (1 - beta2**(iteration + 1))
    grad_adam = mopt_t / (np.sqrt(vopt_t) + epsilon)

    return (grad_adam, mopt, vopt)
