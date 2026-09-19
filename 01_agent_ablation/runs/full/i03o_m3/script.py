# ArcherPre tet mesh generation script
# Load STEP model, generate tetrahedral mesh, export BDF

# 1. Load model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i03o_m3.step", "module": "iomanager"})
print("Step 1: Model loaded")

# 2. Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
print("Step 2: Entered solidmesher")

# 3. Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("Step 3: Selected all")

# 4. Tetrahedral mesh with reasonable parameters
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 8.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 16.0}
}})
print("Step 4: Mesh command issued")

# 5. Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
print("Step 5: Left solidmesher")

# 6. Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数 (total elements):", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # 7. Export BDF
    from arcore.ar_io import ar_io
    out_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/full/i03o_m3/mesh.bdf"
    ret = ar_io.mesh_bdf_output(out_path)
    print("BDF导出返回值 (export retcode):", ret)
    print("导出路径 (output path):", out_path)
    if ret == 0:
        print("BDF file written successfully")
    else:
        print("WARNING: BDF export returned non-zero")

print("Done!")