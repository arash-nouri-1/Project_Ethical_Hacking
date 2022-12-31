import base64
import github3
import json
from rich.console import Console
from rich.table import Table


def github_connect():
    with open("mytoken.txt") as f:
        token = f.read()
    user = "arash-nouri-1"
    sess = github3.login(token=token)
    return sess.repository(user, "Project_Ethical_Hacking")


def get_file_contents(file):
    repo = github_connect()
    contents = repo.file_contents("data/config/" + file)
    raw_data = base64.b64decode(contents.content)
    raw_data = base64.b64decode(raw_data)
    return raw_data


def convert_to_json(raw_data):
    raw_data = raw_data.decode()
    raw_data = raw_data[1:-1]
    results = json.loads(raw_data)
    return results


def print_to_console(results):
    # Create table 1 for network results
    console = Console()
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
            table.add_row(key, value["IP"], str(
                value["Open ports"]), value["OS"])

    # Create table 2 for localhost results
    console2 = Console()
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
            table2.add_row(
                value["System name"],
                value["Hostname"],
                value["Username"],
                str(value["CPU usage (%)"]),
                str(value["Memory usage (MB)"]),
                str(value["Network usage"]),
                str(value["Disk usage (GB)"]),
            )

    console.print(table)
    console2.print(table2)


def main():
    console = Console()
    console.clear()
    console.print(
        "Welcome to the log file reader. Type 'exit' if you want to quit. Please enter the file name you want to read:",
        style="bold purple",
    )
    user_input = input()
    while user_input != "exit":
        try:
            raw_data = get_file_contents(user_input)
            results = convert_to_json(raw_data)
            print_to_console(results)
        except FileNotFoundError:
            console.print("File not found. Please try again", style="bold red")
        except Exception as e:
            console.print("An error occurred", e, style="bold red")
        console.print(
            "Please enter the file name you want to read: ", style="bold purple"
        )
        user_input = input()
    console.print(
        "Thank you for using the log file reader. Goodbye!", style="bold purple"
    )


if __name__ == "__main__":
    main()
