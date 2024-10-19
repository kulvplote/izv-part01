#!/usr/bin/env python3
"""
IZV cast1 projektu
Autor: Veronika Simkova

Detailni zadani projektu je v samostatnem projektu e-learningu.
Nezapomente na to, ze python soubory maji dane formatovani.

Muzete pouzit libovolnou vestavenou knihovnu a knihovny predstavene na prednasce
"""
from bs4 import BeautifulSoup
import requests
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from typing import List, Callable, Dict, Any

# source env/bin/activate


def distance(a: np.array, b: np.array) -> np.array:
    diff = a - b
    diff_squared = np.sum(diff**2, axis=1)
    distances = np.sqrt(diff_squared)
    return distances


def generate_graph(
    a: List[float], show_figure: bool = False, save_path: str | None = None
):
    # f(x) = (a ** 2) * np.sin(x)
    x = np.linspace(0, 6 * np.pi, 500)
    a_array = np.array(a)[:, np.newaxis]
    f_a = a_array**2 * np.sin(x)

    # Nastavení vizualizace
    plt.figure(figsize=(14, 6))

    # Pro každý řádek v matici f_a (odpovídající každému 'a') vykreslíme graf
    for i in range(len(a)):
        plt.plot(x, f_a[i], label = f"$y_{{{a[i]}}}(x)$")
        plt.fill_between(x, f_a[i], alpha=0.1)

    # Osy a popisky s LaTeX stylem
    plt.xlabel(r"$x$", fontsize=12)
    plt.ylabel(r"$f_a(x)$", fontsize=12)

    # Rozsah osy X a Y
    plt.xlim([0, 6 * np.pi])
    plt.ylim([-max(a) ** 2 - max(a), max(a) ** 2 + max(a)])

    # Generování ticků od 0 do 6π, krok π/2
    ticks = np.arange(0, 6 * np.pi + 0.0001, np.pi / 2)

    # Odpovídající popisky od 0 do 6π včetně půlek
    tick_labels = [
        r"$0$",
        r"$\frac{\pi}{2}$",
        r"$\pi$",
        r"$\frac{3\pi}{2}$",
        r"$2\pi$",
        r"$\frac{5\pi}{2}$",
        r"$3\pi$",
        r"$\frac{7\pi}{2}$",
        r"$4\pi$",
        r"$\frac{9\pi}{2}$",
        r"$5\pi$",
        r"$\frac{11\pi}{2}$",
        r"$6\pi$",
    ]

    plt.xticks(ticks, tick_labels)

    # Přidání legendy
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)


    # Uložení grafu, pokud je zadán 'save_path'
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    # Zobrazení grafu, pokud je 'show_figure' True
    if show_figure:
        plt.show()


def generate_sinus(show_figure: bool = False, save_path: str | None = None):
        # Definování časového rozsahu t ∈ <0, 100>
    t = np.linspace(0, 100, 5000)
    
    # Definice funkcí f1(t) a f2(t)
    f1 = 0.5 * np.cos(np.pi * t / 50)
    f2 = 0.25 * (np.sin(np.pi * t) + np.sin(1.5 * np.pi * t))

    # Součet f1(t) + f2(t)
    f_sum = f1 + f2

    # Vytvoření grafu se třemi podgrafy
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True, sharey=True)
    
    # První podgraf: f1(t)
    axs[0].plot(t, f1, color="blue")
    
    # Druhý podgraf: f2(t)
    axs[1].plot(t, f2, color="blue")


    # Třetí podgraf: změna barvy součtu f1(t) + f2(t) podle f1(t)
    for i in range(len(t) - 1):
        if t[i] < 50:
            color = "green" if f_sum[i] > f1[i] else "red"
        else:
            color = "green" if f_sum[i] > f1[i] else "orange"
        
        axs[2].plot(t[i:i+2], f_sum[i:i+2], color=color, linewidth=1.5)
    

    # Nastavení popisků os
    axs[2].set_xlabel(r"$t$", fontsize=12)
    axs[0].set_ylabel(r"$f_1(t)$", fontsize=12)
    axs[1].set_ylabel(r"$f_2(t)$", fontsize=12)
    axs[2].set_ylabel(r"$f_1(t) + f_2(t)$", fontsize=12)

        # Rozsah osy X a Y
    plt.xlim([0, 100])
    plt.ylim([-0.8, 0.8])
    
    # Označení ticků na ose x
    plt.xticks(np.arange(0, 110, 25))
    plt.yticks(np.arange(-0.8, 1, 0.4))
    
    # Uložení grafu, pokud je zadán 'save_path'
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    # Zobrazení grafu, pokud je 'show_figure' True
    if show_figure:
        plt.show()


def download_data() -> Dict[str, List[Any]]:
    url = "https://ehw.fit.vutbr.cz/izv/st_zemepis_cz.html"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Invalid request')
    
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    data = {'positions': [], 'lats': [], 'longs': [], 'heights': []}
    
    table = soup.select_one("body > table:nth-child(4)")

    if not table:
        return data
    
    table_rows = table.find_all('tr')[1:]

    def convert(coord_str):
        return float(coord_str.replace(",", ".").replace("°", "").strip())

    for row in table_rows:
        cells = row.find_all('td')

        position = cells[0].get_text(strip=True)
        lat = convert(cells[2].get_text(strip=True))
        long = convert(cells[4].get_text(strip=True))
        height = convert((cells[6].get_text(strip=True)))

        data['positions'].append(position)
        data['lats'].append(lat)
        data['longs'].append(long)
        data['heights'].append(height)
    
    return data

if __name__ == "__main__":
    #generate_graph([7, 4, 3], False, "./graph.png")
    #generate_sinus(False, "./sinus.png")
    download_data()
