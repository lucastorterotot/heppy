from heppy.framework.analyzer import Analyzer
from heppy.fastsim.pdt import particle_data
from heppy.particles.tlv.particle import Particle 

import math
import random

from ROOT import TLorentzVector

def particle(pdgid, theta, phi, energy, flat_pt=False):
    mass, charge = particle_data[pdgid]
    costheta = math.cos(math.pi/2. - theta)
    sintheta = math.sin(math.pi/2. - theta)
    tantheta = sintheta / costheta
    cosphi = math.cos(phi)
    sinphi = math.sin(phi)        
    if flat_pt:
        pt = energy
        momentum = pt / sintheta
        energy = math.sqrt(momentum**2 + mass**2)
    else:
        momentum = math.sqrt(energy**2 - mass**2)
    tlv = TLorentzVector(momentum*sintheta*cosphi,
                         momentum*sintheta*sinphi,
                         momentum*costheta,
                         energy)
    return Particle(pdgid, charge, tlv) 
    

class Gun(Analyzer):
    
    def process(self, event):
        theta = random.uniform(self.cfg_ana.thetamin, self.cfg_ana.thetamax)
        phi = random.uniform(-math.pi, math.pi)
        energy = random.uniform( self.cfg_ana.ptmin, self.cfg_ana.ptmax)
        event.gen_particles = [particle(self.cfg_ana.pdgid, theta, phi, energy,
                                        flat_pt=self.cfg_ana.flat_pt)]
        event.gen_particles_stable = event.gen_particles