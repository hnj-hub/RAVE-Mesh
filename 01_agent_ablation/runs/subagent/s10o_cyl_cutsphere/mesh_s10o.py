# ArcherPre script: tetrahedral mesh for s10o_cyl_cutsphere.stp
model = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s10o_cyl_cutsphere.stp"
bdf_out = "D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/s10o_cyl_cutsphere/mesh.bdf"

# Step 1: Load geometry
app.process({"action": "loadModel", "fileName": model, "module": "iomanager"})

# Step 2: Enter solid mesher, select all
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Step 3: Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Step 4: Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

# Step 5: Export BDF if elements exist
if n > 0:
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output(bdf_out)
    print("BDF 导出返回值:", ret)
else:
    print("FAIL: 网格未生成任何单元（可能薄板做体剖分无体积），不导出")