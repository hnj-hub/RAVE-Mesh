# Load model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i08o_m8.step", "module": "iomanager"})
print("Model loaded")

# Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
print("Entered solidmesher")

# Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("Selected all parts")

# Tetrahedral mesh with finer settings
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 4.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}
}})
print("Meshing done")

# Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
print("Left solidmesher")

# Check element count - try multiple approaches
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

# Also check by types
result = app.get({"module": "modelmanager", "contentType": "elemNum", "types": ["CTETRA"]})
print("CTETRA count result:", result)

if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
else:
    # Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i08o_m8/mesh.bdf")
    print("BDF 导出返回值:", ret)
    # Check file size
    import os
    if os.path.exists("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i08o_m8/mesh.bdf"):
        size = os.path.getsize("D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i08o_m8/mesh.bdf")
        print("BDF 文件大小:", size, "bytes")
    print("Done!")