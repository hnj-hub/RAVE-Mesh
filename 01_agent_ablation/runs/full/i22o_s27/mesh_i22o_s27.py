import sys

# ===== 1. Load the STEP model =====
app.process({
    "action": "loadModel",
    "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i22o_s27.step",
    "module": "iomanager"
})

# ===== 2. Enter solid mesher and select all parts =====
app.process({
    "action": "enter",
    "entityType": "parts",
    "module": "solidmesher"
})
app.process({
    "action": "whole",
    "entityType": 1,
    "module": "selectionmanager"
})

# ===== 3. Tetrahedral mesh =====
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

# ===== 4. Leave solid mesher =====
app.process({
    "action": "leave",
    "entityType": "parts",
    "module": "solidmesher"
})

# ===== 5. Check element count =====
elem_info = app.get({"module": "modelmanager", "contentType": "elemNum"})
n_total = elem_info["elemNum"]
print("=" * 50)
print("单元总数:", n_total)

if n_total == 0:
    print("FAIL: 网格未生成任何单元(模型可能不是封闭体),不导出BDF")
    sys.exit(1)

# ===== 6. Export BDF =====
from arcore.ar_io import ar_io
bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/full/i22o_s27/mesh.bdf"
ret = ar_io.mesh_bdf_output(bdf_path)
print("BDF导出返回值:", ret)
print("=" * 50)

if ret != 0:
    print("FAIL: BDF导出失败,返回值={}".format(ret))
    sys.exit(1)

print("BDF导出成功: " + bdf_path)
print("Done!")