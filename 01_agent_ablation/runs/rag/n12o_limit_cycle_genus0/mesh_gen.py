# ArcherPre 四面体剖分脚本
# 加载 STEP → 四面体剖分 → 验证单元数 → 导出 BDF

app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/n12o_limit_cycle_genus0.stp", "module": "iomanager"})

app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})

app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 验证单元数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    from arcore.ar_io import ar_io
    out_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/rag/n12o_limit_cycle_genus0/mesh.bdf"
    ret = ar_io.mesh_bdf_output(out_path)
    print("BDF 导出返回值:", ret)
    print("Done! 单元数:", n)
else:
    print("FAIL: 网格未生成任何单元,不导出")