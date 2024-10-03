# standard weak formulation: backward, forward euler + crank-nicolson
python -m main -cf "weak" -fs "CG" -fso 1 -th 1.0 || true
python -m main -cf "weak" -fs "CG" -fso 1 -th 0.5  || true
python -m main -cf "weak" -fs "CG" -fso 1 -th 0.0  || true
# stabilized schemes backward euler
python -m main -cf "weak" -fs "CG" -fso 1 -stab "iad" || true
python -m main -cf "weak" -fs "CG" -fso 1 -stab "su" || true
python -m main -cf "prod" -fs "CG" -fso 1 -stab "supg" || true
python -m main -cf "weak" -fs "CG" -fso 1 -stab "tg" || true
python -m main -cf "prod" -s 0 -fs "DG" -fso 1 -stab "dgu" || true
# stabilized schemes crank nicolson
python -m main -cf "weak" -fs "CG" -fso 1 -stab "iad" -th 0.5  || true
python -m main -cf "weak" -fs "CG" -fso 1 -stab "su" -th 0.5  || true
python -m main -cf "prod" -fs "CG" -fso 1 -stab "supg" -th 0.5  || true
python -m main -cf "weak" -fs "CG" -fso 1 -stab "tg" -th 0.5  || true
python -m main -cf "prod" -s 0 -fs "DG" -fso 1 -stab "dgu" -th 0.5  || true
# stabilized schemes forward euler
python -m main -cf "weak" -fs "CG" -fso 1 -stab "iad" -th 0.0  || true
python -m main -cf "weak" -fs "CG" -fso 1 -stab "su" -th 0.0  || true
python -m main -cf "prod" -fs "CG" -fso 1 -stab "supg" -th 0.0  || true
python -m main -cf "weak" -fs "CG" -fso 1 -stab "tg" -th 0.0  || true
python -m main -cf "prod" -s 0 -fs "DG" -fso 1 -stab "dgu" -th 0.0  || true