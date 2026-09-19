#!/usr/bin/env python
"""Generate tetrahedral mesh for n10o_qtorus_cyl.step and export BDF."""

import sys

# 1. Load the STEP model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/n10o_qtorus_cyl.step", "module": "iomanager"})

# 2. Enter solid mesher, select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 3. Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})

# 4. Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 5. Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
    sys.exit(1)

# 6. Export BDF
from arcore.ar_io import ar_io
ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/full/n10o_qtorus_cyl/mesh.bdf")
print("BDF 导出返回值:", ret)

# 7. Validate the BDF file
import os
bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/full/n10o_qtorus_cyl/mesh.bdf"
if os.path.exists(bdf_path):
    size = os.path.getsize(bdf_path)
    print("BDF 文件大小:", size, "bytes")
    with open(bdf_path, "r") as f:
        content = f.read()
    grid_count = content.count("GRID")
    ctetra_count = content.count("CTETRA")
    print("GRID 卡数量:", grid_count)
    print("CTETRA 卡数量:", ctetra_count)
    if grid_count > 0 and ctetra_count > 0:
        print("SUCCESS: BDF 包含 GRID 和 CTETRA,网格有效")
    else:
        print("FAIL: BDF 缺少 GRID 或 CTETRA")
        sys.exit(1)
else:
    print("FAIL: BDF 文件未生成")
    sys.exit(1)