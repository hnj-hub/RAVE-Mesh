# ArcherPre script: tetrahedral mesh for i29o_bracket.step -> BDF

model_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i29o_bracket.step"
bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i29o_bracket/mesh.bdf"

# 1. Load model
app.process({"action": "loadModel", "fileName": model_path, "module": "iomanager"})

# 2. Enter solidmesher, select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 3. Tetrahedral mesh with reasonable defaults for a bracket
app.process({
    "action": "mesh",
    "module": "solidmesher",
    "meshSetting": {
        "meshType": "tetmesh",
        "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
        "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
        "tetraMesh": {"allTet": 1, "meshSizeMax": 12.0}
    }
})

# 4. Leave solidmesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 5. Check element count - must be > 0
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    # 6. Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output(bdf_path)
    print("BDF 导出返回值:", ret)
else:
    print("FAIL: 网格未生成任何单元,不导出")