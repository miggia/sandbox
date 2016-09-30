
# coding: utf-8

import sympy as sp
from IPython.display import display
sp.init_printing()

def mte(e,var, var_num,o):
    """

    Returns the list of multivariate partial derivatives of expression "e", 
    in the variables listed in "var" up to order "o".
    
    >>> from sympy.abc import x, y
    >>> 
	
	https://en.wikipedia.org/wiki/Taylor_series
    
    """
    dd = [[e]] # list of partial derivatives
    ff = [[1]] # list of polynomial terms
    ll = 1 # factorial term
    
    
    rr = [] # replacements list of tuples
    for v, vn in zip(var,var_num): 
        rr.append((v,vn))

    te = e.subs(rr) # taylor expansion term to be returned    
    
    for o in range(1,o+1):
        aa = []
        hh = []
        ll = 1/sp.factorial(o)
        for d, f in zip(dd[-1],ff[-1]): # process only the last elements of the lists
            bb = []
            gg = []
            for v, vn in zip(var,var_num): 
                gg.append((v-vn)*f)
                bb.append(sp.diff(d,v))
            for tt in bb: aa.append(tt) # flatten bb to aa
            for uu in gg: hh.append(uu) # flatten gg to hh
        
        for a, h in zip(aa,hh):
            te += ll*a.subs(rr)*h

        dd.append(aa)
        ff.append(hh)

    return te


def main():  
    θ_1, θ_2, d, l, r, ρ, ρ_0, a = sp.symbols("theta_1, theta_2, d, l, r, rho, rho_0, a", real=True, positive=True)
    x, y = sp.symbols('x, y', real=True)
    e = (θ_1 + θ_2)**2
    e2 = sp.exp(x)*sp.log(1+y)
    var = [θ_1,θ_2]
    var2 = [x,y]
    var_num = [-1, -2]
    var_num2 = [0,0]
    o = 3
    o2 = 2
    display(mpd(e2,var2,var_num2,o2))
    #display(ptl(var,o))

if __name__ == "__main__":
    main()