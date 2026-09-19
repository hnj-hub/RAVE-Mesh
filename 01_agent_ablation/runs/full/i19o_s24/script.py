# Step 1: Load the CAD model
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i19o_s24.step", "module": "iomanager"})

# Step 2: Enter solid mesher
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})

# Step 3: Select all parts
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# Step 4: Tetrahedral mesh
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 5.0, "growthRatio": 1.3, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
}})

# Step 5: Leave solid mesher
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Step 6: Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
else:
    # Step 7: Export BDF
    from arcore.ar_io import ar_io
    out_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/full/i19o_s24/mesh.bdf"
    ret = ar_io.mesh_bdf_output(out_path)
    print("BDF 导出返回值:", ret)
    
    # Step 8: Validate BDF
    import os
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print("BDF 文件大小:", size, "bytes")
        if size > 1000:
            with open(out_path, "r") as f:
                content = f.read()
            has_grid = "GRID" in content
            has_ctetra = "CTETRA" in content
            print("含 GRID:", has_grid)
            print("含 CTETRA:", has_ctetra)
            if has_grid and has_ctetra:
                print("SUCCESS: BDF 验证通过!")
            else:
                print("FAIL: BDF 缺少 GRID 或 CTETRA 卡片")
        else:
            print("FAIL: BDF 文件太小,可能无网格单元")
    else:
        print("FAIL: BDF 文件未生成")