# 1. Load STEP model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i03o_m3.step", "module": "iomanager"})

# 2. Enter solid mesher, select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 3. Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 15.0, "growthRatio": 2.0, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 30.0}
}})

# 4. Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 5. Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # 6. Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i03o_m3/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("SUCCESS: 网格已生成并导出,单元数:", n)