# ArcherPre mesh generation script
# Load CAD -> tetrahedral mesh -> export BDF

# 1. Load the STEP model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i21o_s26.step", "module": "iomanager"})

# 2. Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# 3. Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 4. Tetrahedral mesh
app.process({
    "action": "mesh",
    "module": "solidmesher",
    "meshSetting": {
        "meshType": "tetmesh",
        "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
        "surfaceMesh": {"elemType": "ETri", "meshSize": 8.0, "growthRatio": 1.2, "sizePriority": 1},
        "tetraMesh": {"allTet": 1, "meshSizeMax": 16.0}
    }
})

# 5. Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 6. Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

# 7. Export BDF if elements > 0
if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i21o_s26/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("SUCCESS: 网格已生成, 单元数:", n)
else:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")