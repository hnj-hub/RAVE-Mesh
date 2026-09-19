# -*- coding: utf-8 -*-
"""s17o_sphere 四面体网格剖分 + BDF 导出"""

import os

# 1. 加载几何模型
app.process({
    "action": "loadModel",
    "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s17o_sphere.stp",
    "module": "iomanager"
})

# 2. 进入零件级体网格剖分
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 3. 四面体剖分
app.process({
    "action": "mesh",
    "module": "solidmesher",
    "meshSetting": {
        "meshType": "tetmesh",
        "surfaceMesh": {
            "elemType": "ETri",
            "meshSize": 2.0,
            "growthRatio": 1.3,
            "refinementAngle": 45.0,
            "sizePriority": 1
        },
        "tetraMesh": {
            "allTet": 1,
            "meshSizeMax": 5.0
        }
    }
})

app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 4. 检查单元数量
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

# 5. 导出 BDF（仅当有单元时）
if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    from arcore.ar_io import ar_io
    out_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/skill/s17o_sphere/mesh.bdf"
    ret = ar_io.mesh_bdf_output(out_path)
    print("BDF 导出返回值:", ret)
    # 确认文件存在
    if os.path.isfile(out_path):
        print("BDF 文件已生成:", out_path)
    else:
        print("FAIL: BDF 文件未生成")
print("Done!")