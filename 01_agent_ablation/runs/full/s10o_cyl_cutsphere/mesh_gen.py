# 四面体剖分脚本
# 加载 STEP → 四面体剖分 → 验证单元数 → 导出 BDF

MODEL_PATH = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s10o_cyl_cutsphere.stp"
BDF_PATH = "D:/新建文件夹/my-agent/evals_p0_1_agent/full/s10o_cyl_cutsphere/mesh.bdf"

# 1. 加载几何
app.process({"action": "loadModel", "fileName": MODEL_PATH, "module": "iomanager"})

# 2. 进入实体剖分器,全选所有体
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 3. 四面体剖分 — 适中尺寸
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 2.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 5.0}
}})

# 4. 退出剖分器
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 5. 查单元总数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # 6. 导出 BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output(BDF_PATH)
    print("BDF 导出返回值:", ret)
    print("Done! 单元数:", n)