app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i21o_s26.step", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.3, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 12.0}
}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i21o_s26/mesh.bdf")
    print("BDF 导出返回值:", ret)
else:
    print("FAIL: 网格未生成任何单元,不导出")