### Hadronic taus IDs weight (including electron to tau fake weight and muon to tau fake weight)

# Tables -----------------------------
# in the form IDweights[gen_match] gives
# a dict which keys are WP that gives then
# the form (etamax, value)

IDWeights = {
    'EToTau' : {
        'VLoose' : [ (99, 1.38),
                     (1.5, 1.21) ],
        'Loose' : [ (99, 1.38),
                    (1.5, 1.32) ],
        'Medium' : [ (99, 1.53),
                     (1.5, 1.32) ],
        'Tight' : [ (99, 1.90),
                    (1.5, 1.40) ],
        'VTight' : [ (99, 1.97),
                     (1.5, 1.21) ],
        },
    'MuToTau' : {
        'Loose' : [ (99, 1.),
                    (2.3, 2.39),
                    (1.7, 1.22),
                    (1.2, 1.26),
                    (0.8, 1.12),
                    (0.4, 1.22) ],
        'Tight' : [ (99, 1.),
                    (2.3, 2.50),
                    (1.7, 1.72),
                    (1.2, 1.33),
                    (0.8, 1.55),
                    (0.4, 1.47) ],
        },
    'TauID' : {
        'VLoose' : [ (99, 0.99) ],
        'Loose' : [ (99, 0.99) ],
        'Medium' : [ (99, 0.97) ],
        'Tight' : [ (99, 0.95) ],
        'VTight' : [ (99, 0.93) ],
        }}
