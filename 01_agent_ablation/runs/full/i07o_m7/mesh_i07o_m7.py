# Step 1: Load the STEP geometry
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i07o_m7.step", "module": "iomanager"})

# Step 2: Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# Step 3: Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Step 4: Generate tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 8.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 16.0}
}})

# Step 5: Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Step 6: Check total element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

# Step 7: Only export if elements exist
if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/full/i07o_m7/mesh.bdf")
    print("BDF 导出返回值:", ret)
    if ret == 0:
        print("BDF 导出成功")
    else:
        print("BDF 导出失败,返回值:", ret)
else:
    print("FAIL: 网格未生成任何单元,不导出")