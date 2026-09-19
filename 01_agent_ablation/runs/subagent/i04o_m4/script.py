# Tetrahedral mesh script for i04o_m4.step
# Load model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i04o_m4.step", "module": "iomanager"})

# Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Tet mesh with moderate parameters
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "surfaceMesh": {"elemType": "ETri", "meshSize": 8.0, "growthRatio": 1.4, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 16.0}
}})

# Leave mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i04o_m4/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("Done!")