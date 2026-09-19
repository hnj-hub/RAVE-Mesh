# Load geometry
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i05o_m5.step", "module": "iomanager"})

# Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 4.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}
}})

# Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Check total element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i05o_m5/mesh.bdf")
    print("BDF 导出返回值:", ret)