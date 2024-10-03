"""
Command Line Interface
"""
from argparse import ArgumentParser, Namespace

def get_args():
    #SECTION - List of different options for better readability
    fs = ["CG", "DG"]                                       # function space options
    fsorder = [0,1,2,3,4,5]                                 # polynomial order
    convectionform = ["strng", "weak", "prod"]              # discretization of the convection term
    sigma = [0,1]                                           # choice for parameter sigma
    theta = [0,1]                                           # choice for parameter theta
    stab = ["standard", "iad", "su", "supg", "tg", "dgu"]   # choice of stabilization scheme
    alpha = [0,1,2]                                         # add later
    dt = 0.01                                               # temporal discretization / time step
    dh = 64                                                 # spatial discretization / partitions
    T = 2.0                                                 # experiment end time

    # rkorder = [0,1,2] #TODO - add higher order runge kutta methods later
    #!SECTION
    
    #SECTION - Define Arguement Parser
    parser = ArgumentParser(description="This program runs a single simulation with specification by command line input.")

    parser.add_argument('-fs','--functionspace', type=str, metavar='', nargs='?', const="CG", default="CG", help='Choose a continous or discontinuous Galerkin approach. The options are: '+str(fs)) 

    parser.add_argument('-fso','--functionspaceorder', type=int, metavar='', nargs='?', const=1, default=1, help='Choose the polynomial order. The options are: '+str(fsorder)) 

    parser.add_argument('-cf','--convection', type=str, metavar='', nargs='?', const="weak", default="weak", help='Choose a convection formulation. strng for (div(vc),w). weak for -(vc,grad(w)). prod for sigma*(div(v) c, w) + ((grad(c), v), w). The options are: '+str(convectionform)) 

    parser.add_argument('-s','--sigma', type=int, metavar='', nargs='?', const=1, default=1, help='Defines sigma in order to define the form as conservative (sigma=1) or non-conservative (sigma=0). The options are 0 or 1.') 

    parser.add_argument('-th','--theta', type=float, metavar='', nargs='?', const=1.0, default=1.0, help='Choose the temporal discretization in the interval [0,1]. Theta = 0 for explicit Euler. Theta = 1 for implicit Euler. The options are floats in the interval: '+str(theta)) 

    #TODO - add higher runge kutta discretizations in time later
    # parser.add_argument('-rk','--rungekuttaorder', type=int, metavar='', nargs='?', const=0, default=0, help='Choose the order of the Runge Kutta approximation in time. The options are: '+str(rkorder)) 

    parser.add_argument('-stab','--stabilization', type=str, metavar='', nargs='?', const="standard", default="standard", help='Choose the stabilization algorithm. For None, Isotropic Artificial Diffusion, Streamline Upwind, Streamline Upwind Petrov-Galerkin, Taylor-Galerkin or Discontinuous Galerkin Upwind choose: '+str(stab)) 

    parser.add_argument('-a','--alpha', type=int, metavar='', nargs='?', const=1, default=1, help='Choose the stabilization parameter alpha. The options are 1.0, max(Pe,1), min(1, Pe/6). Choose with integer keys: '+str(alpha)) 

    parser.add_argument('-dt','--dt', type=float, metavar='',nargs='?', const=dt, default=dt,  help='Specifies resolution of time partition. Default is set to: ' + str(dt))

    parser.add_argument('-dh','--dh', type=int, metavar='',nargs='?', const=dh, default=dh,  help='Specifies resolution of space partition. Default is set to: ' + str(dh))

    parser.add_argument('-T','--T', type=float, metavar='', nargs='?', const=T, default=T,  help='Specifies end time. Default is set to: ' + str(T))

    #!SECTION

    # parse arguments
    args = parser.parse_args()

    #SECTION - Sanity check of parsed arguments
    bool_list = [args.functionspace in fs, args.functionspaceorder in fsorder, args.convection in convectionform, args.sigma in sigma, args.theta <= 1.0, args.theta >= 0.0,  args.stabilization in stab]
    
    # args.rungekuttaorder in rkorder, #TODO - add higher order runge kutta methods later
    
    if False in bool_list:
        raise ValueError("One of the given inputs does not fit to the expected format. Try again. For help use:\n python -m main -h")
    
    #!SECTION

    return args

if __name__ == '__main__':
    print(get_args())