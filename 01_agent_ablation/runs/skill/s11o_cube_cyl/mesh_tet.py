# 1. 加载几何
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s11o_cube_cyl.stp", "module": "iomanager"})

# 2. 进入实体剖分器,全选所有体
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})

# 3. 四面体剖分
app.process({
    "action": "mesh",
    "module": "solidmesher",
    "meshSetting": {
        "meshType": "tetmesh",
        "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
        "surfaceMesh": {"elemType": "ETri", "meshSize": 4.0, "growthRatio": 1.5, "sizePriority": 1},
        "tetraMesh": {"allTet": 1, "meshSizeMax": 10.0}
    }
})

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
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/skill/s11o_cube_cyl/mesh.bdf")
    print("BDF 导出返回值:", ret)
    print("Done!")