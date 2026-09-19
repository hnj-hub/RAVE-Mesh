app.process({"action": "loadModel", "fileName": "C:/Users/10059/Desktop/my-agent/evals_p0_1_agent/models/s13o_cube_rounded_2.stp", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 15.0, "growthRatio": 2.0, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 30.0}}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("C:/Users/10059/Desktop/my-agent/evals_p0_1_agent/skill/s13o_cube_rounded_2/mesh.bdf")
    print("BDF 导出返回值:", ret)
else:
    print("FAIL: 网格未生成任何单元,不导出")
