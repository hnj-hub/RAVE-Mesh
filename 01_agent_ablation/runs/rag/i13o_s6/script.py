print("=== Step 1: Load model ===")
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i13o_s6.step", "module": "iomanager"})
print("Model loaded.")

print("=== Step 2: Enter solidmesher ===")
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("All parts selected.")

print("=== Step 3: Tetrahedral mesh ===")
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})
print("Meshing done.")

print("=== Step 4: Check element count ===")
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n > 0:
    print("=== Step 5: Export BDF ===")
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i13o_s6/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("SUCCESS: Mesh generated with", n, "elements and exported.")
else:
    print("FAIL: 网格未生成任何单元,不导出")