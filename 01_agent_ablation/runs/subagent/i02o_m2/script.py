# ArcherPre mesh script - tetrahedral mesh for i02o_m2.step
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i02o_m2.step", "module": "iomanager"})
print("Model loaded.")

# Enter solid mesher, select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("Parts selected.")

# Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 15.0}
}})
print("Meshing done.")

# Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
print("Exited solid mesher.")

# Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    # Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i02o_m2/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("Success: {} elements exported.".format(n))
else:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")