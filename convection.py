"""
Parses the correct formulation of the convection term and the stabilization scheme
"""
from ufl import inner, dx, jump, avg, dot, grad, ds, dS, sqrt, max_value, min_value, div, nabla_grad
import numpy as np

def convection_parser(args, v, c, testf, normal):
    tex_string = ""

      
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

    if args.stabilization == "supg":
        w = testf + tau*dot(v,grad(testf))
    else:
        w = testf

    #SECTION - Convection Term
    if args.convection == "weak":
        F = (-1)*c*dot(v,grad(w))*dx

        if args.functionspaceorder >0:
            tex_string += "- \int_{ \Omega } c^{ n + \\theta }  v\cdot \\nabla w"

        if args.functionspace == "DG":
            F+= inner(v,normal('+'))* jump(c*w) *dS

            tex_string += " + \sum_{ F \in F^i_h } \int_F v\cdot \eta [ c^{ n + \\theta }  w]"

    elif args.convection == "prod":
        sig = args.sigma
        F = dot(v, grad(c))*w*dx
        tex_string += "+ \\int_{ \Omega } w v\cdot \\nabla c^{ n + \\theta }  "

        if sig > 0:
            F += sig*c*div(v)*w*dx 
            tex_string += "+ \sigma \int_{ \Omega } c^{ n + \\theta }  w \\nabla \cdot v "

    elif args.convection == "strng":
        F = div(v*c) * w*dx
        tex_string += "+  \int_{ \Omega } w \\nabla \cdot (v c^{ n + \\theta } ) "
    #!SECTION


    #SECTION - Stabilization Terms
    if args.stabilization == "iad":
        # source: 
        F+= alpha * h* abs_v * 1/2  * inner(grad(c), grad(w))*dx
        tex_string += "+ \\alpha \\frac{|v| h}{2} (\\nabla c^{ n + \\theta } , \\nabla w)"
    
    elif args.stabilization == "su":
        F+= alpha * h * 1/2 * 1/abs_v * inner(v, grad(c)) * inner(v, grad(w))*dx
        tex_string += "+ \\alpha \\frac{ h }{2 |v| } ((v \cdot \\nabla) c^{ n + \\theta } , (v \cdot \\nabla) w)"
               
    elif args.stabilization == "tg":
        F+= alpha * h * 1/2 * 1/abs_v * inner(v, grad(c)) * div(v * w)*dx
        tex_string += "+ \\alpha \\frac{ h }{2 |v| } ((v \cdot \\nabla) c^{ n + \\theta } , \\nabla \cdot (v w))"

        
    elif args.stabilization == "dgu":
        # source: Di Pietro and Ern
        F+= - inner(v,normal('+'))*jump(c)*avg(w)*dS + 1/2 * abs(inner(v,normal('+')))*jump(c)*jump(w)*dS
        tex_string += "- \sum_{ F \in F^i_h } \int_F v \cdot \eta [ c^{ n + \\theta }  ] \\langle w \\rangle + \\frac{ 1 }{ 2 } \sum_{ F \in F^i_h } \int_F | v \cdot \eta | [ c^{ n + \\theta }  ] [ w ]"
    
    

    #!SECTION

    return (F,tex_string)