from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
import requests

Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput = "below_target"

class Ui(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrannge"
        Builder.load_file('main.kv')
        #self.url = xxx
        #self.key = xxx
        return Ui()
    

    def login_data(self):
        userx = self.root.ids.user.text
        passwordx = self.root.ids.password.text
        state = False
        data= requests.get(self.url + '?auth=' + self.key)

        for key, value in data.json().items():
            user_reg = value['User']
            password_reg = value['Password']

            if userx==user_reg:
                if passwordx == password_reg:
                    state = True
                    self.root.ids.signal_login.text = ''
                    self.root.ids.user.text = ''
                    self.root.ids.password.text = ''
                else:
                    self.root.ids.signal_login.text = 'Contraseña Incorrecta'
                    self.root.ids.user.text = ''
            else:
                self.root.ids.signal_login.text = 'Usuario Incorrecto'
                self.root.ids.user.text = ''
                self.root.ids.password.text = ''
        return state
   
    def tegister_data(self):
       state = 'datos incorretos'

       userx = self.root.ids.user.text 
       password_one = self.root.ids.new_password.text
       password_two = self.root.ids.new_password_two.text

       data = requests.get(self.url + '?auth=' + self.key)

       if password_one != password_two:
           state = 'No coinciden las contraseñas'
       elif len(userx) <= 4:
           state = "Nombre muy corto"
       elif password_one == password_two and len(password_two)<=4:
           state = 'contraseña muy corta'
       else:
           for key, value in data.json().items():
               user = value['User']
               if user == userx:
                   state = 'Este usuario ya existe'
                   break
               else:
                   state = 'Registrado correctamente'
                   data = {userx:{
                       'User': userx,
                       'Password': password_one
                   }}
                   requests.patch(url=self.url, json = data)
                   self.root.ids.signal_register.text = 'Registrado Correctamente'
               self.root.ids.signal_register.text = state
               self.root.ids.user.text = ''
               self.root.ids.new_password.text = ''
               self.root.ids.new_password_two.text = ''
               return state
           def clear_signal(self):
               self.root.ids.signal_register.text = ''
               self.root.ids.signal_login.text = ''          
    

if __name__=="__main__":
    MainApp().run()