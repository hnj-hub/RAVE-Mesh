# -*- coding: utf-8 -*-
"""ArcherPre 四面体剖分脚本: 加载 STP → 四面体剖分 → BDF 导出"""

import ArcherPre

# 1. 加载 CAD 模型
stp_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/models_40/n11o_limit_cycle.stp"
app = ArcherPre.ArcherPre()
app.loadModel(stp_path)

# 2. 设置剖分参数
mesh_size = 15.0          # 表面网格尺寸
growth_ratio = 2.0        # 增长比
mesh_size_max = 30.0      # 最大体网格尺寸
refinement_angle = 45.0   # 细化角度

app.setMeshSize(mesh_size)
app.setGrowthRatio(growth_ratio)
app.setMeshSizeMax(mesh_size_max)
app.setRefinementAngle(refinement_angle)

# 3. 执行四面体剖分
app.process()

# 4. 导出 BDF
bdf_path = "D:/新建文件夹/my-agent/evals_p0_1_agent/skill/n11o_limit_cycle/mesh.bdf"
app.exportBDF(bdf_path)

print("Done!")