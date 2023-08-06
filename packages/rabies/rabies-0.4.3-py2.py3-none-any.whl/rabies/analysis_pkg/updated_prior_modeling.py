from sklearn.utils import check_random_state
import numpy as np
from rabies.analysis_pkg.analysis_math import closed_form


def parallel_OLS_fit(X, q=1, c_init=None, C_prior=None, tol=1e-6, max_iter=200, verbose=1):
    # X: time by voxel matrix
    # q: number of new components to fit
    # c_init: can specify an voxel by component number matrix for initiating weights
    # C_prior: a voxel by component matrix of priors that are included in the fitting, but fixed as constant components
    
    if q<1:
        return np.zeros([X.shape[1], 0])
    
    # q defines the number of new sources to fit
    if c_init is None:
        random_state = check_random_state(None)
        c_init = random_state.normal(
            size=(X.shape[1], q))
        
    if C_prior is None:
        C_prior = np.zeros([X.shape[1], 0])
    C_prior /= np.sqrt((C_prior ** 2).sum(axis=0))
    num_prior = C_prior.shape[1]
    
    C = c_init
    C /= np.sqrt((C ** 2).sum(axis=0))
    
    for i in range(max_iter):
        C_prev = C
        C_ = np.concatenate((C, C_prior), axis=1) # add in the prior to contribute to the fitting
        
        ##### temporal convergence step
        W = closed_form(C_, X.T).T

        C_ = closed_form(W, X).T
            
        if num_prior>0:
            C = C_[:,:-num_prior] # take out the fitted components
        else:
            C = C_
        C /= np.sqrt((C ** 2).sum(axis=0))

        ##### evaluate convergence
        lim = np.abs(np.abs((C * C_prev).sum(axis=0)) - 1).mean()
        if verbose > 2:
            print('lim:'+str(lim))
        if lim < tol:
            if verbose > 1:
                print(str(i)+' iterations to converge.')
            break
        if i == max_iter-1:
            if verbose > 0:
                print(
                    'Convergence failed. Consider increasing max_iter or decreasing tol.')
    return C


def optimized_neural_source_modeling(X, n_extra_fit, C_prior, verbose=1):
    
    num_priors = C_prior.shape[1]

    C_extra = parallel_OLS_fit(X, q=n_extra_fit, C_prior=C_prior, C_ortho=False, method='dual_OLS', verbose=verbose)
    
    corr_list=[]
    C_fitted_prior = np.zeros([X.shape[1], num_priors])
    for i in range(num_priors):
        prior = C_prior[:,i] # the prior that will be fitted
        N_prior = np.concatenate((C_extra, C_prior[:,:i], C_prior[:,i+1:]), axis=1) # combine previously-fitted extra components with priors not getting fitted
        C_fitted_prior[:,i] = parallel_OLS_fit(X, q=1, C_prior=N_prior, C_ortho=False, method='dual_OLS', verbose=verbose).flatten() # fit the selected prior, left out of N_prior
            
        corr = np.corrcoef(C_fitted_prior[:,i].T, prior.T)[0,1]
        if corr<0: # if the correlation is negative, invert the weights on the fitted component
            C_fitted_prior[:,i]*=-1
        corr_list.append(np.abs(corr))

    ### compute the timecourses and normalize variance
    # the finalized C
    C = np.concatenate((C_fitted_prior, C_extra), axis=1)

    # L-2 norm normalization of the components
    C /= np.sqrt((C ** 2).sum(axis=0))
    W = closed_form(C,X.T, intercept=False).T
    # the components will contain the weighting/STD/singular value, and the timecourses are normalized
    C=C*W.std(axis=0)
    # normalize the component timecourses to unit variance
    W /= W.std(axis=0)
    
    return {'C_fitted_prior':C[:,:num_priors], 'C_extra':C[:,num_priors:], 
            'W_fitted_prior':W[:,:num_priors], 'W_extra':W[:,num_priors:],
            'corr_list':corr_list}
