# 加载模型
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i02o_m2.step", "module": "iomanager"})

# 进入实体剖分器,全选所有体
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 四面体剖分
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})

# 退出剖分器
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 查全部单元总数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    # 有单元,导出 BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i02o_m2/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("SUCCESS: 网格生成完成,共", n, "个单元")
else:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")