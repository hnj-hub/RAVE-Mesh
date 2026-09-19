app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i10o_simp.step", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i10o_simp/mesh.bdf")
    print("BDF 导出返回值:", ret)
    import os
    fsize = os.path.getsize("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i10o_simp/mesh.bdf")
    print("BDF 文件大小:", fsize)
    if fsize > 1000:
        with open("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i10o_simp/mesh.bdf", "r") as f:
            content = f.read()
        has_grid = "GRID" in content
        has_ctetra = "CTETRA" in content
        print("含 GRID:", has_grid, "含 CTETRA:", has_ctetra)
        if has_grid and has_ctetra:
            print("SUCCESS: BDF 验证通过!")
        else:
            print("FAIL: BDF 缺少 GRID 或 CTETRA")
    else:
        print("FAIL: BDF 文件太小或为空")