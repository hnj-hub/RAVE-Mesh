# ArcherPre mesh generation script
# Load step -> tetrahedral mesh -> check elements -> export BDF

model_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i25o_s40.step"
bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/full/i25o_s40/mesh.bdf"

# 1. Load geometry
app.process({"action": "loadModel", "fileName": model_path, "module": "iomanager"})
print("Model loaded.")

# 2. Enter solid mesher, select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("Entered solid mesher, all parts selected.")

# 3. Generate tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 3.0, "growthRatio": 1.3, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}
}})
print("Meshing complete.")

# 4. Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
print("Left solid mesher.")

# 5. Verify element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("Element count:", n)

if n == 0:
    print("FAIL: No elements generated. Will not export.")
else:
    # 6. Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output(bdf_path)
    print("BDF export return code:", ret)
    if ret == 0:
        print("BDF exported to:", bdf_path)
    else:
        print("FAIL: BDF export returned non-zero:", ret)

print("Done!")