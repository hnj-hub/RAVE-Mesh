# 网格剖分脚本: i20o_s25.step -> tetmesh -> BDF
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i20o_s25.step", "module": "iomanager"})

# 进入实体剖分器,全选所有体
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 四面体剖分
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 3.0, "growthRatio": 1.2, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 8.0}
}})

# 退出剖分器
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 验证单元数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
else:
    # 导出 BDF
    from arcore.ar_io import ar_io
    out_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i20o_s25/mesh.bdf"
    ret = ar_io.mesh_bdf_output(out_path)
    print("BDF 导出返回值:", ret)

    # 验证 BDF 文件
    import os
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print("BDF 文件大小:", size, "bytes")
        with open(out_path, "r") as f:
            content = f.read()
        grid_count = content.count("GRID")
        ctetra_count = content.count("CTETRA")
        print("GRID 卡片数:", grid_count)
        print("CTETRA 卡片数:", ctetra_count)
        if grid_count > 0 and ctetra_count > 0:
            print("SUCCESS: BDF 验证通过 (GRID>0, CTETRA>0)")
        else:
            print("FAIL: BDF 验证不通过 - GRID或CTETRA为空")
    else:
        print("FAIL: BDF 文件未生成")

print("Done!")