import requests
from colorama import Fore, Style, init as colorama_init
from datetime import datetime, timedelta
from pytz import timezone

colorama_init()

def print_rainbow_ascii_art(art):
    """
    Prints ASCII art with rainbow colors
    """
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    for i, line in enumerate(art):
        color = colors[i % len(colors)]
        print(f"{color}{line}{Style.RESET_ALL}")

def search_engine(query, num_results, engine, api_key):
    api_url = f'https://serpapi.com/search.json?engine={engine}&q={query}&num={num_results}&api_key={api_key}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        results = data.get('organic_results', [])

        if results:
            return [(result.get('title', ''), result.get('link', '')) for result in results]
        else:
            print("No search results found.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return []

def write_results_to_file(results, engine_name):
    brasilia_timezone = timezone('America/Sao_Paulo')
    brasilia_time = datetime.now(brasilia_timezone)

    with open('results.txt', 'w', encoding='utf-8') as f:
        f.write(f'{Fore.YELLOW}[Resultados {engine_name}] [Total {len(results)} links] [Dia {brasilia_time.strftime("%d/%m/%Y")} Hora: {brasilia_time.strftime("%H:%M")}]{Style.RESET_ALL}\n')
        f.write(f'{Fore.CYAN}+====================================================================================+{Style.RESET_ALL}\n')
        f.write(f'{Fore.CYAN}|{Style.RESET_ALL}{Fore.GREEN}{"Título": <30} {Style.RESET_ALL}| {Fore.GREEN}{"URL": <50}{Style.RESET_ALL}|\n')
        f.write(f'{Fore.CYAN}+================================+===================================================+{Style.RESET_ALL}\n')
        for i, result in enumerate(results, start=1):
            f.write(f'{Fore.CYAN}|{Style.RESET_ALL}{Fore.GREEN}{i: >2}. {result[0][:27]: <27} | {result[1][:50]: <50}{Style.RESET_ALL}|\n')
        f.write(f'{Fore.CYAN}+================================+===================================================+{Style.RESET_ALL}\n')
        f.write(f'{Fore.RED}Criado por David A. Mascaro{Style.RESET_ALL}\n')

def main():
    # Rainbow color codes
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

    # ASCII art
    art = [
        "  _____  _____   _____         ____   _____ _____ _   _ _______ ",
        " |  __ \\|  __ \\ / ____|       / __ \\ / ____|_   _| \\ | |__   __|",
        " | |  | | |  | | |  __ ______| |  | | (___   | | |  \\| |  | |   ",
        " | |  | | |  | | | |_ |______| |  | |\\___ \\  | | | . ` |  | |   ",
        " | |__| | |__| | |__| |      | |__| |____) |_| |_| |\\  |  | |   ",
        " |_____/|_____/ \\_____|       \\____/|_____/|_____|_| \\_|  |_|   "
    ]

    print_rainbow_ascii_art(art)

    query = input(f'{Fore.YELLOW}Digite a sua busca: {Style.RESET_ALL}')
    num_results = int(input(f'{Fore.YELLOW}Quantos resultados você deseja? {Style.RESET_ALL}'))
    engine_choice = input(f'{Fore.YELLOW}Escolha o motor de busca (Google ou DuckDuckGo): {Style.RESET_ALL}').lower()

    if engine_choice not in ['google', 'duckduckgo']:
        print(f"{Fore.RED}Opção de motor de busca inválida. Escolha entre Google ou DuckDuckGo.{Style.RESET_ALL}")
        return

    api_key = "8c9f728b3dae4bbbef4f0639f9ddda797ae933a9cc1adf0ea2ccab8d0d61434d"  # Replace with your actual Serpapi API key

    results = search_engine(query, num_results, engine_choice, api_key)

    if results:
        print(f'\n{Fore.GREEN}Resultados da busca:{Style.RESET_ALL}\n')
        write_results_to_file(results, engine_choice.capitalize())
    else:
        print(f'{Fore.RED}Nenhum resultado encontrado.{Style.RESET_ALL}')

if __name__ == "__main__":
    main()
