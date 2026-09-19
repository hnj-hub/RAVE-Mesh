import sys

# 加载STEP模型
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i19o_s24.step", "module": "iomanager"})

# 进入实体剖分模块
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# 选中全部实体
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 执行四面体剖分
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 12.0}}})

# 退出剖分模块
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 获取单元总数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    # 导出BDF文件
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i19o_s24/mesh.bdf")
    print("BDF导出返回值:", ret)
else:
    print("FAIL: 网格未生成任何单元,不导出")