# ArcherPre 四面体剖分 -> BDF 导出脚本
MODEL_PATH = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i30o_9858_screw.step"
BDF_PATH = "D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i30o_9858_screw/mesh.bdf"

# 1. 加载几何
app.process({"action": "loadModel", "fileName": MODEL_PATH, "module": "iomanager"})
print("模型加载完成")

# 2. 进入实体剖分器,全选所有体
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("已全选所有体")

# 3. 四面体剖分 (螺丝带螺纹,用较细网格确保质量)
app.process({
    "action": "mesh",
    "module": "solidmesher",
    "meshSetting": {
        "meshType": "tetmesh",
        "curveMesh": {"alignment": 1, "refinementAngle": 30.0},
        "surfaceMesh": {"elemType": "ETri", "meshSize": 1.5, "growthRatio": 1.2, "sizePriority": 1},
        "tetraMesh": {"allTet": 1, "meshSizeMax": 3.0}
    }
})
print("剖分完成")

# 4. 退出剖分器
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 5. 验证单元数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
    raise SystemExit(1)

# 6. 导出 BDF
from arcore.ar_io import ar_io
ret = ar_io.mesh_bdf_output(BDF_PATH)
print("BDF 导出返回值:", ret)
print("导出路径:", BDF_PATH)

# 7. 验证 BDF 文件
import os
if os.path.exists(BDF_PATH):
    size = os.path.getsize(BDF_PATH)
    print("BDF 文件大小:", size, "bytes")
    with open(BDF_PATH, 'r') as f:
        content = f.read()
    grid_count = content.count("GRID")
    ctetra_count = content.count("CTETRA")
    print("GRID 节点数:", grid_count)
    print("CTETRA 单元数:", ctetra_count)
    if grid_count > 0 and ctetra_count > 0:
        print("PASS: BDF 包含 GRID 节点和 CTETRA 单元")
    else:
        print("FAIL: BDF 缺少 GRID 或 CTETRA")
        raise SystemExit(1)
else:
    print("FAIL: BDF 文件未生成")
    raise SystemExit(1)