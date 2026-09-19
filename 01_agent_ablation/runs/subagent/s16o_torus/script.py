app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s16o_torus.stp", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 3.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/s16o_torus/mesh.bdf")
    print("BDF 导出返回值:", ret)
    # 读回文件验证
    with open("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/s16o_torus/mesh.bdf", "r") as f:
        content = f.read()
    grid_count = content.count("GRID")
    ctetra_count = content.count("CTETRA")
    print("GRID 卡片数:", grid_count)
    print("CTETRA 卡片数:", ctetra_count)
    if grid_count > 0 and ctetra_count > 0:
        print("SUCCESS: BDF 验证通过,含 GRID 和 CTETRA")
    else:
        print("FAIL: BDF 验证失败,缺少 GRID 或 CTETRA")