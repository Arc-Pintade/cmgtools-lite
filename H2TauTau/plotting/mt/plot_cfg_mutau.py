from collections import namedtuple
from operator import itemgetter

from CMGTools.H2TauTau.proto.samples.summer16.htt_common import lumi
from CMGTools.H2TauTau.proto.plotter.PlotConfigs import SampleCfg, HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import inc_sig
from CMGTools.H2TauTau.proto.plotter.categories_common import cat_J1, cat_VBF
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms, createTrees
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import taumu_vars, getVars
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.qcdEstimation import qcd_estimation
from CMGTools.H2TauTau.proto.plotter.JetFakesEstimation import jetFakesEstimation
from CMGTools.H2TauTau.proto.plotter.cut import Cut
from CMGTools.H2TauTau.proto.plotter.metrics import ams_hists_rebin

MyCut = namedtuple('MyCut', ['name', 'cut'])

inc_sig = inc_sig # & Cut('Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_goodVertices && Flag_eeBadScFilter && Flag_globalTightHalo2016Filter && passBadMuonFilter && passBadChargedHadronFilter && badMuonMoriond2017 && badCloneMuonMoriond2017')

def prepareCuts(mode):
    cuts = []

    # categories, do not include charge and iso cuts
    inc_cut = inc_sig
    jet1_cut = inc_sig & Cut(cat_J1)
    vbf_cut = inc_sig & Cut(cat_VBF)

    # append categories to plot
    if mode == 'control':
        # cuts.append(MyCut('inclusive', inc_cut & Cut('n_bjets==0')))
        # cuts.append(MyCut('dilpt50', inc_cut & Cut('n_bjets==0 && dil_pt>50')))

        cuts.append(MyCut('2bjet', inc_cut & Cut('n_bjets>=2')))
        cuts.append(MyCut('gr1bjet', inc_cut & Cut('n_bjets>=1')))

        # cuts.append(MyCut('sm_dysel_new_mz', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>50 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60. && mvis<100')))
        # cuts.append(MyCut('sm_dysel_ptgr100_mz', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>100 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60. && mvis<100')))

        # cuts.append(MyCut('sm_dysel_new', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>50 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_ptgr100', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>100 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_ptgr200', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>200 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_pt150_200', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>150 && l1_pt<200 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_pt100_150', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>100 && l1_pt<150 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_pt80_100', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>80 && l1_pt<100 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_pt50_80', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>50 && l1_pt<80 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))

        # cuts.append(MyCut('inclusive_SS', inc_cut))
        # cuts.append(MyCut('mZ', inc_cut & Cut('mvis < 110.')))
        # cuts.append(MyCut('low_deta', inc_cut & Cut('delta_eta_l1_l2 < 1.5')))
        # cuts.append(MyCut('high_deta', inc_cut & Cut('delta_eta_l1_l2 > 1.5')))

        # cuts.append(MyCut('mZ_0jet', inc_cut & Cut('mvis < 110. && n_jets==0')))
        # cuts.append(MyCut('mZ_1jet', inc_cut & Cut('mvis < 110. && n_jets>=1')))
        # Next is a failed attempt to get a W+jets-enriched control region
        # cuts.append(MyCut('mva_met_sig_1_low_deta', inc_cut & Cut('met_pt/sqrt(met_cov00 + met_cov11) > 1. && delta_eta_l1_l2 < 2.')))

    if mode == 'mssm':
        #cuts.append(MyCut('nobtag', inc_cut & Cut('n_bjets==0')))
        cuts.append(MyCut('inclusive', inc_cut & Cut('1')))
        #cuts.append(MyCut('btag', inc_cut & Cut('n_bjets>=1')))
        
        # cuts.append(MyCut('1bjet', inc_cut & Cut('n_bjets==1')))
        # # cuts.append(MyCut('0jet', inc_cut & Cut('n_bjets==1 && n_jets==0')))

        # # cuts.append(MyCut('inclusive_largedphi', inc_cut & Cut('n_bjets==0 && abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))>1.5')))
        # cuts.append(MyCut('inclusive_tau1pt60', inc_cut & Cut('n_bjets==0 && l1_pt>60')))
        # cuts.append(MyCut('inclusive_tau1ptl60', inc_cut & Cut('n_bjets==0 && l1_pt<60')))
        # cuts.append(MyCut('inclusive_tau1pt75', inc_cut & Cut('n_bjets==0 && l1_pt>75')))
        # cuts.append(MyCut('inclusive_tau1ptl75', inc_cut & Cut('n_bjets==0 && l1_pt<75')))
        # cuts.append(MyCut('inclusive_tau1pt100', inc_cut & Cut('n_bjets==0 && l1_pt>100')))
        # cuts.append(MyCut('inclusive_tau1ptl100', inc_cut & Cut('n_bjets==0 && l1_pt<100')))
        # cuts.append(MyCut('inclusive_tau1pt150', inc_cut & Cut('n_bjets==0 && l1_pt>150')))
        # cuts.append(MyCut('inclusive_tau1ptl150', inc_cut & Cut('n_bjets==0 && l1_pt<150')))
        # cuts.append(MyCut('inclusive_lowdphimetl2', inc_cut & Cut('n_bjets==0 && abs(TVector2::Phi_mpi_pi(l2_phi-met_phi))<0.5')))
        # cuts.append(MyCut('inclusive_lowdphimetl2_highdphimetl1', inc_cut & Cut('n_bjets==0 && abs(TVector2::Phi_mpi_pi(l2_phi-met_phi))<0.5 && abs(TVector2::Phi_mpi_pi(l1_phi-met_phi))>2')))
        
        # cuts.append(MyCut('inclusive_mttotal300', inc_cut & Cut('n_bjets==0 && mt_total>300')))


    if mode == 'sm':
        #cuts.append(MyCut('sm_1jet', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>50 && l2_pt>40')))
        #cuts.append(MyCut('sm_0jet', inc_cut & Cut('n_bjets==0 && n_jets==0 && l1_pt>50 && l2_pt>40')))
        cuts.append(MyCut('sm_1jet', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>23 && l2_pt>30')))
        cuts.append(MyCut('sm_0jet', inc_cut & Cut('n_bjets==0 && n_jets==0 && l1_pt>23 && l2_pt>30')))
        cuts.append(MyCut('1jet', jet1_cut)) # with VBF veto
        cuts.append(MyCut('vbf', vbf_cut))


    if mode == 'susy':
        # cuts.append(MyCut('mva_met_sig_3', inc_cut & Cut('met_pt/sqrt(met_cov00 + met_cov11) > 3.')))

        # cuts.append(MyCut('met200', inc_cut & Cut('met_pt > 200.')))


        # cuts.append(MyCut('susy_loose_met', inc_cut & Cut('mvis>100 && n_bjets==0 && met_pt>100.')))
        # cuts.append(MyCut('susy_loose', inc_cut & Cut('mvis>100 && n_bjets==0 && pzeta_disc < -40.')))

        # cuts.append(MyCut('susy_mtsum200', inc_cut & Cut('n_bjets==0 && mt + mt_leg2>200.')))
        # cuts.append(MyCut('susy_highmva', inc_cut & Cut('n_bjets==0 && mva1>0.75')))

        # cuts.append(MyCut('susy_mva_mtsum200_mt2_20', inc_cut & Cut('n_bjets==0 && mt2>20 && mt + mt_leg2>200. && mva1>0.85')))
        # cuts.append(MyCut('susy_mva2_mtsum200_mt2_20', inc_cut & Cut('n_bjets==0 && mt2>20 && mt + mt_leg2>200. && mva1>0.90')))
        # cuts.append(MyCut('susy_mva3_mtsum200_mt2_20', inc_cut & Cut('n_bjets==0 && mt2>20 && mt + mt_leg2>200. && mva1>0.95')))
        # cuts.append(MyCut('susy_mtsum200_mt2_20', inc_cut & Cut('n_bjets==0 && mt2>20 && mt + mt_leg2>200.')))

        # cuts.append(MyCut('pieter_1', inc_cut & Cut('n_bjets==0 && mt2>90. && abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))>1.5')))
        # cuts.append(MyCut('pieter_2', inc_cut & Cut('n_bjets==0 && mt2>40. && mt2<90. && mt2>40. && abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))>1.5 && mt + mt_leg2>300. && mt + mt_leg2<300. ')))
        # cuts.append(MyCut('pieter_3', inc_cut & Cut('n_bjets==0 && mt2>40. && mt2<90. && mt2>40. && abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))>1.5 && mt + mt_leg2>350.')))

        # cuts.append(MyCut('maryam_incl', inc_cut & Cut('n_bjets==0 && mt2>20. && mvis>85. && pfmet_pt>30.')))
        
        # cuts.append(MyCut('maryam_1', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30.')))
        # cuts.append(MyCut('maryam_1_0jet', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && n_jets==0')))
        # cuts.append(MyCut('maryam_1_1jet', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && n_jets>=1')))

        # cuts.append(MyCut('maryam_1_SS', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30.')))
        # cuts.append(MyCut('maryam_1_0jet_SS', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && n_jets==0')))
        # cuts.append(MyCut('maryam_1_1jet_SS', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && n_jets>=1')))


        cuts.append(MyCut('maryam_1_mt2sideband_1jet', inc_cut & Cut('n_bjets==0 && mt2>75. && mt2<90. && mvis>85. && pfmet_pt>30. && n_jets>=1')))
        cuts.append(MyCut('maryam_1_mt2sideband_1jet_SS', inc_cut & Cut('n_bjets==0 && mt2>75. && mt2<90. && mvis>85. && pfmet_pt>30. && n_jets>=1')))

        # cuts.append(MyCut('maryam_1_tight', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && l1_pt>100.')))
        # cuts.append(MyCut('maryam_1_tight_1jet', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && l1_pt>100. && n_jets>=1')))
        # cuts.append(MyCut('maryam_1_tight_0jet', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && l1_pt>100. && n_jets==0')))
        # cuts.append(MyCut('maryam_2', inc_cut & Cut('n_bjets==0 && mt2<90. && mvis>85. && pfmet_pt>30. && mt + mt_leg2 > 250. && l1_pt>100.')))

        # cuts.append(MyCut('susy_onlytaupt', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20.')))
        # cuts.append(MyCut('susy_taupt', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50.')))
        # cuts.append(MyCut('susy_taupt_pzetamet', inc_cut & Cut(
        #     'mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50. && pzeta_met<-50. && delta_eta_l1_l2<3. && (min(abs(TVector2::Phi_mpi_pi(met_phi - jet2_phi)) + 20*(jet2_phi<-50), abs(TVector2::Phi_mpi_pi(met_phi - jet1_phi))+ 20*(jet1_phi<-50)) > 0.8 || jet1_pt<30.)')))
        # cuts.append(MyCut('susy_jan_opt', inc_cut & Cut('met_pt/sqrt(met_cov00 + met_cov11) > 2. && mvis>100 && mt + mt_leg2 > 200. && n_bjets==0 && pzeta_disc < -40.')))
        # cuts.append(MyCut('susy_jan_tight', inc_cut & Cut(
        #     'met_pt/sqrt(met_cov00 + met_cov11) > 1. && mvis>100 && mt + mt_leg2 > 150. && n_bjets==0 && pzeta_disc < -40. && abs(abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))) > 1. && mt_total>300.')))

        # cuts.append(MyCut('susy_onlytaupt_0jet', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && n_jets==0')))
        # cuts.append(MyCut('susy_taupt_0jet', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50. && n_jets==0')))
        # cuts.append(MyCut('susy_taupt_pzetamet_0jet', inc_cut & Cut(
        #     'mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50. && pzeta_met<-50. && delta_eta_l1_l2<3. && (min(abs(TVector2::Phi_mpi_pi(met_phi - jet2_phi)) + 20*(jet2_phi<-50), abs(TVector2::Phi_mpi_pi(met_phi - jet1_phi))+ 20*(jet1_phi<-50)) > 0.8 || jet1_pt<30.) && n_jets==0')))
        # cuts.append(MyCut('susy_jan_opt_0jet', inc_cut & Cut('met_pt/sqrt(met_cov00 + met_cov11) > 2. && mvis>100 && mt + mt_leg2 > 200. && n_bjets==0 && pzeta_disc < -40. && n_jets==0')))
        # cuts.append(MyCut('susy_jan_tight_0jet', inc_cut & Cut(
        #     'met_pt/sqrt(met_cov00 + met_cov11) > 1. && mvis>100 && mt + mt_leg2 > 150. && n_bjets==0 && pzeta_disc < -40. && abs(abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))) > 1. && mt_total>300. && n_jets==0')))


        # cuts.append(MyCut('susy_onlytaupt_gr1jet', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && n_jets>0')))
        # cuts.append(MyCut('susy_taupt_gr1jet', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50. && n_jets>0')))
        # cuts.append(MyCut('susy_taupt_pzetamet_gr1jet', inc_cut & Cut(
        #     'mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50. && pzeta_met<-50. && delta_eta_l1_l2<3. && (min(abs(TVector2::Phi_mpi_pi(met_phi - jet2_phi)) + 20*(jet2_phi<-50), abs(TVector2::Phi_mpi_pi(met_phi - jet1_phi))+ 20*(jet1_phi<-50)) > 0.8 || jet1_pt<30.) && n_jets>0')))
        # cuts.append(MyCut('susy_jan_opt_gr1jet', inc_cut & Cut(
        #     'met_pt/sqrt(met_cov00 + met_cov11) > 2. && mvis>100 && mt + mt_leg2 > 200. && n_bjets==0 && pzeta_disc < -40. && n_jets>0')))
        # cuts.append(MyCut('susy_jan_tight_gr1jet', inc_cut & Cut(
        #     'met_pt/sqrt(met_cov00 + met_cov11) > 1. && mvis>100 && mt + mt_leg2 > 150. && n_bjets==0 && pzeta_disc < -40. && abs(abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))) > 1. && mt_total>300. && n_jets>0')))

        # cuts.append(MyCut('susy_jan_nomet', inc_cut & Cut('mvis>100 && n_bjets==0 && mt + mt_leg2 > 150.')))

    return cuts

    # if optimisation:
    #     cuts = []
    #     met_sig_cuts = [2, 3]
    #     # met_sig_cuts = [1]
    #     sum_mt_cuts = [0, 50, 100, 150, 200, 250]
    #     # pzeta_disc_cuts = [-40, 0, 1000]
    #     pzeta_disc_cuts = [-40, 1000]

    #     for met_sig_cut in met_sig_cuts:
    #         for sum_mt_cut in sum_mt_cuts:
    #             for pzeta_cut in pzeta_disc_cuts:
    #                 cut_name = 'susy_jan_{c1}_{c2}_{c3}'.format(c1=met_sig_cut, c2=sum_mt_cut, c3=pzeta_cut)
    #                 cut = 'met_pt/sqrt(met_cov00 + met_cov11) > {met_sig_cut} && mvis>100 && mt + mt_leg2 > {sum_mt_cut} && n_bjets==0 && pzeta_disc < {pzeta_disc_cut}'.format(met_sig_cut=met_sig_cut, sum_mt_cut=sum_mt_cut, pzeta_disc_cut=pzeta_cut)
    #                 cuts.append(MyCut(cut_name, inc_cut & cut))


    # cuts.append(MyCut('susy_jan_SS', inc_cut & Cut('met_pt/sqrt(met_cov00 + met_cov11) > 1. && mvis>100 && mt + mt_leg2 > 150. && n_bjets==0 && pzeta_disc < -40.')))

    

def getVariables(mode):
    # Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
    # variables = taumu_vars
    if mode == 'control':
        variables = getVars(['_norm_', 'mvis', 'mt2', 'l1_pt', 'l2_pt', 'delta_phi_l1_l2', 'delta_eta_l1_l2', 'met_pt', 'mt_total', 'mt_total_mssm', 'mt_sum', 'pzeta_met', 'l2_mt', 'mt', 'pzeta_vis', 'pzeta_disc', 'pthiggs', 'jet1_pt', 'n_jets', 'dil_pt', 'l1_byCombinedIsolationDeltaBetaCorrRaw3Hits', 'l1_byIsolationMVArun2v1DBoldDMwLTraw', 'l1_dz_sig', 'l1_log_dz', 'l1_dxy_sig', 'l1_log_dxy', 'l1_decayMode', 'l1_chargedIsoPtSum', 'l1_neutralIsoPtSum', 'l1_puCorrPtSum', 'l1_photonPtSumOutsideSignalCone', 'l1_zImpact', 'l1_jet_charge', 'l1_jet_pt_div_l1_pt'], channel='taumu')
    if mode == 'mssm':
        # variables = getVars(['mt_total', 'mt_total_mssm', 'mt_total_mssm_fine', 'mvis_extended', 'l1_pt', 'dil_pt'], channel='taumu')
        variables = getVars(['mt_total_mssm_fine'], channel='taumu')#, 'mt_total_mssm''mt_total_mssm', 
        from numpy import array
        binning_mttotal_fine = array([0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200., 225., 250., 275., 300., 325., 350., 400., 500., 700., 900., 1100., 1300., 1500., 1700., 1900., 2100., 2300., 2500., 2700., 2900., 3100., 3300., 3500., 3700., 3900.])
        binning_mttotal_fine = array([0., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200., 225., 250., 275., 300., 325., 350., 400., 500.])
        variables = [VariableCfg(name='mt_total_mssm_fine', drawname='mt_total', binning=binning_mttotal_fine, unit='GeV', xtitle='M_{T}^{total}')]
    # variables += [
    #     VariableCfg(name='mt2', binning={'nbinsx':15, 'xmin':0., 'xmax':150.}, unit='GeV', xtitle='m_{T2}')
    # ]
    if mode == 'mva':
        variables += getVars(['_norm_'])
        variables += [
            VariableCfg(name='mva1', binning={'nbinsx':10, 'xmin':0., 'xmax':1.}, unit='', xtitle='Stau MVA')
        ]

    if mode == 'susy':
        variables = getVars(['l1_pt', '_norm_', 'l2_pt', 'mt2', 'mt', 'mt_leg2', 'mt_total_mssm', 'min_delta_phi_tau1tau2_met'], channel='taumu')

    return variables



def createSamples(mode, analysis_dir, optimisation=False):
    samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(
        analysis_dir = analysis_dir,
        channel = 'mt',
        mode = mode,
        ztt_cut = '(l2_gen_match == 5)',
        zl_cut = '(l2_gen_match < 5)',
        zj_cut = '(l2_gen_match == 6)',
        signal_scale=1. if optimisation else 20.
        )
    # import pdb;pdb.set_trace()
    # all_samples = [s for s in all_samples if s.name not in ['WZJToLLLNu_J','WZJToLLLNu','WZJToLLLNu_T','WZTo1L3Nu_J','WZTo1L3Nu_T','WZTo1L3Nu']]#'TTT','TTJ','TT','data_obs']]
    # samples = [s for s in samples if s.name not in ['WZJToLLLNu_J','WZJToLLLNu','WZJToLLLNu_T','WZTo1L3Nu_J','WZTo1L3Nu_T','WZTo1L3Nu']]#['TTT','TTJ','TT','data_obs']]
    return all_samples, samples


def makePlots(variables, cuts, total_weight, all_samples, samples, friend_func, mode='control', dc_postfix='', make_plots=True, optimisation=False):
    sample_names = set()
    ams_dict = {}

    from CMGTools.H2TauTau.proto.plotter.cut import Cut

    # def_iso_cut = inc_sig_tau1_iso & inc_sig_tau2_iso
    iso_cuts = {
        # 'vvtight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>5.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>5.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>3.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>3.5')),
        # 'vtight_relax2nd':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>2.5')),
        # 'loose_not_vtight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>1.5 && l1_byIsolationMVArun2v1DBoldDMwLT<4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>1.5&&l2_byIsolationMVArun2v1DBoldDMwLT<4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT<1.5 && l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT<1.5 && l2_byIsolationMVArun2v1DBoldDMwLT>0.5')),
        # 'one_loose_other_vtight':(Cut('(l1_byIsolationMVArun2v1DBoldDMwLT>4.5 && (l2_byIsolationMVArun2v1DBoldDMwLT>1.5&&l2_byIsolationMVArun2v1DBoldDMwLT<4.5)) || (l2_byIsolationMVArun2v1DBoldDMwLT>4.5 && (l1_byIsolationMVArun2v1DBoldDMwLT>1.5&&l1_byIsolationMVArun2v1DBoldDMwLT<4.5)) '), Cut('l1_byIsolationMVArun2v1DBoldDMwLT<1.5 && l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT<1.5 && l2_byIsolationMVArun2v1DBoldDMwLT>0.5')),
        # 'vtight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>2.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>2.5')),
        # 'tight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>3.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>3.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>3.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>1.5')),
        'medium':(Cut('l2_byIsolationMVArun2v1DBoldDMwLT>2.5'), Cut('l2_byIsolationMVArun2v1DBoldDMwLT>0.5')),
        # 'loose':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>1.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>1.5'), Cut('1')),
        # 'vloose':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>0.5'), Cut('1')),
    }

    # iso_cuts = {
    #     'l1_vvtight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>5.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>5.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>3.5')),
    #     'l1_vtight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>2.5')),
    #     'l1_tight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>3.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>3.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>1.5')),
    #     'l1_medium':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>2.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>2.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>0.5')),
    #     'l1_loose':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>1.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>1.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>0.5')),
    #     'l1_vloose':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'),Cut('l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('1')),
    # }

    for cut in cuts:
        for iso_cut_name, (iso_cut, max_iso_cut) in iso_cuts.items():
            
            # iso and charge cuts, need to have them explicitly for the QCD estimation
            # max_iso_cut = Cut('l1_byIsolationMVArun2v1DBoldDMwLT > 2.5 && l2_byIsolationMVArun2v1DBoldDMwLT > 2.5')
            iso_sideband_cut = (~iso_cut) & max_iso_cut
            OS_cut = Cut('l1_charge != l2_charge')
            SS_cut = ~OS_cut
            # all_samples_qcd = qcd_estimation(
            #     cut.cut & iso_cut          & SS_cut,  # shape sideband
            #     cut.cut & iso_sideband_cut & OS_cut,  # norm sideband 1
            #     cut.cut & iso_sideband_cut & SS_cut,  # norm sideband 2
            #     all_samples if mode in ['mssm'] else samples,
            #     int_lumi,
            #     total_weight,
            #     verbose=verbose,
            #     friend_func=friend_func
            # )
            all_samples_qcd = all_samples

            # now include charge and isolation too
            isSS = 'SS' in cut.name
            the_cut = MyCut(cut.name+iso_cut_name, cut.cut & iso_cut & (OS_cut if not isSS else SS_cut))

            
            # all_samples_qcd = jetFakesEstimation(all_samples,
            #                                      cut.cut & charge_cut,
            #                                      int_lumi,
            #                                      total_weight)

            # for variable in variables:
            cfg_total = HistogramCfg(name=the_cut.name, vars=variables, cfgs=all_samples_qcd, cut=str(the_cut.cut), lumi=int_lumi, weight=total_weight)
            # all_samples_qcd[-1].vars = variables

            if mode == 'mva_train':
                #createTrees(cfg_total, '/data1/steggema/tt/MVATrees', verbose=True)
                continue

            plots = createHistograms(cfg_total, verbose=True, friend_func=friend_func)

            for variable in variables:
                plot = plots[variable.name]
                plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'])  # 'TToLeptons_sch',
                plot.Group('VV', ['VVTo2L2Nu', 'ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L',  'WZTo2L2Q', 'WZTo1L1Nu2Q', 'Single t', 'VVTo2L2Nu_ext', 'WZJToLLLNu'])  # 'WZTo3L',
                plot.Group('Single t T', ['T_tWch_T', 'TBar_tWch_T', 'TToLeptons_tch_powheg_T', 'TBarToLeptons_tch_powheg_T'])
                plot.Group('Single t J', ['T_tWch_J', 'TBar_tWch_J', 'TToLeptons_tch_powheg_J', 'TBarToLeptons_tch_powheg_J'])
                plot.Group('VVT', ['VVTo2L2Nu_T', 'ZZTo2L2Q_T', 'WWTo1L1Nu2Q_T', 'WZTo1L3Nu_T', 'ZZTo4L_T',  'WZTo2L2Q_T', 'WZTo1L1Nu2Q_T', 'Single t T', 'VVTo2L2Nu_ext_T', 'WZJToLLLNu_T'])
                plot.Group('VVJ', ['VVTo2L2Nu_J', 'ZZTo2L2Q_J', 'WWTo1L1Nu2Q_J', 'WZTo1L3Nu_J', 'ZZTo4L_J',  'WZTo2L2Q_J', 'WZTo1L1Nu2Q_J', 'Single t J', 'VVTo2L2Nu_ext_J', 'WZJToLLLNu_J'])
                plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets','ZTT_10_50'])
                plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets','ZJ_10_50'])
                plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets','ZL_10_50'])
                plot.Group('ZLL', ['ZLL', 'ZLL1Jets', 'ZLL2Jets', 'ZLL3Jets', 'ZLL4Jets','ZLL_10_50'])
                plot.Group('W', ['WJets', 'WJets_ext', 'W1Jets', 'W2Jets_ext', 'W2Jets', 'W3Jets_ext', 'W3Jets', 'W4Jets', 'W4Jets_ext', 'W4Jets_ext2'])
                plot.Group('jetFakes', ['jetFakes_direct','jetFakes_tosubstract'])
                # plot.Group('jetFakes',['JetFakes1','JetFakes2','JetFakes3','JetFakes4','JetFakes5','JetFakes6','JetFakes7','JetFakes8'])
                # plot.Group('Electroweak', ['W', 'VV', 'Single t', 'ZJ'])

                if optimisation:
                    plot.DrawStack('HIST')
                    print plot
                    for signal_hist in plot.SignalHists():
                        sample_names.add(signal_hist.name)
                        ams = ams_hists_rebin(signal_hist.weighted, plot.BGHist().weighted)
                        if variable.name == 'mt_total_mssm' and signal_hist.name == 'ggH1800':
                            print ams_hists_rebin(signal_hist.weighted, plot.BGHist().weighted, debug=True)
                            # import pdb; pdb.set_trace()
                        ams_dict[variable.name + '__' + the_cut.name + '__' + signal_hist.name + '_'] = ams
                
                if not make_plots:
                    continue

                blindxmin = 0.7 if 'mva' in variable.name else None
                blindxmax = 1.00001 if 'mva' in variable.name else None

                if variable.name == 'mt2':
                    blindxmin = 60.
                    blindxmax = variable.binning['xmax']

                if variable.name == 'mt_sum':
                    blindxmin = 250.
                    blindxmax = variable.binning['xmax']

                if variable.name == 'mt_total':
                    blindxmin = 200.
                    blindxmax = variable.binning['xmax']
                plot_dir = 'plot_' + the_cut.name
                HistDrawer.draw(plot, channel='#mu#tau_{h}', plot_dir=plot_dir, blindxmin=blindxmin, blindxmax=blindxmax)
                # HistDrawer.drawRatio(plot, channel='#tau_{h}#tau_{h}')

                # plot.UnGroup('Electroweak')#, ['W', 'VV', 'Single t', 'ZJ'])
                # plot.Group('VV', ['VV', 'Single t'])
                if variable.name in ['mt_total', 'svfit_mass', 'mt_total_mssm', 'mt_total_mssm_fine']:
                    plot.WriteDataCard(filename=plot_dir+'/htt_tt.inputs-sm-13TeV_{var}{postfix}.root'.format(var=variable.name, postfix=dc_postfix), dir='mt_' + cut.name, mode='RECREATE')

            # Save AMS dict
            import pickle
            pickle.dump(ams_dict, open('opt.pkl', 'wb'))
            

    if optimisation:
        print '\nOptimisation results:'
        all_vals = ams_dict.items()
        for sample_name in sample_names:
            vals = [v for v in all_vals if sample_name + '_' in v[0]]
            vals.sort(key=itemgetter(1))
            for key, item in vals:
                print item, key

            print '\nBy variable'
            for variable in variables:
                name = variable.name
                print '\nResults for variable', name
                for key, item in vals:
                    if key.startswith(name + '__'):
                        print item, key


if __name__ == '__main__':
    mode = 'mssm' # 'control' 'mssm' 'mva_train' 'susy' 'sm'

    int_lumi = lumi
    analysis_dir = '/eos/user/l/ltortero/Prod/Samples_v1/'
    verbose = True
    total_weight = 'weight'

    import os
    from ROOT import gSystem, gROOT
    # if "/sHTTEfficiencies_cc.so" not in gSystem.GetLibraries(): 
    #     gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/HTTEfficiencies.cc+" % os.environ['CMSSW_BASE']);
    gSystem.Load("libCMGToolsH2TauTau")
    from ROOT import getTauWeight

    if "/sFakeFactor_cc.so" not in gSystem.GetLibraries(): 
        gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/FakeFactor.cc+" % os.environ['CMSSW_BASE']);
        from ROOT import getFFWeight

    total_weight = 'weight' # 'weight*getTauWeight(l2_gen_match, l2_pt, l2_eta, l2_decayMode,1,2,3)'

    optimisation = False
    make_plots = True

    # Check whether friend trees need to be added
    friend_func = None
    if mode == 'mva':
        # friend_func = lambda f: f.replace('MC', 'MCMVAmt200')
        friend_func = lambda f: f.replace('MC', 'MCMVAmt200_7Vars')

    cuts = prepareCuts(mode)
    all_samples, samples = createSamples(mode, analysis_dir, optimisation)
    ########### Lucas debug internship
    selected_all_samples_to_plot = []
    samples_to_ignore = ['DYJetsToLL_M10to50_LO', 'DYJetsToLL_M50_LO_ext', 'DYJetsToLL_M50_LO_ext2', 'WJetsToLNu_LO', 'WJetsToLNu_LO_ext','data_single_muon_1', 'data_single_muon_2', 'data_single_muon_3']
    for sample in all_samples:
        if sample.dir_name in os.listdir(analysis_dir) and sample.dir_name not in samples_to_ignore:
            selected_all_samples_to_plot.append(sample)
    all_samples = selected_all_samples_to_plot
    selected_samples_to_plot = []
    for sample in samples:
        if sample.dir_name in os.listdir(analysis_dir) and sample.dir_name not in samples_to_ignore:
            selected_samples_to_plot.append(sample)
    samples = selected_samples_to_plot
    ###########
    variables = getVariables(mode)
    makePlots(variables, cuts, total_weight, all_samples, samples, friend_func, mode=mode, optimisation=optimisation)
