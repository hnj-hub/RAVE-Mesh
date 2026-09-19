# ArcherPre mesh script - i09o_m9.step
# Tet mesh -> BDF export with validation

app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i09o_m9.step", "module": "iomanager"})

app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Count elements
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i09o_m9/mesh.bdf")
    print("BDF 导出返回值:", ret)
    # Verify BDF
    import os
    fpath = "D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i09o_m9/mesh.bdf"
    if os.path.exists(fpath):
        fsize = os.path.getsize(fpath)
        print("BDF 文件大小:", fsize, "bytes")
        if fsize > 1000:
            with open(fpath, "r") as f:
                content = f.read()
            grid_cnt = content.count("GRID")
            tet_cnt = content.count("CTETRA")
            print("GRID 数:", grid_cnt)
            print("CTETRA 数:", tet_cnt)
            if grid_cnt > 0 and tet_cnt > 0:
                print("SUCCESS: BDF 验证通过 - 含 GRID 和 CTETRA")
            else:
                print("FAIL: BDF 缺少 GRID 或 CTETRA")
        else:
            print("FAIL: BDF 文件过小或无内容")
    else:
        print("FAIL: BDF 文件未生成")