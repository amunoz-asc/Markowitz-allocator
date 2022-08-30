class Markowitz_Allocator:
    def __init__(self,observations,stock_name = np.array([])):
        self.stock = stock_name
        self.n_assets, self.n_obs = observations.shape
        self.C = np.asmatrix(np.cov(observations))
        self.Cinv = np.linalg.inv(self.C)
        self.mu = observations[:,self.n_obs-1]*(1+np.random.rand(self.n_assets)/10)
        
    def get_parametres(self):
        ones = np.ones(self.n_assets)
        k1 = np.asarray(float(1/(ones@self.Cinv@ones))*self.Cinv@ones)[0]
        k2 = self.mu-float(float(1/(ones@self.Cinv@ones))*ones@self.Cinv@self.mu)*ones
        k2 = np.asarray(self.Cinv@k2)[0]
        return k1, k2
    
    def get_var_and_ret(self,start=0,stop=0.1,step = 0.000001):
        k1, k2 = self.get_parametres()
        thetac = np.arange(start,stop,step)
        var = []
        ret = []
        for tc in thetac:
            s = (k1 + tc*k2)
            var.append(float(s@self.C@s))
            ret.append(float(s@self.mu))
        var = np.array(var)
        ret = np.array(ret)
        return var, ret, k1, k2
    
    def efficient(self,ex_return = -1, ex_variance =-1,start=0,stop=0.1,step = 0.000001):
        if ((ex_return == -1) and (ex_variance ==-1) or (ex_return != -1) and (ex_variance !=-1)):
            print ("Nous suggérons de donner des valeur au rendement ou à la variance")
            return None
        var, ret, k1, k2 = self.get_var_and_ret(start,stop,step)
        plt.plot(var,ret)
        plt.title('Rendement attendu vs Variance')
        if ex_variance == -1:
            index = np.argmin(abs(ret-ex_return))
        if ex_return == -1:
            index = np.argmin(abs(var-ex_variance))
        plt.plot(var[index], ret[index], marker="o", markersize=10)
        plt.axvline(var[index],linestyle = '--')
        plt.axhline(ret[index],linestyle = '--')
        print('Rendement : ', ret[index],'      ','Variance : ', var[index])
        plt.axis([0.4, 1, 20, 50])
        s_opt = (k1 + (step*index)*k2)
        return optimal_portfolio_weights(self.stock,s_opt)
