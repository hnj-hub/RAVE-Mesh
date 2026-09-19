# -*- coding: utf-8 -*-
"""Generate tetrahedral mesh for s12o_cube_rounded_1.stp -> mesh.bdf"""

import os
import sys

# ── 1. load geometry ──────────────────────────────────────────────
model_path = r"D:\新建文件夹\my-agent\evals_p0_1_agent\models_40\s12o_cube_rounded_1.stp"
app.loadModel(model_path, fileName=model_path)

# ── 2. set meshing parameters ─────────────────────────────────────
meshSize = 4.0          # base element size
growthRatio = 1.2       # growth ratio
refinementAngle = 45.0  # refinement angle (degrees)
meshSizeMax = 8.0       # max element size

# ── 3. mesh generation ────────────────────────────────────────────
app.process((
    f'meshSize={meshSize}',
    f'growthRatio={growthRatio}',
    f'refinementAngle={refinementAngle}',
    f'meshSizeMax={meshSizeMax}',
    'meshType=3',       # tetrahedral mesh
))

# ── 4. export BDF ─────────────────────────────────────────────────
out_dir = r"D:\新建文件夹\my-agent\evals_p0_1_agent\skill\s12o_cube_rounded_1"
out_path = os.path.join(out_dir, "mesh.bdf")
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

app.meshExportBDF(out_path, version="new")
print(f"[OK] BDF exported to {out_path}")