# ArcherPre script: tetrahedral mesh for s09o_bridge.step -> mesh.bdf
model = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s09o_bridge.step"
bdf_out = "D:/新建文件夹/my-agent/evals_p0_1_agent/full/s09o_bridge/mesh.bdf"

# 1. Load geometry
app.process({"action": "loadModel", "fileName": model, "module": "iomanager"})

# 2. Enter solid mesher, select all parts
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 3. Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 8.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 20.0}
}})

# 4. Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 5. Check total element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
else:
    # 6. Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output(bdf_out)
    print("BDF 导出返回值:", ret)
    # Recheck file
    import os
    if os.path.getsize(bdf_out) > 1024:
        with open(bdf_out, "r") as f:
            head = f.read(2000)
        if "GRID" in head and "CTETRA" in head:
            print("SUCCESS: BDF contains GRID and CTETRA")
        else:
            print("WARNING: BDF file exists but may lack GRID/CTETRA cards")
    else:
        print("FAIL: BDF file too small or empty")