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

# ===== 7. Validate BDF content =====
with open(bdf_path, "r") as f:
    content = f.read()

grid_count = content.count("GRID")
ctetra_count = content.count("CTETRA")
print("BDF文件验证: GRID卡数={}, CTETRA卡数={}".format(grid_count, ctetra_count))

if grid_count == 0:
    print("FAIL: BDF中无GRID节点卡")
    sys.exit(1)
if ctetra_count == 0:
    print("FAIL: BDF中无CTETRA单元卡")
    sys.exit(1)

print("BDF验证通过! 网格含 {} 个节点, {} 个CTETRA单元".format(grid_count, ctetra_count))
print("Done!")