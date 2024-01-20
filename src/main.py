"""

    Main archive of Crimson Launcher v1.0 by @devcheckog

"""


import os
import json
import getpass
import platform
import shutil
import sys
from typing import List, Literal
import psutil
import jdk
import customtkinter
import tkinter
import signal
from PIL import Image
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
from utils import check_internet
from constants import VERSION

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    if not platform.platform().startswith('Windows'):
        messagebox.showerror(title= f'Crimson Launcher - {VERSION}', message= 'Sistema operativo incompatible.', type= 'ok')
        raise RuntimeError('Sistema operativo incompatible.')

    class CrimsonLauncher:

        def __init__(self, user : str) -> None:

            self.BASE_PATH : str = f'C:/Users/{user}/AppData/Roaming/'
            self.PATH : str = f'C:/Users/{user}/AppData/Roaming/.crimson/'
            self.CRIMSON_BACKGROUND : ThreadPoolExecutor = ThreadPoolExecutor(max_workers= 10, thread_name_prefix= 'Crimson Background Process')
            self.USER : str = user
            self.RAM_TOTAL : int  = round(0.65 * psutil.virtual_memory().total / (1024 ** 2))
            self.RAM_ASSIGNED : int = 500
            self.PATH_ASSETS : str = os.getcwd().replace('\\', '/') + '/assets'
            self.COLOR : str = '#333333'
            self.DEBUG_TERMINAL : bool = False

            self.checker()

        def java(self, version : Literal['17', '8']) -> None:

            try:
                jdk.install(version= version, operating_system= jdk.OperatingSystem.WINDOWS, path= self.PATH + 'Java/', arch= jdk.Architecture.X64)
                messagebox.showinfo(title= f'Crimson Launcher - {VERSION}', message= f'Java {version} instalado correctamente.', type = 'ok')

            except:    
                messagebox.showerror(title= f'Crimson Launcher - {VERSION}', message= f'No se logró instalar Java {version} correctamente.')
                raise RuntimeError(f'No se instaló correctamente Java {version}')    

        def checker(self) -> None:

            internet : bool = check_internet()

            if internet == False:
                messagebox.showerror(title= f'Crimson Launcher - {VERSION}', message= 'No hay conexión a internet.', type= 'ok')
                self.CRIMSON_BACKGROUND.shutdown()
                raise RuntimeError('No hay conexión a internet.')

            elif not os.path.exists(self.BASE_PATH):
                messagebox.showerror(title= f'Crimson Launcher - {VERSION}', message= f'No existe la ruta principal de programas {self.BASE_PATH}.', type= 'ok')
                self.CRIMSON_BACKGROUND.shutdown(cancel_futures= True)
                raise RuntimeError(f'No existe la ruta principal {self.BASE_PATH}')
            
            elif not os.path.exists(self.PATH):
                os.mkdir(self.BASE_PATH + '.crimson')
                os.mkdir(self.BASE_PATH + '.crimson/Crimson Settings')
                os.mkdir(self.BASE_PATH + '.crimson/Java')
                
                if not os.path.exists(self.PATH + 'Crimson Settings/config.json'):
                    with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:
                        json.dump({
                            'accounts' : {},
                            'java' : {
                                'path' : None,
                            },
                            'launcher settings' : {
                                'close_on_start' : False,
                                'ram_asigned' : 1000
                            }
                        }, write, indent= 5)

                    with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:
                        config = json.load(read)
                        self.RAM_ASSIGNED = config['launcher settings']['ram_asigned']      

                if not os.path.exists(self.PATH + 'launcher_profiles.json'):
                    with open(self.PATH + 'launcher_profiles.json', 'w') as write:
                        json.dump({
                            'profiles' : {},                  
                            'settings': {
                                'enableAdvanced': False,
                                'profileSorting': 'byName'
                            },
                            'version': 3
                        }, write, indent= 5)

                self.CRIMSON_BACKGROUND.submit(self.java, '17')
                self.start()

            else:

                if not os.path.exists(self.PATH + 'Java/'):
                    messagebox.showerror(title= f'Crimson Launcher - {VERSION}', message= f'No existe la carpeta principal de Java {self.PATH}.', type= 'ok')
                    self.CRIMSON_BACKGROUND.shutdown()
                    raise RuntimeError(f'No existe la carpeta principal de Java {self.PATH}.')
                
                if not os.path.exists(self.PATH + 'Crimson Settings/config.json'):
                    with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:
                        json.dump({
                            'accounts' : {},
                            'java' : {
                                'path' : None,
                            },
                            'launcher settings' : {
                                'close_on_start' : False,
                                'ram_asigned' : 1000
                            }
                        }, write, indent= 5)

                    with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:
                        config = json.load(read)
                        self.RAM_ASSIGNED = config['launcher settings']['ram_asigned']      

                if not os.path.exists(self.PATH + 'launcher_profiles.json'):
                    with open(self.PATH + 'launcher_profiles.json', 'w') as write:
                        json.dump({
                            'profiles' : {},                  
                            'settings': {
                                'enableAdvanced': False,
                                'profileSorting': 'byName'
                            },
                            'version': 3
                        }, write, indent= 5)

                with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:
                    config = json.load(read)
                    self.RAM_ASSIGNED = config['launcher settings']['ram_asigned']            

                jdks : List[str] = [java for java in os.listdir(self.PATH + 'Java/') if java.startswith('jdk-17') or java.startswith('jdk-8')]

                if len(jdks) == 0:
                    self.CRIMSON_BACKGROUND.submit(self.java, '17')

                else:

                    for java in jdks:

                        if not os.path.exists(self.PATH + f'Java/{java}/bin/java.exe'):
                            
                            if java.startswith('jdk-17'):  
                                shutil.rmtree(path= self.PATH + f'Java/{java}',ignore_errors= True)
                                self.CRIMSON_BACKGROUND.submit(self.java, '17')
                                break

                            elif java.startswith('jdk-8'):    
                                shutil.rmtree(path= self.PATH + f'Java/{java}',ignore_errors= True)
                                self.CRIMSON_BACKGROUND.submit(self.java, '8')
                                break

                self.start()

        def start(self) -> None:

            def terminate_start_window() -> None:

                StartWindowLoadBar.stop()
                StartWindow.quit()
                StartWindow.withdraw()

                return self.main()

            StartWindow : customtkinter.CTk = customtkinter.CTk()   
            StartWindow.title(f'Crimson Launcher - {VERSION}')
            StartWindow.config(bg= self.COLOR)
            StartWindow.resizable(False, False)
            StartWindow.geometry('580x620')
            StartWindow.wm_iconbitmap(f'{self.PATH_ASSETS}/logo.ico')
            StartWindow.wm_protocol('WM_DELETE_WINDOW', terminate_start_window)

            StartWindowImage : customtkinter.CTkLabel = customtkinter.CTkLabel(
                StartWindow,
                text= None,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/logo.png'), size= (256, 256)),
                bg_color= 'transparent',
                fg_color= self.COLOR 
            )
            StartWindowImage.pack_configure(anchor= 'center', pady= 100)
            
            StartWindowLoadBar : customtkinter.CTkProgressBar = customtkinter.CTkProgressBar(
                StartWindow,
                corner_radius= 20,
                progress_color= '#0077ff',
                orientation= 'horizontal',
                mode= 'indeterminate',
                height= 30,
                width= 300,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                indeterminate_speed= 1.2
            )
            StartWindowLoadBar.place_configure(relx= 0.2_5, rely= 0.8)
            StartWindowLoadBar.start()

            StartWindow.after(300, terminate_start_window)
            StartWindow.mainloop()

        def main(self) -> None:

            def terminate_home_window() -> None:
                
                HomeWindow.quit()
                HomeWindow.withdraw()

                return self.terminate()
           
            HomeWindow : customtkinter.CTkToplevel = customtkinter.CTkToplevel()
            HomeWindow.title(f'Crimson Launcher - {VERSION}')
            HomeWindow.config(bg= self.COLOR)
            HomeWindow.after(300, HomeWindow.iconbitmap, f'{self.PATH_ASSETS}/logo.ico')
            HomeWindow.geometry('1290x720')
            HomeWindow.minsize(1290, 720)
            HomeWindow.maxsize(1920, 1080)
            HomeWindow.protocol('WM_DELETE_WINDOW', terminate_home_window)

            CanvasLogo : customtkinter.CTkLabel = customtkinter.CTkLabel(
                HomeWindow,
                text= None,
                fg_color= self.COLOR,
                image=  customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/logo.png'), size= (160, 160)),
                bg_color= self.COLOR
            )
            CanvasLogo.place_configure(relx= 0.0_2, rely= 0.0_4, anchor= 'nw')

            Discord : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/discord.png'), size= (96, 96)),
                height= 35,
                text= None
            )
            Discord.place_configure(relx= 0.99, rely= 0.0_8, anchor= 'ne')

            Github : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/github.png'), size= (96, 96)),
                height= 35,
                text= None
            )
            Github.place_configure(relx= 0.99, rely= 0.4_8, anchor= 'e')

            Donate : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/donate.png'), size= (96, 96)),
                height= 35,
                text= None
            )
            Donate.place_configure(relx= 0.99, rely= 0.8_8, anchor= 'se')

            VersionsAndMods : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                height= 37,
                bg_color= self.COLOR,
                fg_color= '#0077ff',
                corner_radius= 20,
                text= 'Versiones y Mods',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/download.png'), size= (22, 22)),
                compound= 'left',
                font= ('Roboto', 15),
                border_width= 2,
                border_color= '#70ceff'
            )
            VersionsAndMods.place_configure(relx= 0.2_5, rely= 0.1, anchor= 'n')

            Config : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                height= 37,
                bg_color= self.COLOR,
                fg_color= '#0077ff',
                corner_radius= 20,
                text= 'Configuración',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/config.png'), size= (22, 22)),
                compound= 'left',
                font= ('Roboto', 15),
                border_width= 2,
                border_color= '#70ceff'
            )
            Config.place_configure(relx= 0.5, rely= 0.1, anchor= 'n')

            Accounts : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                height= 37,
                bg_color= self.COLOR,
                fg_color= '#0077ff',
                corner_radius= 20,
                text= 'Cuentas',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/account.png'), size= (22, 22)),
                compound= 'left',
                font= ('Roboto', 15),
                border_width= 2,
                border_color= '#70ceff'
            )
            Accounts.place_configure(relx= 0.7_5, rely= 0.1, anchor= 'n')

            FrameDecorationCenter : customtkinter.CTkFrame = customtkinter.CTkFrame(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= '#232323',
                border_color= '#0077ff',
                border_width= 2
            )
            FrameDecorationCenter.place_configure(relx= 0.09, rely= 0.9_1, anchor= 'sw', relheight= 0.6_3, relwidth= 0.7_2)

            LabelLaunch : customtkinter.CTkLabel = customtkinter.CTkLabel(
                HomeWindow,
                text= ' Lanzar',
                compound= 'left',
                font= ('Roboto', 30),
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#232323',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/launch.png'), size= (96, 96))
            )
            LabelLaunch.place_configure(relx= 0.1_3, rely= 0.4_5, anchor= 'sw')

            LaunchVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                HomeWindow,
                height= 40,
                corner_radius= 20,
                bg_color= '#232323',
                font= ('Roboto', 15),
                dropdown_font= ('Roboto', 15),
                dynamic_resizing= False,
                text_color= 'white',
                dropdown_fg_color= '#232323',
                dropdown_text_color= 'white',
                width= 210,
                fg_color= '#0077ff', 
                button_color= '#0077ff',
                values= ['Test']
            )
            LaunchVersion.place_configure(relx= 0.1_4, rely= 0.6_3, anchor= 'sw')

            OptimizationTitle : customtkinter.CTkLabel = customtkinter.CTkLabel(
                HomeWindow,
                text= ' Optimización',
                compound= 'left',
                font= ('Roboto', 30),
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#232323',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/optimize.png'), size= (96, 96))

            )
            OptimizationTitle.place_configure(relx= 0.7_6, rely= 0.4_5, anchor= 'se')

            OptimizeJavaArgs : customtkinter.CTkSwitch = customtkinter.CTkSwitch(
                HomeWindow,
                text= ' Optimizar Java',
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#0077ff',
                font= ('Roboto', 18),
                onvalue= 'si',
                offvalue= 'no',
                button_color= 'white',
                button_hover_color= 'white',
                progress_color= '#70ceff',
                height= 60,
				width= 100
            ) 
            OptimizeJavaArgs.place_configure(relx= 0.7_3, rely= 0.5_5, anchor= 'se')

            OpenOrClose : customtkinter.CTkSwitch = customtkinter.CTkSwitch(
                HomeWindow,
                text= 'abrir o cerrar al iniciar',
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#0077ff',
                font= ('Roboto', 18),
                onvalue= 'si',
                offvalue= 'no',
                button_color= 'white',
                button_hover_color= 'white',
                progress_color= '#70ceff',
                height= 60,
				width= 100
            ) 
            OpenOrClose.place_configure(relx= 0.7_5, rely= 0.6_3, anchor= 'se')
        
            HomeWindow.mainloop()
            
        def terminate(self) -> None:

            self.CRIMSON_BACKGROUND.shutdown()
            sys.exit(0)

    def get_user() -> str:

        USER : str = ''
        USERS_PATH : str = 'C:/Users'

        if not os.path.exists(USERS_PATH):
            messagebox.showerror(title= f'Crimson Launcher - {VERSION}', message= f'No existe la carpeta {USERS_PATH} del sistema.', type= 'ok')
            raise RuntimeError(f'No existe la carpeta {USERS_PATH} del sistema.')
        
        for user in [username for username in os.listdir('C:/Users') if username.find('.') == -1 and username == 'ingke' or username == getpass.getuser() or username == getpass.getuser().lower()]:

            if os.path.exists(f'C:/Users/{user}/AppData/Roaming/'):
                USER = user
                break

        return USER
    
    CrimsonLauncher(get_user())
    
    sys.exit(0)
