#!/bin/env python

def var( tree, varName, type=float ):
    tree.var(varName, type)

def fill( tree, varName, value ):
    tree.fill( varName, value )

# simple p4

def bookP4( tree, pName ):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_theta'.format(pName=pName))
    var(tree, '{pName}_eta'.format(pName=pName))
    var(tree, '{pName}_phi'.format(pName=pName))
    var(tree, '{pName}_m'.format(pName=pName))

def fillP4( tree, pName, p4 ):
    fill(tree, '{pName}_e'.format(pName=pName), p4.e() )
    fill(tree, '{pName}_pt'.format(pName=pName), p4.pt() )
    fill(tree, '{pName}_theta'.format(pName=pName), p4.theta() )
    fill(tree, '{pName}_eta'.format(pName=pName), p4.eta() )
    fill(tree, '{pName}_phi'.format(pName=pName), p4.phi() )
    fill(tree, '{pName}_m'.format(pName=pName), p4.m() )

# simple particle
ptc_tags = ["pdgid", "ip", "ip_signif", "theta_0", "ip_xy", "ip_z", "sigma_pos", "sigma_dev" ]

def bookParticle( tree, pName ):
    for tag in ptc_tags:
        var(tree, '{pName}_{tag}'.format(pName=pName, tag=tag))
        
    bookP4(tree, pName)
    
def fillParticle( tree, pName, particle ):
    fill(tree, '{pName}_pdgid'.format(pName=pName), particle.pdgid() )
    ip = -99
    ip_signif = -1e9
    theta_0 = -99
    ip_xy = -99
    ip_z = -99
    sigma_pos = -99
    sigma_dev = -99
    if hasattr(particle, 'path'):
        path = particle.path
        if hasattr(path, 'IP'):
            ip = path.IP
        if hasattr(path, 'IP_signif'):
            ip_signif = path.IP_signif
            sigma_dev = path.IP_sigma_dev
            sigma_pos = path.IP_sigma_pos
        if hasattr(path, 'theta_0'):
            theta_0 = path.theta_0
        if hasattr(path, 'IPcoord'):
            ip_z = particle.path.IPcoord.z()
            ip_xy = (particle.path.IPcoord.x()**2 + particle.path.IPcoord.y()**2)**0.5
    fill(tree, '{pName}_ip'.format(pName=pName), ip )
    fill(tree, '{pName}_ip_signif'.format(pName=pName), ip_signif )
    fill(tree, '{pName}_theta_0'.format(pName=pName), theta_0 )
    fill(tree, '{pName}_ip_xy'.format(pName=pName), ip_xy )
    fill(tree, '{pName}_ip_z'.format(pName=pName), ip_z )
    fill(tree, '{pName}_sigma_dev'.format(pName=pName), sigma_dev )
    fill(tree, '{pName}_sigma_pos'.format(pName=pName), sigma_pos )
    fillP4(tree, pName, particle )


def bookCluster( tree, name ):
    var(tree, '{name}_e'.format(name=name))
    var(tree, '{name}_layer'.format(name=name))

layers = dict(
    ecal_in = 0,
    hcal_in = 1
)
    
def fillCluster( tree, name, cluster ):
    fill(tree, '{name}_e'.format(name=name), cluster.energy )
    fill(tree, '{name}_layer'.format(name=name), layers[cluster.layer] )
    
# jet

def bookComponent( tree, pName ):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_num'.format(pName=pName))

def fillComponent(tree, pName, component):
    fill(tree, '{pName}_e'.format(pName=pName), component.e() )
    fill(tree, '{pName}_pt'.format(pName=pName), component.pt() )
    fill(tree, '{pName}_num'.format(pName=pName), component.num() )
    
    
pdgids = [211, 22, 130, 11, 13]
    
def bookJet( tree, pName ):
    bookP4(tree, pName )
    for pdgid in pdgids:
        bookComponent(tree, '{pName}_{pdgid:d}'.format(pName=pName, pdgid=pdgid))
    for tagger in ['IP_b_LL', 'IPs_b_LL', 'TCHE', 'TCHE_IP', 'TCHE_x', 'TCHE_y',\
                    'TCHE_z', 'TCHE_xy', 'TCHE_pt', 'TCHE_dr', 'TCHP', 'TCHP_IP']:
        var(tree, '{pName}_{tagger}'.format(pName=pName, tagger=tagger))
    for ptc in ['K0s', 'Kp', 'L0', 'S0', 'Sp', 'Sm', 'Muons'] :
        var(tree, '{pName}_{ptc}'.format(pName=pName, ptc=ptc))

