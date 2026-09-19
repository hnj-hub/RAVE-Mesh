# 剖分 i17o_s20.step 并导出 BDF 到 skill 目录
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i17o_s20.step", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i17o_s20/mesh.bdf")
    print("BDF 导出返回值:", ret)

    # 验证 BDF 文件内容
    import os
    path = "D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i17o_s20/mesh.bdf"
    if os.path.exists(path):
        size = os.path.getsize(path)
        print("BDF 文件大小:", size, "bytes")
        if size > 200:
            with open(path, "r") as f:
                content = f.read()
            has_grid = "GRID" in content
            has_ctetra = "CTETRA" in content
            grid_count = content.count("GRID")
            ctetra_count = content.count("CTETRA")
            print("GRID 出现次数:", grid_count)
            print("CTETRA 出现次数:", ctetra_count)
            if has_grid and has_ctetra and ctetra_count > 0:
                print("SUCCESS: BDF 验证通过 - 包含 GRID 节点和 CTETRA 单元")
            else:
                print("FAIL: BDF 验证失败 - 缺少 GRID 或 CTETRA")
        else:
            print("FAIL: BDF 文件太小,可能无有效网格数据")
    else:
        print("FAIL: BDF 文件未生成")