"""
Assistant functions for computation of metrics
"""
from dolfinx.fem import assemble_scalar, form
from ufl import dx

def total_mass(u):
    return assemble_scalar(form(u*dx))

def average(u):
    abs_domain = 1
    return assemble_scalar(form(u*dx)) / abs_domain 

def dev_from_average(u):
    abs_domain = 1
    return assemble_scalar(form(u*u*dx)) - abs_domain * average(u)**2 