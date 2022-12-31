from rich.table import Table
from rich.console import Console

results = [
   {
      "Host0":{
         "IP":"192.168.0.1",
         "Open ports":[
            53
         ],
         "OS":"Linux"
      }
   },
   {
      "Host2":{
         "IP":"192.168.0.176",
         "Open ports":[
            135,
            139,
            445,
            554
         ],
         "OS":"Windows"
      }
   },
   {
      "Localhost":{
         "System name":"Windows",
         "Hostname":"DESKTOP-2Q7IGDN",
         "Username":"arash",
         "CPU usage (%)":8.5,
         "Memory usage (MB)":5215.13671875,
         "Network usage":{
            "Bytes sent":217423925,
            "Bytes received":1597674033
         },
         "Disk usage (GB)":407.8482971191406
      }
   }
]

console = Console()

# Create table for network scan results
table = Table(show_header=True, header_style="bold purple")
table.add_column("Host", style="dim", width=20)
table.add_column("IP", style="dim", width=20)
table.add_column("Open Ports", style="dim", width=30)
table.add_column("OS", style="dim", width=20)

# Add the results to the table
for result in results:
    for key, value in result.items():
        if key == "Localhost":
            continue
        table.add_row(key, value["IP"], str(value["Open ports"]), value["OS"])

console2 = Console()

# Create a table for localhost results
table2 = Table(show_header=True, header_style="bold green")
table2.add_column("System name", style="dim", width=20)
table2.add_column("Hostname", style="dim", width=20)
table2.add_column("Username", style="dim", width=20)
table2.add_column("CPU usage (%)", style="dim", width=20)
table2.add_column("Memory usage (MB)", style="dim", width=20)
table2.add_column("Network usage", style="dim", width=20)
table2.add_column("Disk usage (GB)", style="dim", width=20)

# Add the results to the table
for result in results:
    for key, value in result.items():
        if key != "Localhost":
            continue
        table2.add_row(value["System name"], value["Hostname"], value["Username"], str(value["CPU usage (%)"]), str(value["Memory usage (MB)"]), str(value["Network usage"]), str(value["Disk usage (GB)"]))

console.print(table)
console2.print(table2)