def fillJet( tree, pName, jet ):
    fillP4(tree, pName, jet )
    for tagger in ['IP_b_LL', 'IPs_b_LL', 'TCHE', 'TCHE_IP', 'TCHE_x', 'TCHE_y',\
                    'TCHE_z', 'TCHE_xy', 'TCHE_pt', 'TCHE_dr', 'TCHP', 'TCHP_IP']:
        if tagger in jet.tags:
            fill(tree, '{pName}_{tagger}'.format(pName=pName, tagger=tagger), jet.tags.get(tagger, None))
        else:
            fill(tree, '{pName}_{tagger}'.format(pName=pName, tagger=tagger), -99)
                
    for ptc in ['K0s', 'Kp', 'L0', 'S0', 'Sp', 'Sm', 'Muons'] :
        if ptc in jet.tags:
            fill(tree, '{pName}_{ptc}'.format(pName=pName, ptc=ptc), jet.tags.get('{ptc}'.format(ptc=ptc), None))
        else:
            fill(tree, '{pName}_{ptc}'.format(pName=pName, ptc=ptc), -99)
    for pdgid in pdgids:
        component = jet.constituents.get(pdgid, None)
        if component is not None:
            fillComponent(tree,
                          '{pName}_{pdgid:d}'.format(pName=pName, pdgid=pdgid),
                          component )
        else:
            import pdb; pdb.set_trace()
            print jet
    

# isolation
from LeptonAnalyzer import pdgids as iso_pdgids
# iso_pdgids = [211, 22, 130]

def bookIso(tree, pName):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_num'.format(pName=pName))    
    
def fillIso(tree, pName, iso):
    fill(tree, '{pName}_e'.format(pName=pName), iso.sume )
    fill(tree, '{pName}_pt'.format(pName=pName), iso.sumpt )
    fill(tree, '{pName}_num'.format(pName=pName), iso.num )    

def bookLepton( tree, pName ):
    bookParticle(tree, pName )
    for pdgid in iso_pdgids:
        bookIso(tree, '{pName}_iso{pdgid:d}'.format(pName=pName, pdgid=pdgid))
    bookIso(tree, '{pName}_iso'.format(pName=pName))
        
        
def fillLepton( tree, pName, lepton ):
    fillParticle(tree, pName, lepton )
    for pdgid in iso_pdgids:
        #import pdb; pdb.set_trace()
        isoname='iso_{pdgid:d}'.format(pdgid=pdgid)
        if hasattr(lepton, isoname):
            iso = getattr(lepton, isoname)
            fillIso(tree, '{pName}_iso{pdgid:d}'.format(pName=pName, pdgid=pdgid), iso)
    #fillIso(tree, '{pName}_iso'.format(pName=pName), lepton.iso)
    
        
def bookIsoParticle(tree, pName):
    bookParticle(tree, pName )
    bookLepton(tree, '{pName}_lep'.format(pName=pName) )

def fillIsoParticle(tree, pName, ptc, lepton):
    fillParticle(tree, pName, ptc)
    fillLepton(tree, '{pName}_lep'.format(pName=pName), lepton)
    
def bookZed(tree, pName):
    bookParticle(tree, pName )
    bookParticle(tree, '{pName}_leg1'.format(pName=pName)  )
    bookParticle(tree, '{pName}_leg2'.format(pName=pName)  )

def fillZed(tree, pName, zed):
    fillParticle(tree, pName, zed)
    fillParticle(tree, '{pName}_leg1'.format(pName=pName), zed.leg1 )
    fillParticle(tree, '{pName}_leg2'.format(pName=pName), zed.leg2 )

def bookMet(tree, pName):
    var(tree, '{pName}_pt'.format(pName=pName)  )
    var(tree, '{pName}_sumet'.format(pName=pName)  )    
    var(tree, '{pName}_phi'.format(pName=pName)  )

def fillMet(tree, pName, met):
    fill(tree, '{pName}_pt'.format(pName=pName), met.pt() )
    fill(tree, '{pName}_sumet'.format(pName=pName), met.sum_et() )
    fill(tree, '{pName}_phi'.format(pName=pName), met.phi() )


