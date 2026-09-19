# ArcherPre mesh script: tetrahedral mesh for i24o_s34.step -> BDF
# Uses forward-slashed paths for ArcherPre compatibility
import sys

model_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i24o_s34.step"
bdf_output_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i24o_s34/mesh.bdf"

# Step 1: Load geometry
app.process({"action": "loadModel", "fileName": model_path, "module": "iomanager"})
print("Step 1: Model loaded.")

# Step 2: Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
print("Step 2: Entered solidmesher.")

# Step 3: Select all parts (entityType 1 = solid)
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("Step 3: Selected all solids.")

# Step 4: Tetrahedral mesh with reasonable sizes
app.process({
    "action": "mesh",
    "module": "solidmesher",
    "meshSetting": {
        "meshType": "tetmesh",
        "curveMesh": {"alignment": 1, "refinementAngle": 45.0, "enableProximity": 1},
        "surfaceMesh": {"elemType": "ETri", "meshSize": 3.0, "growthRatio": 1.2, "sizePriority": 1, "adaptiveCurvature": 1},
        "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}
    }
})
print("Step 4: Mesh command issued.")

# Step 5: Leave mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
print("Step 5: Left solidmesher.")

# Step 6: Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("Element count:", n)

if n == 0:
    print("FAIL: No elements generated. Skipping BDF export.")
    sys.exit(1)

# Step 7: Export BDF
from arcore.ar_io import ar_io
ret = ar_io.mesh_bdf_output(bdf_output_path)
print("BDF export return value:", ret)

# Step 8: Quick validation - check file exists and has content
import os
size = os.path.getsize(bdf_output_path)
print("BDF file size:", size, "bytes")

# Read first few lines to check for GRID and CTETRA
with open(bdf_output_path, "r") as f:
    content = f.read()

has_grid = "GRID" in content
has_ctetra = "CTETRA" in content

print("Contains GRID:", has_grid)
print("Contains CTETRA:", has_ctetra)

if size > 0 and has_grid and has_ctetra:
    print("SUCCESS: BDF validation passed.")
else:
    print("FAIL: BDF validation failed.")
    sys.exit(1)