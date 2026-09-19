# 探测模型尺寸
from arcore.ar_io import ar_io

inp = r"D:\新建文件夹\my-agent\evals_p0_1_agent\models_40\i16o_s9.step"
app.process({"action": "loadModel", "fileName": inp, "module": "iomanager"})

# 获取 bounding box
ret = app.process({"action": "get", "module": "modelmanager", "var": "boundingBox"})
print("boundingBox:", ret)

# 获取模型信息
ret = app.process({"action": "get", "module": "modelmanager", "var": "modelInfo"})
print("modelInfo:", ret)