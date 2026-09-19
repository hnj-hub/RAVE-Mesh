# ArcherPre script: tetrahedral mesh for i31o_dlr_f6.brep, export BDF
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i31o_dlr_f6.brep", "module": "iomanager"})

app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "curveMesh": {"alignment": 1, "refinementAngle": 45.0},
    "surfaceMesh": {"elemType": "ETri", "meshSize": 8.0, "growthRatio": 1.3, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 20.0}
}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# Check element count
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print("单元总数:", n)

if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
else:
    # Export BDF
    from arcore.ar_io import ar_io
    bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/rag/i31o_dlr_f6/mesh.bdf"
    ret = ar_io.mesh_bdf_output(bdf_path)
    print("BDF 导出返回值:", ret)
    print("Done!")