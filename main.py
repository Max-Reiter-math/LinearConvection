import csv
import numpy as np
from dolfinx import mesh
from dolfinx.fem import functionspace, ElementMetaData, Function
from dolfinx.fem.petsc import LinearProblem
from dolfinx.io import VTXWriter
from ufl import TrialFunction, TestFunction, inner, dx, FacetNormal, grad, lhs,rhs, sqrt, max_value, min_value
from mpi4py import MPI

from CLI import get_args
from predfuncs import init_mass, initial_velocity
from convection import convection_parser
from post import *


#SECTION - getting and initializing args
args = get_args()
id = args.stabilization+"-"+args.functionspace+str(args.functionspaceorder)+"-"+args.convection+str(args.sigma)+"-to"+str(args.theta)
#TODO - add higher runge kutta discretizations in time later
# +"-rko"+str(args.rungekuttaorder)
print("ID: ", id)


dt = args.dt
T = args.T

#SECTION - DOMAIN
domain_partitions = args.dh
domain = mesh.create_unit_square(MPI.COMM_WORLD,domain_partitions, domain_partitions)
#!SECTION



#SECTION - FUNCTION SPACES AND FUNCTIONS
FS = functionspace(domain, (args.functionspace, args.functionspaceorder)) # Function Space for scalar variable
Vh = functionspace(domain, ElementMetaData("CG", 2 , shape=(2,)))  # Function Space for Velocity

v = Function(Vh, dtype=np.float64) # velocity field

# Trial Function
c = TrialFunction(FS)

# Test Function
testf = TestFunction(FS)

c1, c0 = Function(FS, dtype=np.float64, name = "c1"), Function(FS, dtype=np.float64, name = "c0")

if args.functionspace == "DG" and args.functionspaceorder == 0:
    c_out = Function(functionspace(domain, (args.functionspace, 1)), dtype=np.float64, name = "c")
else:
    c_out = Function(FS, dtype=np.float64, name = "c")
#!SECTION

#SECTION - Parameters
h = 1/args.dh    
abs_v = sqrt(inner(v,v))

eps = 0.01 # amount of artifical diffusion
Pe_h = abs_v *h /eps

alphas = [1.0, max_value(Pe_h,1), min_value(Pe_h/6,1) ]
# alpha = coth(Pe_h * 0.5) - 0.5 / Pe_h #TODO - implement later
alpha = alphas[args.alpha]
alpha_str = "1.0"

tau = alpha * h * 1/2 * 1/abs_v
#!SECTION

#SECTION - evtl. change of test function for SUPG scheme
if args.stabilization == "supg":
    w = testf + tau*inner(v,grad(testf))
else:
    w = testf
#!SECTION

#SECTION - Prescribing initial conditions
v.interpolate(initial_velocity)
c0.interpolate(init_mass)
c1.x.array[:] = c0.x.array[:]
c_out.interpolate(c0)
#!SECTION

#SECTION - Variational Formulation
n = FacetNormal(domain)

theta = args.theta
c_theta = theta*c + (1-theta)*c0

( C , textmp) = convection_parser(args, v, c_theta, w, n)

F = inner(c - c0, w)*dx + dt * C

texstr = "\\int_{ \Omega } \\frac{ c^{ n+1 } - c^n }{\Delta t} w " + textmp +" = 0 "

a = lhs(F)
L = rhs(F)

problem = LinearProblem(a, L, u=c1)#, bcs=bcs) #, petsc_options={"ksp_type": "preonly", "pc_type": "lu"})
#!SECTION



#SECTION - Temporal Loop
t = 0
vtx = VTXWriter(MPI.COMM_WORLD, "outputs/"+id+".bp", c_out, engine="BP4")
vtx.write(t)

metrics = [["time", "total mass", "min mass", "max mass", "dev from avg"]]

while t<=T:
    t+= dt  

    print(id, " time step - ", t)     
    metrics.append([t, total_mass(c1), np.min(c1.x.array[:]), np.max(c1.x.array[:]), dev_from_average(c1)])

    problem.solve()
    c0.x.array[:] = c1.x.array[:]
    c_out.interpolate(c1)
    
    vtx.write(t)
       

vtx.close()
#!SECTION

#SECTION - Output of model description
if args.stabilization == "supg":
    texstr = texstr.replace(" w","\\bar{ w }")
with open('outputs/'+id+'.md', 'w') as f:
    f.write("Model-ID: "+id+" \n\n")
    f.write("For a given $c^n$ we want to find a solution $c^{ n+1 } \\in "+args.functionspace+"^"+str(args.functionspaceorder)+"$ that solves the equation \n")
    f.write("$$ \n")
    f.write(texstr)
    f.write("\n")
    f.write("$$ \n")
    if args.stabilization == "supg":
        f.write("with $ \\bar{ w } = w + \\tau ( v \\cdot \\nabla) w $ ")
    f.write("for all $ w \\in "+args.functionspace+"^"+str(args.functionspaceorder)+"$. \n")
    f.write("Thereby the parameters were chosen as:\n")
    f.write("$$ \n")
    f.write("\\Delta t = "+str(args.dt))
    f.write("\n$$ \n")
    f.write("$$ \n")
    f.write("\\theta = "+str(args.theta))
    f.write("\n$$ \n")
    f.write("$$ \n")
    f.write("\\tau = \\frac{ \\alpha h }{2 \\vert v \\vert }")
    f.write("\n$$ \n")
    f.write("$$ \n")
    f.write("\\alpha = "+alpha_str)
    f.write("\n$$ \n")
    if args.convection == "prod" and args.sigma>0:
        f.write("$$ \n")
        f.write("\\sigma = "+str(args.sigma))
        f.write("\n$$ \n")
#!SECTION

#SECTION - Output of metrics
with open('outputs/'+id+'.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(metrics)
#!SECTION