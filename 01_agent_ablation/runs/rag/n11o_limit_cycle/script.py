app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/n11o_limit_cycle.stp", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 15.0, "growthRatio": 2.0, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 30.0}}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/n11o_limit_cycle/mesh.bdf")
    print("BDF 导出返回值:", ret)
    # Validate: check file size and content
    import os
    size = os.path.getsize("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/n11o_limit_cycle/mesh.bdf")
    print("BDF 文件大小:", size, "bytes")
    if size > 0:
        with open("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/n11o_limit_cycle/mesh.bdf") as f:
            content = f.read()
        has_grid = "GRID" in content
        has_ctetra = "CTETRA" in content
        grid_count = content.count("GRID")
        ctetra_count = content.count("CTETRA")
        print("GRID 出现次数:", grid_count)
        print("CTETRA 出现次数:", ctetra_count)
        if has_grid and has_ctetra and ctetra_count > 0:
            print("SUCCESS: BDF 包含 GRID 节点和 CTETRA 单元,验证通过")
        else:
            print("FAIL: BDF 缺少 GRID 或 CTETRA")
    else:
        print("FAIL: BDF 文件为空")