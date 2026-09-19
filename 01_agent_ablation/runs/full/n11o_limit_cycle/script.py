# Mesh generation script for n11o_limit_cycle.stp
# Load model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/n11o_limit_cycle.stp", "module": "iomanager"})

# Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# Select all solids
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Tetrahedral mesh with moderate settings
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 3.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 6.0}
}})

# Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
else:
    # Export BDF
    from arcore.ar_io import ar_io
    bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/full/n11o_limit_cycle/mesh.bdf"
    ret = ar_io.mesh_bdf_output(bdf_path)
    print("BDF 导出返回值:", ret)
    if ret == 0:
        print("BDF 文件已写入:", bdf_path)
    else:
        print("FAIL: BDF 导出失败,返回值", ret)