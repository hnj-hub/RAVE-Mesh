app.process({"action": "loadModel", "fileName": "C:/Users/10059/Desktop/my-agent/evals_p0_1_agent/models/n11o_limit_cycle.stp", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 15.0, "growthRatio": 2.0, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 30.0}}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("elemNum:", n)
if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("C:/Users/10059/Desktop/my-agent/evals_p0_1_agent/skill/n11o_limit_cycle/mesh.bdf")
    print("BDF export ret:", ret)
else:
    print("FAIL: no element generated, skip export")
print("Done!")
