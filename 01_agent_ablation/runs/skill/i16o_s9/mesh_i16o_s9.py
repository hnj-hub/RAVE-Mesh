# 剖分 i16o_s9.step 并导出 BDF
from arcore.ar_io import ar_io

inp = r"D:\新建文件夹\my-agent\evals_p0_1_agent\models_40\i16o_s9.step"
out = r"D:\新建文件夹\my-agent\evals_p0_1_agent\skill\i16o_s9\mesh.bdf"

print("=== 开始剖分:", inp)
app.process({"action": "loadModel", "fileName": inp, "module": "iomanager"})
app.process({"action": "enter", "entityType": "parts", "module": "solidmesher"})
app.process({"action": "whole", "entityType": 1, "module": "selectionmanager"})
app.process({"action": "mesh", "module": "solidmesher", "meshSetting": {
    "meshType": "tetmesh",
    "surfaceMesh": {"elemType": "ETri", "meshSize": 8.0, "growthRatio": 1.5, "sizePriority": 1},
    "tetraMesh": {"allTet": 1, "meshSizeMax": 16.0}}})
app.process({"action": "leave", "entityType": "parts", "module": "solidmesher"})
print("=== 剖分完成，导出 BDF")

ret = ar_io.mesh_bdf_output(out)
print("BDF 导出返回值:", ret, "->", out)

# 验证导出的 BDF
with open(out, 'r') as f:
    content = f.read()
n_grid = content.count('GRID')
n_ctetra = content.count('CTETRA')
print(f"=== 验证: GRID 节点数 = {n_grid}, CTETRA 单元数 = {n_ctetra}")
if n_grid > 0 and n_ctetra > 0:
    print("=== 验证通过: BDF 包含节点和四面体单元")
else:
    print("=== 验证失败: BDF 缺少节点或单元!")
print("=== 完成")