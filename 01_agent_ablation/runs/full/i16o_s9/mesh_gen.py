# ArcherPre 四面体剖分脚本
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i16o_s9.step", "module": "iomanager"})

app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 检查单元总数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
    import sys
    sys.exit(1)
else:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/full/i16o_s9/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("Done!")