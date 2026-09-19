# ArcherPre script: tetrahedral mesh for i12o_s5.step -> mesh.bdf

model_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i12o_s5.step"
bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/subagent/i12o_s5/mesh.bdf"

# 1. Load geometry
app.process({"action": "loadModel", "fileName": model_path, "module": "iomanager"})

# 2. Enter solid mesh module
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
        "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
        "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
    }
})

# 5. Leave mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 6. Check element count (use global app)
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n == 0:
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # 7. Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output(bdf_path)
    print("BDF 导出返回值:", ret)
    if ret == 0:
        print("BDF 写入成功,需验证内容")
    else:
        print("FAIL: BDF 导出失败")