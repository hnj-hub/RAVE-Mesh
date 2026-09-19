# -*- coding: utf-8 -*-
"""Generate tetrahedral mesh for i02o_m2.step and export BDF."""
import sys
from arcore.ar_io import ar_io

model_file = r"D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i02o_m2.step"
bdf_path = r"D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i02o_m2/mesh.bdf"

# Load STEP model
app.process({"action": "loadModel", "fileName": model_file, "module": "iomanager"})

# Enter parts module for meshing
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# Select entire part
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Generate tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.4, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 12.0}
}})

# Leave parts module
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Query element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print(f"单元总数: {n}")

if n == 0:
    print("FAIL: 网格未生成任何单元")
    sys.exit(1)

# Export BDF
ret = ar_io.mesh_bdf_output(bdf_path)
print(f"BDF 导出返回值: {ret}")

if ret != 0:
    print(f"FAIL: BDF 导出失败,返回值={ret}")
    sys.exit(1)

print("SUCCESS: 网格剖分完成, BDF 已导出")