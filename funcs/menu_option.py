import subprocess
import winreg

def create_menu_option(name, command, icon, extension):
    HK_ROOT_shell = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{extension}\\shell")
    winreg.CloseKey(HK_ROOT_shell)

    HK_ROOT = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{extension}\\shell\\{name}")
    winreg.SetValue(HK_ROOT, "", winreg.REG_SZ, name)
    winreg.SetValueEx(HK_ROOT, "Icon", 0, winreg.REG_SZ, icon)
    winreg.SetValueEx(HK_ROOT, "MUIVerb", 0, winreg.REG_SZ, name)
    winreg.CloseKey(HK_ROOT)

    HK_ROOT_COMMAND = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{extension}\\shell\\{name}\\command")
    winreg.SetValue(HK_ROOT_COMMAND, "", winreg.REG_SZ, command)
    winreg.CloseKey(HK_ROOT_COMMAND)

def borrar_menu_option(name, extension):
    ruta = f"HKCR\\{extension}\\shell\\{name}"
    try:
        subprocess.run(
            f"reg delete \"{ruta}\" /f",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"[✓] Eliminada: {ruta}")
    except subprocess.CalledProcessError as e:
        if "el sistema no puede encontrar el archivo especificado" in e.stderr.decode().lower():
            print(f"[ ] No existe: {ruta}")
        else:
            print(f"[!] Error en {ruta}: {e.stderr.decode().strip()}")

if __name__ == "__main__":
    create_menu_option(
        "carpeta",
        r'C:\Users\Edouard\Documents\curso de programacion\Python\aplicaciones\Regedit Changer\funcs\compilar_carpeta.bat "%v"',
        r"C:\Users\Edouard\Documents\curso de programacion\Python\API's\Acelerador-de-descargas\Acelerador de descargas.exe",
        r'Python.File\Shell\Crear ejecutable'
    )
    # create_folder_shortcut(
    #     nombre="Acelerador de descargas",
    #     carpeta_destino=r"C:\Users\Edouard\Documents\curso de programacion\Python\API's\Acelerador-de-descargas",
    #     icono=r"C:\Users\Edouard\Documents\curso de programacion\Python\API's\Acelerador-de-descargas\Assets\img\descargas.ico"  # Ícono por defecto
    # )