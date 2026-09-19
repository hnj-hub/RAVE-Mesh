# ArcherPre mesh script: tetrahedral mesh + BDF export
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i22o_s27.step", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "surfaceMesh": {"elemType": "ETri", "meshSize": 15.0, "growthRatio": 2.0, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 30.0}}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i22o_s27/mesh.bdf")
    print("BDF 导出返回值:", ret)
    # Validate BDF content
    import os
    sz = os.path.getsize("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i22o_s27/mesh.bdf")
    print("BDF 文件大小:", sz, "bytes")
    found_grid = False
    found_ctetra = False
    with open("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i22o_s27/mesh.bdf") as f:
        for line in f:
            if line.startswith("GRID"):
                found_grid = True
            if "CTETRA" in line:
                found_ctetra = True
    if found_grid and found_ctetra and sz > 1000:
        print("VALIDATION PASSED: BDF contains GRID and CTETRA, size=" + str(sz))
    else:
        print("VALIDATION FAILED: grid=" + str(found_grid) + " ctetra=" + str(found_ctetra) + " size=" + str(sz))
else:
    print("FAIL: 网格未生成任何单元,不导出")