#!/usr/bin/python3
#I know most of you still prefer python2 and it is still more widle
#awaiable and installed by default, but I am a python starter. This is
#my fisrt real application ever, and I see no reason to learn something
#old that will wanish completely not in so faar future, instead I want
#to make sure I can put the skill I gain in use in the future easily.
#Same thing applys to the gtk3 too ^_^

#### Imports
### Backend
import sys
import os
import configparser
import io #We need to emulate a dummy [section] header for
          #configparesr to underdstand our config.txt file.
import rpiconf
###Gui
##GTK+ 3.x
from gi.repository import Gtk
##What about ncurses and QT variants too? Turn this into a full fledged
##library on handling the config file.
####

#Helper variables
raw_hdmi_mode = ['AUTO', ''] #One for resolution, one for refreshrate
advanced = False

##Load some of our widgets from the glade file to the current namespace
#Load our window from the glade/gtkbuilder file
builder = Gtk.Builder()
builder.add_from_file("mainwindow.ui")
refreshrate_box = builder.get_object("combo_refreshrate")

#Get the proper filename for our config file.
configfile = rpiconf.get_configfile(sys.argv)
# Thanks for user Tauran on stackowerflow for this hack
config_str = io.StringIO()
config_str.write('[dummy]')
config_str.write(open(configfile, 'r').read())
config_str.seek(0, os.SEEK_SET)

config_parser = configparser.ConfigParser()
config_parser.read_file(config_str)

config = rpiconf.rpi_config()
#This check whether the configfile has the option defined
#and sets it accordigly to our config object.
def populate_options(option):
	if config_parser.has_option('dummy', option):
		#I was told to be extreamly carefull with this, so I think it
		#is a bit dangerous way to do stuff. So Im more than happy
		#if someone tells me a more safer way to do this
		setattr(config , option, config_parser.get('dummy', option))

def populate_refreshrates(mode):
	# Set the refreshrate list to that of supported ones
	#Make 1st sure we are clean of the old ones
	refreshrate_box.remove_all()
	if mode != "AUTO" and mode != "VGA":
		if advanced:
			list_name = "refreshrates_" + mode + "_advanced"
		else:
			list_name = "refreshrates_" + mode
		for rate in rpiconf.refreshrates[list_name]:
			refreshrate_box.append_text(rate)


#Populate the config with all of the supported
#settings defined in our conf file
for option in rpiconf.options:
	populate_options(option)

##Define what to do, when we get a signal from the main GTK loop
class Handler:
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
		
	def on_check_refreshrate_toggled(self, button):
		global advanced
		advanced = not advanced
		populate_refreshrates(raw_hdmi_mode[0])
		
	def on_sdtv_change(self, combo):
		config.sdtv_mode = rpiconf.sdtv_modes[combo.get_active_text()]
		
	def on_aspectratio_change(self, combo):
		config.sdtv_aspect = \
			rpiconf.aspectratios[combo.get_active_text()]
			
	def on_resolution_change(self, combo):
		raw_hdmi_mode[0] = combo.get_active_text()
		populate_refreshrates(raw_hdmi_mode[0])
				
	def on_refreshrate_change(self, combo):
		raw_hdmi_mode[1] = combo.get_active_text()
		
	def on_drive_change(self, button):
		state = button.get_active()
		config.hdmi_drive = rpiconf.get_drive_mode(state)
		
	def on_top_change(self, spin):
		config.overscan_top = spin.get_value_as_int()
	def on_bottom_change(self, spin):
		config.overscan_bottom = spin.get_value_as_int()
	def on_left_change(self, spin):
		config.overscan_left = spin.get_value_as_int()
	def on_right_change(self, spin):
		config.overscan_right = spin.get_value_as_int()
		
	def on_power_change(self, combo):
		if combo.get_active_text() == "DEFAULT":
			config.hdmi_boost = 0
		else:
			# Make sure we get the value as int and not str
			# I think this might not be needed, but to be sure (HELP!)
			config.hdmi_boost = int(combo.get_active_text())

	def on_show_about(self, window):
		about = builder.get_object("aboutwindow")
		about.show_all()
	def on_print_variables(self, button):
		config.hdmi_mode = rpiconf.translate_hdmi_mode(raw_hdmi_mode)
		for option in rpiconf.options:
			print (option + " = " + str(getattr(config, option)))
	


builder.connect_signals(Handler())
window = builder.get_object("mainwindow")
window.show_all()
Gtk.main()
