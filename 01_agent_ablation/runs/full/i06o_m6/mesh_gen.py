import sys

# 1. 加载几何模型
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i06o_m6.step", "module": "iomanager"})
print("STEP loaded")

# 2. 进入实体剖分器
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("Parts selected")

# 3. 四面体剖分
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 4.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})
print("Meshing done")

# 4. 退出剖分器
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
print("Left solid mesher")

# 5. 检查单元总数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
    sys.exit(1)

# 6. 导出 BDF
from arcore.ar_io import ar_io
ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/full/i06o_m6/mesh.bdf")
print("BDF 导出返回值:", ret)
print("Done! 单元数:", n)