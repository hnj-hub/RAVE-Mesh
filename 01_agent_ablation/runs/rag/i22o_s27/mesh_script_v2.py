# 1. 加载 STEP 几何模型
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i22o_s27.step", "module": "iomanager"})

# 2. 进入实体剖分器,全选所有体
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 3. 四面体剖分
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 3.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}
}})

# 4. 退出剖分器
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 5. 验证单元数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
else:
    # 6. 导出 BDF
    from arcore.ar_io import ar_io
    output_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i22o_s27/mesh.bdf"
    ret = ar_io.mesh_bdf_output(output_path)
    print("BDF导出返回值:", ret)

    # 7. 验证 BDF 文件内容
    import os
    file_size = os.path.getsize(output_path)
    print("BDF文件大小:", file_size, "bytes")

    # 用读取方式验证内容
    with open(output_path, "r") as f:
        content = f.read()

    grid_count = content.count("GRID")
    ctetra_count = content.count("CTETRA")
    print("GRID节点数:", grid_count)
    print("CTETRA单元数:", ctetra_count)

    if grid_count > 0 and ctetra_count > 0:
        print("PASS: BDF包含GRID节点和CTETRA单元,验证通过!")
    else:
        print("FAIL: BDF验证失败 - 缺少GRID或CTETRA")