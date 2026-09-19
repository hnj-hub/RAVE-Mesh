app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i31o_dlr_f6.brep", "module": "iomanager"})
print("Model loaded.")

app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("Selected all parts.")

app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 15.0, "growthRatio": 2.0, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 30.0}}})
print("Meshing done.")

app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
print("Left solid mesher.")

n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i31o_dlr_f6/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("SUCCESS: 网格生成并导出")
else:
    print("FAIL: 网格未生成任何单元")