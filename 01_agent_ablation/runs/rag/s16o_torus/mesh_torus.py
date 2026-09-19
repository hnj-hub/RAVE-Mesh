# 加载模型
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s16o_torus.stp", "module": "iomanager"})

# 进入实体剖分器
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# 全选所有体
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 四面体剖分
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 3.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}
}})

# 退出剖分器
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 检查单元数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    # 导出 BDF
    from arcore.ar_io import ar_io
    bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/rag/s16o_torus/mesh.bdf"
    ret = ar_io.mesh_bdf_output(bdf_path)
    print("BDF 导出返回值:", ret)
else:
    print("FAIL: 网格未生成任何单元,不导出")