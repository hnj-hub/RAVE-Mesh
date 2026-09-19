# ArcherPre mesh script - i13o_s6.step -> tetrahedral mesh -> BDF
app.process({"action": "loadModel", "fileName": "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i13o_s6.step", "module": "iomanager"})

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
    print("FAIL: 网格未生成任何单元,不导出")
else:
    # Quality check
    quality = app.getElemQuality([])
    for q in quality:
        if q["name"] == "tet collapse":
            print("坍塌率(threshold=%.2f): badElems=%d" % (q["threshold"], len(q["badElems"])))
            break
    # Export BDF
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output("D:/新建文件夹/my-agent/evals_p0_1_agent/full/i13o_s6/mesh.bdf")
    print("BDF 导出返回值:", ret)