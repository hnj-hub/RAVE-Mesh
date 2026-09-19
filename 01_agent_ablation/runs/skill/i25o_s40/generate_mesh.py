# ArcherPre tetrahedral meshing script for i25o_s40.step
# Load STEP -> tet mesh -> validate -> export BDF

# 1. Load geometry
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i25o_s40.step", "module": "iomanager"})

# 2. Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# 3. Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 4. Generate tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 12.0}
}})

# 5. Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 6. Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    # 7. Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i25o_s40/mesh.bdf")
    print("BDF 导出返回值:", ret)
    if ret == 0:
        print("SUCCESS: 网格已导出至 mesh.bdf, 单元数:", n)
    else:
        print("FAIL: BDF 导出失败, 返回码:", ret)
else:
    print("FAIL: 网格未生成任何单元, 不导出")