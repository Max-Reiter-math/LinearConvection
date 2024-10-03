# standard weak formulation: backward, forward euler + crank-nicolson
python -m main -cf "weak" -fs "DG" -fso 0 -stab "dgu" || true
python -m main -cf "weak" -fs "DG" -fso 1 -stab "dgu" || true
python -m main -cf "weak" -fs "DG" -fso 2 -stab "dgu" || true
python -m main -cf "weak" -fs "CG" -fso 1 -stab "iad" || true
python -m main -cf "weak" -fs "CG" -fso 1 -stab "su" || true
python -m main -cf "prod" -fs "CG" -fso 1 -stab "supg" || true
python -m main -cf "weak" -fs "CG" -fso 1 -stab "tg" || true
python -m main -cf "weak" -fs "CG" -fso 1 || true
python -m main -cf "weak" -fs "CG" -fso 2 || true
python -m main -cf "weak" -fs "CG" -fso 1 -th 0.5 || true
python -m main -cf "weak" -fs "CG" -fso 2 -th 0.5 || true
python -m main -cf "weak" -fs "CG" -fso 1 -th 0.0 || true
python -m main -cf "weak" -fs "CG" -fso 2 -th 0.0 || true