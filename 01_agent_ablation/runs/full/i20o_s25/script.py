# Step 1: Load the STEP model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i20o_s25.step", "module": "iomanager"})

# Step 2: Enter solid mesher and select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Step 3: Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})

# Step 4: Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Step 5: Check total element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    # Step 6: Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/full/i20o_s25/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("BDF 导出完成")
else:
    print("FAIL: 网格未生成任何单元,不导出")