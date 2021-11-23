#disable logging
from os import environ
environ["KIVY_NO_CONSOLELOG"] = '1'

from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.switch import Switch
from kivy.uix.button import Button
from pathlib import Path
from util import start_script


class CityTextInput(TextInput):
    cities = []

    def addCity(self, cbox, label, city, app):
        if city and not cbox.active:
            self.cities.append(city)
            label.text += f'[ref={city}]{city}, [/ref]'
            app.filter_dict['Cities']['chosen'] = self.cities
            app.filter_dict['Cities']['allChosen'] = False
            self.text = ''
    def removeCity(self, cbox, label, city, app):
        if not cbox.active:
            self.cities.remove(city)
            label.text = label.text.replace(f'{city}, ', '') 
            app.filter_dict['Cities']['chosen'] = self.cities
            app.filter_dict['Cities']['allChosen'] = False

    def toggleAll(self, cbox, label, app):
        if cbox.active:
            label.text = 'Canada'
            self.cities = []
            app.filter_dict['Cities']['chosen'] = self.cities
            app.filter_dict['Cities']['allChosen'] = True

        else:
            label.text = ''
            app.filter_dict['Cities']['allChosen'] = False




class CTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = ''.join([i for i in substring if i.isdigit()])
        return super().insert_text(s, from_undo=from_undo)
    

    def update_dict(self, app, start_or_end, text, cbox):
        cbox.active = False
        d = app.filter_dict['Price Range']
        int_val = int(text) if text else 0
        d[start_or_end] = int_val
        d['allChosen'] = cbox.active
        app.update_filter_dict('Price Range', d)


class CCheckBox(CheckBox):
    def toggleAll(self, ids, cbox, app):
        for i in ids:
            i.text = ''
        cbox.active = True
        app.filter_dict['Price Range']['allChosen'] = cbox.active



class DCheckBox(CheckBox):
    def toggleAll(self, ids, cbox, app, key):
        for i in ids:
            i.text = ''
        cbox.active = True
        app.filter_dict[key]['allChosen'] = cbox.active

class DTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = ''.join([i for i in substring if i.isdigit() or i == '/'])
        return super().insert_text(s, from_undo=from_undo)
    

    def update_dict(self, app, start_or_end, text, cbox, key):
        cbox.active = False
        d = app.filter_dict[key]
        d[start_or_end] = text
        d['allChosen'] = cbox.active
        app.update_filter_dict(key, d)


class MyButtonLayout(GridLayout):
    def update_for_rent_by_dict(self, app):
        chosen = ''
        for i in self.ids:
            e = self.ids[i]
            if e.state == 'down':
                chosen = e.text

        if chosen == 'No Preference':
            app.filter_dict['For Rent By']['allChosen'] = True

        else:
            app.filter_dict['For Rent By']['allChosen'] = False
            app.filter_dict['For Rent By']['chosen'] = chosen


    def update_dict(self, app):
        app.filter_dict['Unit Type']['chosen'] = []
        if self.ids['No Preference'].state == 'down':
            app.filter_dict['Unit Type']['allChosen'] = True
            
        else:
            for i in self.ids:
                element = self.ids[i]
                if element.state == 'down':
                    app.filter_dict['Unit Type']['chosen'].append(element.text)

            app.filter_dict['Unit Type']['allChosen'] = False


    def toggleAll(self, app, for_rent_by = False):
        for i in self.ids:
            if i != 'No Preference':
                self.ids[i].state = 'normal'
        if for_rent_by:
            self.update_for_rent_by_dict(app)
        else:
            self.update_dict(app)


    def toggleNoPref(self, app, for_rent_by = False):
        self.ids['No Preference'].state = 'normal'
        if for_rent_by:
            self.update_for_rent_by_dict(app)
        else:
            self.update_dict(app)

class NewButtonLayout(GridLayout):
    def update_for_rent_by_dict(self, app):
            chosen = ''
            for i in self.ids:
                e = self.ids[i]
                if e.state == 'down':
                    chosen = e.text

            if chosen == 'No Preference':
                app.filter_dict['For Rent By']['allChosen'] = True

            else:
                app.filter_dict['For Rent By']['allChosen'] = False
                app.filter_dict['For Rent By']['chosen'] = chosen


    def update_dict(self, app):
        app.filter_dict['Unit Type']['chosen'] = []
        if self.ids['No Preference'].state == 'down':
            app.filter_dict['Unit Type']['allChosen'] = True
            
        else:
            for i in self.ids:
                element = self.ids[i]
                if element.state == 'down':
                    app.filter_dict['Unit Type']['chosen'].append(element.text)

            app.filter_dict['Unit Type']['allChosen'] = False


    def toggleAll(self, app, for_rent_by = False):
        for i in self.ids:
            if i != 'No Preference':
                self.ids[i].state = 'normal'
        if for_rent_by:
            self.update_for_rent_by_dict(app)
        else:
            self.update_dict(app)


    def toggleNoPref(self, app, for_rent_by = False):
        self.ids['No Preference'].state = 'normal'
        if for_rent_by:
            self.update_for_rent_by_dict(app)
        else:
            self.update_dict(app)




