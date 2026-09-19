# ArcherPre mesh script for i29o_bracket.step
# Tetrahedral mesh -> Nastran BDF

# Step 1: Load geometry
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i29o_bracket.step", "module": "iomanager"})

# Step 2: Enter solid mesher and select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Step 3: Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 4.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}
}})

# Step 4: Leave mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Step 5: Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # Step 6: Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/full/i29o_bracket/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("Done!")