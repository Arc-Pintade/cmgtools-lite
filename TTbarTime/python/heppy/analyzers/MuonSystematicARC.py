import os
import ROOT
from ROOT import TFile, TH2F

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer


# for eta the abs is for the parameter at function call
def eta_binned(eta_param):
    if(0 <= eta_param and eta_param < 0.9):
        return 1
    elif(0.9 <= eta_param and eta_param < 1.2):
        return 2   
    elif(1.2 <= eta_param and eta_param < 2.1):
        return 3
    elif(2.1 <= eta_param and eta_param < 2.4):
        return 4
 
def pt_binned(pt_param):
    if(20 <= pt_param and pt_param < 25):
        return 1
    elif(25 <= pt_param and pt_param < 30):
        return 2         
    elif(30 <= pt_param and pt_param < 40):
        return 3
    elif(40 <= pt_param and pt_param < 50):
        return 4 
    elif(50 <= pt_param and pt_param < 60):
        return 5 
    elif(60 <= pt_param and pt_param <= 120):
        return 6   


class MuonSystARC(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(MuonSystARC, self).__init__(cfg_ana, cfg_comp, looperName)
        
        rootfname_id = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/RunBCDEF_SF_ID_syst.root'])                       
        rootfname_iso = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/RunBCDEF_SF_ISO_syst.root'])

                              
        self.mc_syst_id_file = TFile(rootfname_id)
        self.mc_syst_id_hist = self.mc_syst_id_file.Get('NUM_TightID_DEN_genTracks_pt_abseta')                              
                
        self.mc_syst_iso_file = TFile(rootfname_iso)
        self.mc_syst_iso_hist = self.mc_syst_iso_file.Get('NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta')                              
        
        
    def process(self, event):

        syst_id_weight = 0.    
        syst_iso_weight = 0.
        muons = getattr(event, self.cfg_ana.muons)    
        for muon in muons: # caution abs(eta)
            if(muon.pt() <= 120):
                syst_id_weight  *= self.mc_syst_id_hist.GetBinContent(pt_binned(muon.pt()), eta_binned(abs(muon.eta())))
                syst_iso_weight *= self.mc_syst_iso_hist.GetBinContent(pt_binned(muon.pt()), eta_binned(abs(muon.eta())))
            
        setattr(event, 'systMuonIdWeight', syst_id_weight)
        setattr(event, 'systMuonIsoWeight', syst_iso_weight)
        event.eventSystWeight *= event.systMuonIdWeight
        event.eventSystWeight *= event.systMuonIsoWeight
        
        
        
