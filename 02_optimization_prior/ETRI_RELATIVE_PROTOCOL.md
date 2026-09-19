# ETri relative-size main experiment

## Failure handling

RUNNER_ERROR is an infrastructure incident, not an objective observation.
The runner writes it to infrastructure_errors.jsonl and stops the affected
unit before appending to trials.jsonl or training the surrogate. It does not
consume an optimization evaluation. Repair the environment before resuming;
automatic retries are deliberately disabled for undiagnosed runner errors.
Resuming legacy history containing RUNNER_ERROR is rejected: restart that
affected unit in a clean output directory, retaining the old files for audit.

Actual mesh failures remain infeasible with objective penalty [1,1,1] and
consume one evaluation. An exported BDF is required for every evaluation.
The independent validator requires GRID and CTETRA records, valid node
references, four distinct corner nodes, no duplicate tetrahedra, positive
scale-normalized volume, manifold face incidence, and a closed manifold
boundary. A failed export or parser failure is a RUNNER_ERROR because no
parameter-dependent mesh observation was obtained. `total_elems` and
`tet_count` are recorded as mesh-size/cost descriptors; there is no universal
150-element feasibility cutoff. TIMEOUT retains the
predefined 90-second evaluation-budget rule and is penalized likewise; do not
reclassify timeouts based on whether the resulting comparison looks favorable.
Confirmed infrastructure incidents require separate auditing. The reference
point [1,1,1] gives penalty points zero additional hypervolume. Failure rounds
remain on the time axis: cumulative HV carries forward its previous value.

Entry: `config.a0_a0prime_etri_relative.json`; the validity-v2 output directory
is independent of all earlier runs, whose observations lack the new checks.
Four continuous coordinates: `surface_size_ratio` alpha in [0.02,0.10],
`growth_ratio` in [1.05,1.50], `refinement_angle` in [15,60] degrees,
`tet_size_ratio` k in [1,4]. Three binary coordinates remain unchanged:
`curvature`, `fastaft` (forceAFT), `conformal`. ETri is fixed outside the search space.
The resulting GP input has 7 dimensions and 8 discrete combinations.

Immediately before CAE evaluation, compute h_s=alpha*L and h_t_max=k*h_s.
L is the diagonal of the union of imported CAD solid bounding boxes (surfaces
when no solids exist). Gmsh/OpenCASCADE imports the CAD and queries its AABB;
STEP control-point extents are not used. Bounds include CAD-kernel tolerance.
Confirm imported length units agree with Archer before a full production run.
The search parameters, dimensional parameters, CAD bounds and Gmsh version are
stored in each trial JSON and trials.jsonl. Old absolute-size configs retain
their old interpretation. Resuming a changed search space is rejected.

The six CAD models, seeds 11/12/13, 20-evaluation budgets, quality objectives,
binary switch implementation and paired warmup logic are retained from the
main confirmatory configuration. All six Random/ParEGO/native-qLogEHVI A0/A0-prime
arms must run in the new space: legacy baseline results cannot be reused.
A0-prime uses six newly generated geometry-only defaults, not clipped old seeds.
Request/response provenance is in `config.a0_a0prime_etri_relative.defaults-audit.json`.

Install `requirements-relative.txt` in the existing optimizer Python environment.
The existing NumPy/SciPy/scikit-learn and qLogEHVI/PyTorch dependencies are also
required. Launch from PowerShell:

```powershell
.\run_etri_relative.ps1 -Python 'path\to\optimizer\python.exe'
```

The launcher defaults to one worker; `-ParallelWorkers 8` restores the configured
parallelism and requires the existing fused-kernel setup. It sets ARCHER_DIR to
the supplied installation. No full experiment is launched by installing/editing.

To regenerate defaults explicitly (changes the intervention, use a new result
directory if runs already exist), put the experiment `src` and my-agent `src`
on PYTHONPATH, then run:

```text
python -m mesh_optimization.derive_relative_defaults --config config.a0_a0prime_etri_relative.json
```

Matching audited responses are reused. Invalid/out-of-domain responses are
rejected, not silently clamped. All six seeds are committed together.
