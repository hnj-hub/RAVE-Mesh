"""Generate tetrahedral mesh for i03o_m3.step and export to BDF."""
from arcore.ar_io import ar_io
import os

step_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i03o_m3.step"
bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i03o_m3/mesh.bdf"

print("=== 1. Load model ===")
app.process({"action": "loadModel", "fileName": step_path, "module": "iomanager"})

print("=== 2. Enter solid mesher ===")
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

print("=== 3. Select all parts ===")
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

print("=== 4. Generate tetrahedral mesh ===")
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})

print("=== 5. Leave solid mesher ===")
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

print("=== 6. Export BDF ===")
ret = ar_io.mesh_bdf_output(bdf_path)
print("BDF export returned:", ret, "->", bdf_path)

# Verify file exists
if os.path.exists(bdf_path):
    size = os.path.getsize(bdf_path)
    print("BDF file size:", size, "bytes")
else:
    print("ERROR: BDF file was not created!")