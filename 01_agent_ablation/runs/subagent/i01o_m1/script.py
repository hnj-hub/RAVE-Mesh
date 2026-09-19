# 1. Load STEP model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i01o_m1.step", "module": "iomanager"})

# 2. Enter solid mesher, select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 3. Tetrahedral mesh with reasonable parameters
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})

# 4. Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 5. Check total element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    # 6. Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i01o_m1/mesh.bdf")
    print("BDF导出返回值:", ret)
    
    # 7. Validate BDF - check GRID and CTETRA cards
    with open("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i01o_m1/mesh.bdf", "r") as f:
        content = f.read()
    grid_count = content.count("GRID")
    ctetra_count = content.count("CTETRA")
    print("GRID节点数:", grid_count)
    print("CTETRA单元数:", ctetra_count)
    if grid_count > 0 and ctetra_count > 0:
        print("VALIDATION PASSED: BDF contains GRID nodes and CTETRA elements.")
    else:
        print("VALIDATION FAILED: BDF missing GRID or CTETRA cards.")
else:
    print("FAIL: 网格未生成任何单元,不导出BDF")