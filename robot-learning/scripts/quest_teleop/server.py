import asyncio, json, ssl, time
from pathlib import Path
from aiohttp import web, WSMsgType

HERE = Path(__file__).parent
latest = {"msg": None, "count": 0}

async def index(request):
    return web.FileResponse(HERE / "index.html")

async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("Quest connected")
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            latest["msg"] = json.loads(msg.data)
            latest["count"] += 1
    print("Quest disconnected")
    return ws

def fmt(h):
    if not h:
        return "--"
    x, y, z = h["pos"]
    return f"({x:+.3f},{y:+.3f},{z:+.3f}) trig={h['trigger']:.2f} grip={h['grip']:.2f}"

async def printer(app):
    async def loop():
        last_count, last_t = 0, time.time()
        while True:
            await asyncio.sleep(0.5)
            now = time.time()
            rate = (latest["count"] - last_count) / (now - last_t)
            last_count, last_t = latest["count"], now
            m = latest["msg"]
            if not m:
                continue
            print(f"{rate:5.1f} Hz | R {fmt(m['hands'].get('right'))} | L {fmt(m['hands'].get('left'))}")
    task = asyncio.create_task(loop())
    yield
    task.cancel()

app = web.Application()
app.add_routes([web.get("/", index), web.get("/ws", ws_handler)])
app.cleanup_ctx.append(printer)

ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ctx.load_cert_chain(HERE / "cert.pem", HERE / "key.pem")
web.run_app(app, host="0.0.0.0", port=8443, ssl_context=ctx)
