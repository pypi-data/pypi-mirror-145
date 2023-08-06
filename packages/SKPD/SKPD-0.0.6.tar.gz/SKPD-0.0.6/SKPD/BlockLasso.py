from sklearn.linear_model import Lasso,LassoCV
from  .my_operator import *
from .criterion import *
def _ols(Z,Y):
    regr = LR(fit_intercept = True)
    regr.fit(Z,np.array(Y).squeeze())

    pred_design = regr.predict(Z)
    residual = [Y[i] - pred_design[i] for i in range(len(Y))]
    # return self.z,self.Y
    return residual
def BlockLasso(X,Y,p1,d1,p2,d2,p3,d3,lam,Z = None):
    if not Z is None:
        Y = _ols(Z,Y)
    RX = [Rearrange(xi,p1,d1,p2,d2,p3,d3) for xi in X]
    RX = np.asarray(RX)
    design_X = np.mean(RX, axis = 2)
    if isinstance(lam,list):
        sample_size = len(Y)
        MBIC_list = []
        for lmbda in lam:
            reg = Lasso(alpha = lmbda, random_state=0,fit_intercept =False).fit(design_X, Y)
            Y_hat = reg.predict(design_X)
            fN = RMSE(Y_hat,Y)
            a_hat = reg.coef_
            s = np.where(a_hat !=0)[0].shape[0]
            p = a_hat.shape[0]
            MBIC = sample_size * np.log(fN ** 2) + s * np.log(sample_size) * np.log(np.log(p))
            MBIC_list.append(MBIC)

        print("MBIC results: ",MBIC_list)
        opt_idx = MBIC_list.index(min(MBIC_list))
        lam = lam[opt_idx]
        print("choosed lambda is : ",lam, " and its MBIC : ", MBIC_list[opt_idx])

    reg = Lasso(alpha = lam, random_state=0,fit_intercept =False).fit(design_X, Y)
    Y_hat = reg.predict(design_X)
    return reg, Y_hat