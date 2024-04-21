import os
import shutil
import subprocess
import requests
import winreg
import ctypes

def download_registry_file(url, download_path):
    # Получаем содержимое файла по ссылке
    response = requests.get(url)
    if response.status_code == 200:
        # Определяем путь для сохранения файла
        file_path = os.path.join(download_path, "game_settings.reg")
        # Записываем содержимое файла
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path
    else:
        print("Не удалось загрузить файл.")
        return None

def import_registry_settings(reg_file):
    # Получаем полный путь к файлу reg.exe
    reg_exe_path = ctypes.windll.advapi32.GetFullPathNameW("reg.exe", 0, None)
    if reg_exe_path:
        # Формируем команду для выполнения с правами администратора
        command = f'runas /user:Administrator "{reg_exe_path}" import "{reg_file}"'
        try:
            # Запускаем команду с правами администратора
            subprocess.run(command, shell=True, check=True)
            print("Настройки успешно импортированы в реестр Windows.")
        except subprocess.CalledProcessError:
            print("Ошибка при импорте настроек в реестр Windows.")
            choice = input("Хотите внести настройки вручную? (да/нет): ")
            if choice.lower() == "да":
                print("Откройте файл game_settings.reg и выполните внесение настроек вручную.")
            else:
                print("Продолжение работы без внесения настроек в реестр.")
    else:
        print("Ошибка при получении пути к reg.exe.")

def launch_game(game_exe_path):
    # Запускаем Steam или игру
    try:
        subprocess.Popen([game_exe_path])
        print("Игра запущена.")
    except FileNotFoundError:
        print("Файл игры не найден.")

def main():
    # Запрашиваем путь для сохранения .reg файла
    download_path = input("Введите путь для сохранения файла: ")
    # Скачиваем .reg файл по предоставленной ссылке
    reg_file_path = download_registry_file("https://drive.google.com/uc?export=download&id=1IGENwFzLm8bBEboISadYSNEdxbnjz1fH", download_path)
    if reg_file_path:
        # Импортируем настройки из .reg файла в реестр Windows
        import_registry_settings(reg_file_path)
        # Запрашиваем путь к исполняемому файлу игры
        game_exe_path = input("Введите путь до исполняемого файла игры (.exe): ")
        # Запускаем игру
        launch_game(game_exe_path)

if __name__ == "__main__":
    main()
