# Mesh script for i30o_9858_screw.step -> tetrahedral mesh -> BDF
# Load model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i30o_9858_screw.step", "module": "iomanager"})

# Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 2.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 5.0}
}})

# Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    # Export BDF
    from arcore.ar_io import ar_io
    out_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i30o_9858_screw/mesh.bdf"
    ret = ar_io.mesh_bdf_output(out_path)
    print("BDF 导出返回值:", ret)
    print("Done!")
else:
    print("FAIL: 网格未生成任何单元,不导出")