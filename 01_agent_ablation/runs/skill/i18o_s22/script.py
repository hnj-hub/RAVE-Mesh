import os

model_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/i18o_s22.step"
output_dir = "D:/新建文件夹/my-agent/evals_p0_1_agent/skill/i18o_s22"
output_bdf = os.path.join(output_dir, "mesh.bdf")

print("=" * 60)
print("i18o_s22 网格剖分")
print("模型:", model_path)
print("输出:", output_bdf)
print("=" * 60)

# 1. 加载 STEP 模型
print("\n[1/4] 加载模型...")
app.process({"action": "loadModel", "fileName": model_path, "module": "iomanager"})
print("  模型加载完成")

# 2. 进入实体剖分
print("\n[2/4] 进入实体剖分模块...")
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
print("  已选择全部实体")

# 3. 执行四面体剖分
print("\n[3/4] 执行四面体剖分...")
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "surfaceMesh": {
        "elemType": "ETri",
        "meshSize": 6.0,
        "growthRatio": 1.5,
        "sizePriority": 1,
        "refinementAngle": 45.0
    },
    "tetraMesh": {
        "allTet": 1,
        "meshSizeMax": 10.0
    }
}})
print("  剖分完成")

# 4. 离开剖分模块
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})

# 5. 检查单元数
n = app.get({"module": "modelmanager", "contentType": "elemNum"})["elemNum"]
print(f"\n单元总数: {n}")

# 6. 导出 BDF
if n == 0:
    print("FAIL: 网格未生成任何单元(可能薄板做体剖分无体积),不导出")
else:
    print("\n[4/4] 导出 BDF 文件...")
    from arcore.ar_io import ar_io
    ret = ar_io.mesh_bdf_output(output_bdf)
    print(f"BDF 导出返回值: {ret}")
    # 验证文件存在且非空
    if os.path.isfile(output_bdf):
        size = os.path.getsize(output_bdf)
        print(f"BDF 文件大小: {size} 字节")
        if size > 0:
            print("SUCCESS: BDF 文件已生成")
        else:
            print("FAIL: BDF 文件为空")
    else:
        print(f"FAIL: BDF 文件未生成于 {output_bdf}")

print("\nDone!")