# Mesh script for s12o_cube_rounded_1.stp -> BDF
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s12o_cube_rounded_1.stp", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
else:
    # Export BDF
    from arcore.ar_io import ar_io
    bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/s12o_cube_rounded_1/mesh.bdf"
    ret = ar_io.mesh_bdf_output(bdf_path)
    print("BDF 导出返回值:", ret)
    print("导出完成")