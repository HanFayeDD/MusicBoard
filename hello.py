from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI()

# 定义根路由，返回 "Hello World"
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# 定义一个带路径参数的路由
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
