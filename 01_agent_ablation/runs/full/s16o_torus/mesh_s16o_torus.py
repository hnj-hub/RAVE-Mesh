# ArcherPre mesh script: s16o_torus.stp -> tetrahedral mesh -> BDF
# Torus: major radius 20mm, minor radius 5mm

# 1. Load STEP geometry
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s16o_torus.stp", "module": "iomanager"})

# 2. Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# 3. Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 4. Tetrahedral mesh (fine enough for a torus with small cross-section)
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 30.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 2.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 5.0}
}})

# 5. Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 6. Verify element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数 (Element count):", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # 7. Export BDF
    from arcore.ar_io import ar_io
    out_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/full/s16o_torus/mesh.bdf"
    ret = ar_io.mesh_bdf_output(out_path)
    print("BDF 导出返回值:", ret)
    print("Done!")