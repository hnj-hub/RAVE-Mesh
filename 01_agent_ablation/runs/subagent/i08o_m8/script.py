# ArcherPre mesh script for i08o_m8.step
# Tetrahedral mesh -> BDF export

MODEL_PATH = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i08o_m8.step"
BDF_PATH = "D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i08o_m8/mesh.bdf"

# Step 1: Load the STEP model
app.process({"action": "loadModel", "fileName": MODEL_PATH, "module": "iomanager"})
print("Model loaded.")

# Step 2: Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
print("Entered solidmesher.")

# Step 3: Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("All parts selected.")

# Step 4: Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 8.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 16.0}
}})
print("Meshing done.")

# Step 5: Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
print("Left solidmesher.")

# Step 6: Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("Total element count:", n)

# Step 7: Export BDF only if elements > 0
if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output(BDF_PATH)
    print("BDF export return code:", ret)
    print("BDF exported to:", BDF_PATH)
else:
    print("FAIL: No elements generated — mesh likely empty. Skipping BDF export.")