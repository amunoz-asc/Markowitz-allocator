class Markowitz_Allocator_WR:
    def __init__(self,observations,r,stock_name = np.array([])):
        self.stock = stock_name
        self.r = r
        assert r>0, "Rate must be greater than 0"
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
    
    def get_parametres_wr(self):
        diff = self.mu - self.r
        temp = np.asarray(self.Cinv@diff)[0]
        temp = np.sum(temp)
        thet_t = 1/temp
        s = np.asarray(thet_t*self.Cinv@diff)[0]
        var_t = (float(s@self.C@s))
        ret_t = (float(s@self.mu))
        return thet_t, ret_t, var_t
    
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
    
    def get_var_and_ret_sr(self,start=0,step=0.000001):
        thet_t, ret_t, var_t = self.get_parametres_sr()
        the_sr = np.arange(start,thet_t,step)
        mu_sr = np.insert(self.mu,0,self.r)
        diff = self.mu - self.r
        var_sr = []
        ret_sr = []
        for tc in the_sr:
            s = np.asarray(tc*self.Cinv@diff)[0]
            var_sr.append(float(s@self.C@s))
            x0 = 1-sum(s)
            s = np.insert(s,0,x0)
            ret_sr.append(float(s@mu_sr))
        var_sr = np.array(var_sr)
        ret_sr = np.array(ret_sr)
        return var_sr, ret_sr, var_t, ret_t, diff
    
    def efficient(self,ex_return = -1, ex_variance =-1,start=0,stop=0.1,step = 0.000001):
        if ((ex_return == -1) and (ex_variance ==-1) or (ex_return != -1) and (ex_variance !=-1)):
            print ("Nous suggérons de donner des valeur au rendement ou à la variance")
            return None
        var, ret, k1, k2 = self.get_var_and_ret(start,stop,step)
        var_sr, ret_sr, var_t, ret_t, diff = self.get_var_and_ret_sr(start,step)
        plt.plot(var,ret)
        plt.plot(var_sr,ret_sr,label = 'Frontière d\'efficience ')
        plt.title('Rendement attendu vs Variance')
        plt.plot(var_t, ret_t, marker="*", markersize=10,label = 'Portefeuille Tangent')
        plt.plot(0, self.r, marker="o", markersize=5, label = 'Taux')
        if ex_variance == -1:
            index = np.argmin(abs(ret_sr-ex_return))
        if ex_return == -1:
            index = np.argmin(abs(var_sr-ex_variance))
        plt.plot(var_sr[index], ret_sr[index], marker="o", markersize=7)
        plt.axvline(var_sr[index],linestyle = '--')
        plt.axhline(ret_sr[index],linestyle = '--')
        print('Rendement :',ret_sr[index],'       ' ,'Variance :',var_sr[index])
        plt.axis([-0.05, 2.3, -2, 95])
        plt.legend()
        s_opt = np.asarray((step*index)*self.Cinv@diff)[0]
        x0 = 1 - sum(s_opt)
        s_opt = np.insert(s_opt,self.n_assets,x0)
        return optimal_portfolio_weights(self.stock,s_opt)
