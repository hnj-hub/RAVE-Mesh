# Tetrahedral mesh script for i06o_m6.step

# 1. Load model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i06o_m6.step", "module": "iomanager"})

# 2. Enter solid mesher, select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 3. Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})

# 4. Leave mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 5. Check total element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    # 6. Export BDF
    from arcore.ar_io import ar_io
    bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i06o_m6/mesh.bdf"
    ret = ar_io.mesh_bdf_output(bdf_path)
    print("BDF 导出返回值:", ret)
    print("导出路径:", bdf_path)
else:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
    print("RESULT: FAIL")