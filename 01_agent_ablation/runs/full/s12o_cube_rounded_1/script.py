# Step 1: Load the CAD model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s12o_cube_rounded_1.stp", "module": "iomanager"})

# Step 2: Enter solid mesher and select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Step 3: Tetrahedral mesh with reasonable sizes for a rounded cube
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "surfaceMesh": {"elemType": "ETri", "meshSize": 2.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 4.0}
}})

# Step 4: Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Step 5: Check total element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # Step 6: Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/full/s12o_cube_rounded_1/mesh.bdf")
    print("BDF 导出返回值:", ret)