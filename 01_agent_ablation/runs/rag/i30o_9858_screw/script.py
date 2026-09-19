app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i30o_9858_screw.step", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 1.5, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 4.0}}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i30o_9858_screw/mesh.bdf")
    print("BDF 导出返回值:", ret)
    # 验证 BDF 文件
    import os
    fpath = "D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i30o_9858_screw/mesh.bdf"
    if os.path.exists(fpath):
        fsize = os.path.getsize(fpath)
        print("BDF 文件大小:", fsize, "字节")
        with open(fpath, 'r') as f:
            content = f.read()
        has_grid = "GRID" in content
        has_ctetra = "CTETRA" in content
        grid_count = content.count("GRID")
        ctetra_count = content.count("CTETRA")
        print("GRID 数量:", grid_count)
        print("CTETRA 数量:", ctetra_count)
        if fsize > 1024 and has_grid and has_ctetra and ctetra_count > 0:
            print("SUCCESS: BDF 验证通过 - 含 GRID 和 CTETRA 单元")
        else:
            print("FAIL: BDF 验证未通过")
    else:
        print("FAIL: BDF 文件未生成")