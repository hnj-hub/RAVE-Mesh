# Step 1: Load geometry
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/n10o_qtorus_cyl.step", "module": "iomanager"})

# Step 2: Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# Step 3: Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Step 4: Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 15.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 30.0}
}})

# Step 5: Leave mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Step 6: Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

# Step 7: Export BDF if elements exist
if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/n10o_qtorus_cyl/mesh.bdf")
    print("BDF 导出返回值:", ret)
else:
    print("FAIL: 网格未生成任何单元,不导出")