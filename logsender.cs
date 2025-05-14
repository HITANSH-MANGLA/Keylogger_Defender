using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class LogSender
{
    private static readonly string logFilePath = "C:\\path\\to\\your\\logfile.txt"; // Apna actual log file path do
    private static readonly string serverUrl = "http://127.0.0.1:5000/upload"; // Flask server ka address

    public static async Task SendLogFile()
    {
        try
        {
            if (File.Exists(logFilePath))
            {
                string logContent = File.ReadAllText(logFilePath);  // `ReadAllTextAsync` hata diya
                using (HttpClient client = new HttpClient())
                {
                    var content = new StringContent(logContent, Encoding.UTF8, "text/plain");
                    HttpResponseMessage response = await client.PostAsync(serverUrl, content);

                    if (response.IsSuccessStatusCode)
                    {
                        Console.WriteLine("Log file sent successfully!");
                    }
                    else
                    {
                        Console.WriteLine($"Failed to send log: {response.StatusCode}");
                    }
                }
            }
            else
            {
                Console.WriteLine("Log file not found!");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error sending log: {ex.Message}");
        }
    }
}
