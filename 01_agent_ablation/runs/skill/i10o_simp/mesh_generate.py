app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i10o_simp.step", "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 4.0, "growthRatio": 1.3, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 查单元总数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)
if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
else:
    # 导出 BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i10o_simp/mesh.bdf")
    print("BDF 导出返回值:", ret)

    # 验证 BDF 文件内容
    import os
    path = "D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i10o_simp/mesh.bdf"
    if os.path.exists(path):
        size = os.path.getsize(path)
        print("BDF 文件大小:", size, "bytes")
        if size > 1000:
            with open(path, "r") as f:
                content = f.read()
            has_grid = "GRID" in content
            has_ctetra = "CTETRA" in content
            grid_count = content.count("GRID")
            ctetra_count = content.count("CTETRA")
            print("GRID 出现次数:", grid_count)
            print("CTETRA 出现次数:", ctetra_count)
            if has_grid and has_ctetra and ctetra_count > 0:
                print("SUCCESS: BDF 验证通过 - 包含 GRID 节点和 CTETRA 单元")
            else:
                print("FAIL: BDF 验证失败 - 缺少 GRID 或 CTETRA")
                if not has_grid:
                    print("  - 缺少 GRID 卡片")
                if not has_ctetra:
                    print("  - 缺少 CTETRA 卡片")
                if ctetra_count == 0:
                    print("  - CTETRA 数量为 0")
        else:
            print("FAIL: BDF 文件太小,可能无有效网格数据")
            # 打印前几行看看
            with open(path, "r") as f:
                print("文件内容:")
                print(f.read())
    else:
        print("FAIL: BDF 文件未生成")