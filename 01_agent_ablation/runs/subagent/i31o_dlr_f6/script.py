# ArcherPre script: tet mesh i31o_dlr_f6.brep -> mesh.bdf
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i31o_dlr_f6.brep", "module": "iomanager"})

app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 12.0}
}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Get total element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i31o_dlr_f6/mesh.bdf")
    print("BDF 导出返回值:", ret)
    # Quick validation
    import os
    fpath = "D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i31o_dlr_f6/mesh.bdf"
    if os.path.exists(fpath):
        fsize = os.path.getsize(fpath)
        print("BDF 文件大小:", fsize, "bytes")
        with open(fpath, "r") as f:
            content = f.read()
        grid_cnt = content.count("GRID")
        ctetra_cnt = content.count("CTETRA")
        cquad_cnt = content.count("CQUAD4")
        ctria_cnt = content.count("CTRIA3")
        print("GRID 行数:", grid_cnt)
        print("CTETRA 行数:", ctetra_cnt)
        print("CQUAD4 行数:", cquad_cnt)
        print("CTRIA3 行数:", ctria_cnt)
        if grid_cnt > 0 and ctetra_cnt > 0:
            print("VALIDATION PASSED: BDF contains GRID nodes and CTETRA elements.")
        else:
            print("VALIDATION FAILED: BDF missing GRID or CTETRA.")
    else:
        print("VALIDATION FAILED: BDF file not found.")
else:
    print("FAIL: 网格未生成任何单元,不导出BDF")