class StartButton(Button):
    def startScript(self, filter_dict, app):
        self.disabled = True
        self.text = 'Running...'
        return start_script(filter_dict, app)

class MySwitch(Switch):
    def handleToggle(self, _, active, app):
        app.filter_dict['Options']['continueFile'] = active


class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args, **kwargs):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args, **kwargs)
        return super(ShowcaseScreen, self).add_widget(*args, **kwargs)



class ShowcaseApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])
    
    title = 'Web Scraper'

    
    filter_dict = {
        'Unit Type': {
            'allChosen': True,
        },
        'Price Range': {
            'allChosen': True,
        },
        'For Rent By': {
            'allChosen': True,
        },
        'Cities': {
            'allChosen': True,
        },
        'Move-In Date': {
            'allChosen': True,
        },    
        'Date Posted': {
            'allChosen': True,
        }, 
        'Options': {

        } 
    } 

    
    def update_filter_dict(self, key, value):
        self.filter_dict[key] = value


    def build(self):
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}

        def swap(a, x,y):
            a[x],a[y]=a[y],a[x]

        self.available_screens = [p.name.split('.kv')[0] for p in Path('./frontend/data/screens').glob('*.kv')]
        try:
            #move start to end
            swap(self.available_screens, self.available_screens.index('Start'), -1)
        except:
            pass

        
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
            '{}.kv'.format(fn).lower()) for fn in self.available_screens]

        self.go_next_screen()

    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        self.update_sourcecode()

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

    def toggle_start(self):
        try:
            return self.go_screen(len(self.available_screens) - 1)
        except ValueError:
            pass

    def read_sourcecode(self):
        fn = self.available_screens[self.index]
        with open(fn) as fd:
            return fd.read()

    def toggle_source_code(self):
        self.show_sourcecode = not self.show_sourcecode
        if self.show_sourcecode:
            height = self.root.height * .3
        else:
            height = 0

        Animation(height=height, d=.3, t='out_quart').start(
                self.root.ids.sv)

        self.update_sourcecode()

    def update_sourcecode(self):
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1

    def showcase_floatlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 5:
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
#:import random random.random
Button:
    size_hint: random(), random()
    pos_hint: {'x': random(), 'y': random()}
    text:
        'size_hint x: {} y: {}\\n pos_hint x: {} y: {}'.format(\
            self.size_hint_x, self.size_hint_y, self.pos_hint['x'],\
            self.pos_hint['y'])
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_boxlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 5:
                layout.orientation = 'vertical'\
                    if layout.orientation == 'horizontal' else 'horizontal'
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_gridlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 15:
                layout.rows = 3 if layout.rows is None else None
                layout.cols = None if layout.rows == 3 else 3
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text:
        'rows: {}\\ncols: {}'.format(self.parent.rows, self.parent.cols)\
        if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_stacklayout(self, layout):
        orientations = ('lr-tb', 'tb-lr',
                        'rl-tb', 'tb-rl',
                        'lr-bt', 'bt-lr',
                        'rl-bt', 'bt-rl')

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 11:
                layout.clear_widgets()
                cur_orientation = orientations.index(layout.orientation)
                layout.orientation = orientations[cur_orientation - 1]
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
    size_hint: .2, .2
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_anchorlayout(self, layout):

        def change_anchor(self, *l):
            if not layout.get_parent_window():
                return
            anchor_x = ('left', 'center', 'right')
            anchor_y = ('top', 'center', 'bottom')
            if layout.anchor_x == 'left':
                layout.anchor_y = anchor_y[anchor_y.index(layout.anchor_y) - 1]
            layout.anchor_x = anchor_x[anchor_x.index(layout.anchor_x) - 1]

            Clock.schedule_once(change_anchor, 1)
        Clock.schedule_once(change_anchor, 1)

    def _update_clock(self, dt):
        self.time = time()


if __name__ == '__main__':
    ShowcaseApp().run()
