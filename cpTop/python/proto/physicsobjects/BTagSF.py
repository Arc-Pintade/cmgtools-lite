import os
import ROOT
import numpy as np

from ROOT import TRandom3, TFile
ROOT.gSystem.Load('libCondToolsBTau')

#todo: move this to separate BTagSF analyzer that could be configured? 
class BTagSF(object):
    '''Translate heppy run 1 BTagSF class to python, and update to 2012.
    '''
    def __init__ (self, seed, wp='loose', measurement='central') :
        self.randm = TRandom3(seed)

        rootfname = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/btag_efficiency_CSVv2.root'])# tagging_efficiencies_march2018_btageff-all_samp-inc-DeepCSV_medium.root
        self.mc_eff_file = TFile(rootfname)

        # MC b-tag efficiencies as measured in HTT by Adinda
        self.btag_eff_b = self.mc_eff_file.Get('btag_eff_b')
        self.btag_eff_c = self.mc_eff_file.Get('btag_eff_c')
        self.btag_eff_oth = self.mc_eff_file.Get('btag_eff_oth')

        # b-tag SFs from POG
        # Todo : COLIN 3jul18: new recommendation is DeepCSV V2. what about CSV v2? 
        calib = ROOT.BTagCalibration("CSVv2", os.path.expandvars("$CMSSW_BASE/src/CMGTools/TTbarTime/data/CSVv2_94XSF_V2_B_F.csv"))
        
        op_dict = {
            'loose':0,
            'medium':1,
            'tight':2
        }
        print 'Booking b/c reader'

        v_sys = getattr(ROOT, 'vector<string>')()
        v_sys.push_back('up')
        v_sys.push_back('down')

        self.reader_bc = ROOT.BTagCalibrationReader(op_dict[wp], measurement, v_sys)
        self.reader_bc.load(calib, 0, 'comb')
        self.reader_bc.load(calib, 1, 'comb')
        print 'Booking light reader'
        self.reader_light = ROOT.BTagCalibrationReader(op_dict[wp], measurement, v_sys)
        self.reader_light.load(calib, 2, 'incl')

    @staticmethod
    def getBTVJetFlav(flav):
        if abs(flav) == 5:
            return 0
        elif abs(flav) == 4:
            return 1
        return 2

    def getMCBTagEff(self, pt, eta, flavor):
        hist = self.btag_eff_oth
        if flavor == 5:
            hist = self.btag_eff_b
        elif flavor == 4:
            hist = self.btag_eff_c

        binx = hist.GetXaxis().FindFixBin(pt)
        biny = hist.GetYaxis().FindFixBin(abs(eta))
        eff = hist.GetBinContent(binx, biny)
        return eff

    def getPOGSFB(self, pt, eta, flavor):
        if flavor in [4, 5]:
            return self.reader_bc.eval_auto_bounds('central', self.getBTVJetFlav(flavor), eta, pt)

        return self.reader_light.eval_auto_bounds('central', self.getBTVJetFlav(flavor), eta, pt)

    def isBTagged(self, pt, eta, csv, jetflavor, is_data, csv_cut=0.5803 ):
        jetflavor = abs(jetflavor)

        if is_data or pt < 20. or abs(eta) > 2.5:
            if csv > csv_cut:
                return True
            else:
                return False


        SFb = self.getPOGSFB(pt, abs(eta), jetflavor)
        eff_b = self.getMCBTagEff(pt, abs(eta), jetflavor)

        # if pt < 30.:
        #     print 'pt, eta:', pt, eta
        #     print 'SFb', SFb
        #     print 'eff_b', eff_b

        promoteProb_btag = 0. # probability to promote to tagged
        demoteProb_btag = 0. #probability to demote from tagged

        self.randm.SetSeed((int)((np.float32(eta)+5)*100000))
        btagged = False

        if SFb < 1.:
            demoteProb_btag = abs(1. - SFb)
        else:
            if eff_b in [0.,1.]:
                promoteProb_btag = 0.
            else:
                promoteProb_btag = abs(SFb - 1.)/((1./eff_b) - 1.)

        if csv > csv_cut:
            btagged = True
            if demoteProb_btag > 0. and self.randm.Uniform() < demoteProb_btag:
                btagged = False
        else:
            btagged = False
            if promoteProb_btag > 0. and self.randm.Uniform() < promoteProb_btag:
                btagged = True

        return btagged


if __name__ == '__main__':

    btag = BTagSF(12345)
    print 'created BTagSF instance'
    print btag.isBTagged(25., 2.3, 0.9, 5, False)
    print btag.isBTagged(104.3933, -0.885529, 0.9720, 5, False)

