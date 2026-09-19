# 加载几何
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i02o_m2.step", "module": "iomanager"})

# 进入实体剖分器，全选所有体
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 四面体剖分（使用合理的参数）
app.process({
    "action": "mesh",
    "module": "solidmesher",
    "meshSetting": {
        "meshType": "tetmesh",
        "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
        "surfaceMesh": {"elemType": "ETri", "meshSize": 3.0, "growthRatio": 1.2, "sizePriority": 1},
        "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}
    }
})

# 退出剖分器
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 检查单元数量
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元，不导出")
else:
    # 导出 BDF
    output_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i02o_m2/mesh.bdf"
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output(output_path)
    print("BDF 导出返回值:", ret)

    # 验证 BDF 文件
    import os
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            content = f.read()
        grid_count = content.count("GRID")
        ctetra_count = content.count("CTETRA")
        print("BDF 验证: GRID 出现次数 =", grid_count, ", CTETRA 出现次数 =", ctetra_count)
        if grid_count > 0 and ctetra_count > 0:
            print("SUCCESS: BDF 文件包含 GRID 节点和 CTETRA 单元，验证通过")
        else:
            print("FAIL: BDF 文件缺少 GRID 或 CTETRA")
    else:
        print("FAIL: BDF 文件未生成")