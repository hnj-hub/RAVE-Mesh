# -*- coding: utf-8 -*-
import ArcherPy
from arcore.ar_io import ar_io

app = ArcherPy.App()

# 导入STEP模型
model_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/s09o_bridge.step"
app.process("import", "step", [model_path])

# 四面体网格剖分参数
meshSize = 6.0
growthRatio = 1.3
refinementAngle = 45.0
meshSizeMax = 12.0

# 执行表面网格剖分
app.process("surfacemesh", "tetramesh", [
    "meshsize=" + str(meshSize),
    "growthratio=" + str(growthRatio),
    "refinementangle=" + str(refinementAngle),
    "meshSizeMax=" + str(meshSizeMax),
])

# 执行体网格剖分
app.process("solidmesh", "tetramesh", [
    "meshsize=" + str(meshSize),
    "growthratio=" + str(growthRatio),
    "refinementangle=" + str(refinementAngle),
    "meshSizeMax=" + str(meshSizeMax),
])

# 导出为BDF文件
output_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/skill/s09o_bridge/mesh.bdf"
ar_io.mesh_bdf_output(output_path)

print("Mesh generation and BDF export completed successfully.")
print("Output file:", output_path)