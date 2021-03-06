import os
import configparser
import io #We need to emulate a dummy [section] header for
          #configparesr to underdstand our config.txt file.


#Some lists of options
options = ['arm_freq', 'gpu_freq', 'core_freq', 'h264_freq', 
'isp_freq', 'v3d_freq', 'sdram_freq', 'over_voltage', 
'over_voltage_sdram', 'over_voltage_sdram_c', 'over_voltage_sdram_i', 
'over_voltage_sdram_p', 'sdtv_mode', 'sdtv_aspect', 'hdmi_mode', 
'hdmi_drive', 'hdmi_boost', 'disable_overscan','overscan_left',
'overscan_right', 'overscan_top', 'overscan_bottom',
'framebuffer_width', 'framebuffer_height', 'test_mode', 'enable_l2cache']

sdtv_modes={'NTSC' : 0, 'NTSC-J' : 1, 'PAL' : 2, 'PAL-M' :3}
aspectratios={'4:3' : 1, '14:9' : 2, '16:9' : 3}

hdtv_resolutions=['VGA', '240p', '288p', '480i', '480p', '576i', \
'576p', '720p', '1080i', '1080p']

hdtv_modes={'VGA' : 1, '480p60' : 2, '480p60H' : 3, '720p60' : 4, 
'1080i60' : 5, '480i60' : 6, '480i60H' : 7, '240p60' : 8, 
'240p60H' : 9, '480i60_4x' : 10, '480i60_4xH' : 11, '240p60_4x' : 12, 
'240p60_4xH' : 13, '480p60_2x' : 14, '480p60_2xH' : 15, 
'1080p60' : 16, '576p50' : 17, '576p50H' : 18, '720p50' : 19, 
'1080i50' : 20, '576i50' : 21, '576i50H' : 22, '288p50' : 23, 
'288p50H' : 24, '576i50_4x' : 25, '576i50_4xH' : 26, '288p50_4x' : 27, 
'288p50_4xH' : 28, '576p50_2x' : 29, '576p50_2xH' : 30, 
'1080p50' : 31, '1080p24' : 32, '1080p25' : 33, '1080p30' : 34, 
'480p60_4x' : 35, '480p60_4xH' : 36, '576p50_4x' : 37, 
'576p50_4xH' : 38, '1080i50_rb' : 39, '1080i100' : 40, '720p100' : 41, 
'576p100' : 42, '576p100H' : 43, '576i100' : 44, '576i100H' : 45, 
'1080i120' : 46, '720p120' : 47, '480p120' : 48, '480p120H' : 49, 
'480i120' : 50, '480i120H' : 51, '576p200' : 52, '576p200H' : 53, 
'576i200' : 54, '576i200H' : 55, '480p240' : 56, '480p240H' : 57, 
'480i240' : 58, '480i240H' : 59}

##Usable refreshrates by resolution
refreshrates = {
'refreshrates_240p' : ['60'] ,
'refreshrates_240p_advanced' : ['60', '60H', '60_4x', '60_4xH'] ,
'refreshrates_288p' : ['50'] ,
'refreshrates_288p_advanced' : ['50', '50H', '50_4x', '50_4xH'] ,
'refreshrates_480i' : ['60', '120', '200'] ,
'refreshrates_480i_advanced' : ['60', '60H', '60_4x', '60_4xH', 
                              '120', '120H', '240', '240H'] ,
'refreshrates_480p' : ['60', '120', '200'] ,
'refreshrates_480p_advanced' : ['60', '60H', '60_2x', '60_2xH', 
                              '60_4x', '60_4xH', '120', '120H', 
                              '240', '240H'] ,
'refreshrates_576i' : ['50', '100', '200'] ,
'refreshrates_576i_advanced' : ['50', '50H', '50_4x', '50_4xH', 
                              '100', '100H', '200', '200H'] ,
'refreshrates_576p' : ['50', '100', '200'] ,
'refreshrates_576p_advanced' : ['50', '50H', '50_2x', '50_2xH', 
                              '50_4x', '50_4xH', '100', '100H', 
                              '200', '200H'] ,
'refreshrates_720p' : ['50', '60', '100', '120'] ,
'refreshrates_720p_advanced' : ['50', '60', '100', '120'] ,
'refreshrates_1080i' : ['50', '60', '100', '120'] ,
'refreshrates_1080i_advanced' : ['50', '50_rb', '60', '100', '120'] ,
'refreshrates_1080p' : ['24', '25', '30', '50', '60'] ,
'refreshrates_1080p_advanced' : ['24', '25', '30', '50', '60'] }


####Configfile variables object/class
###Overclocking stuff
##Set voltage/frewuency variables to 0
##0 is a no go value for all of them, so
##we can exclude them from the saved file
##if == 0
class rpi_config:
####Start Variables###################################################
	arm_freq = 0 #Arm CPU core frequency
	             #Default is 700

	gpu_freq = 0   #Sets all 4 following at same time
	               #Defaults to 250
	core_freq = 0  #General GPU core frequency
	               #Default is 250.
	h264_freq = 0  #Sets the video decoder frequency
	               #Default is 250.
	isp_freq = 0   #Image sensor pipeline frequency
	               #Default is 250.
	v3d_freq = 0   #Frequency of the 3D builder
	               #Default 250.

	sdram_freq = 0 #Frequency of the SDRAM memory chip
	               #Default 400.

	over_voltage = 0 #ARM/GPU core voltage adjust.
	                 #[-16,8] equates to [0.8V,1.4V].
	                 #This rule applys to all of the voltages.
	                 #Default 0 (1.2V)

	over_voltage_sdram = 0   #Sets all voltage variables
	                         #Default is 0 (1.2V)
	over_voltage_sdram_c = 0 #SDRAM controller voltage adjust.
	                         #Default is 0 (1.2V)
	over_voltage_sdram_i = 0 #SDRAM I/O voltage adjust.
	                         #Default is 0 (1.2V)
	over_voltage_sdram_p = 0 #SDRAM phy voltage adjust.
	                         #Default is 0 (1.2V)
	###Video output stuff
	sdtv_mode = 0   #composite tv mode. Default is 0 (NTSC)
	sdtv_aspect = 0 #composite aspect ratio. Default is 1 (4:3)
	hdmi_mode = 0   #hdmi mode. Default is negotiated with display.
	hdmi_drive = 0  #hdmi port outputs HDMI(2)/DVI(1) signal
	                #Default to HDMI as it is HDMI port ^_^
	hdmi_boost = 0  #Not documented offically anywhere. Use 0 and
					#exclude from config at save time. HDMI signal power

	disable_overscan = 0#Disables the overscanning when set to 1
	overscan_left = 0   #number of pixels to skip on left
	overscan_right = 0  #number of pixels to skip on right
	overscan_top = 0    #number of pixels to skip on top
	overscan_bottom = 0 #number of pixels to skip on bottom
	                    #Assume we have a sane display,
	                    #which doens't need any overscanning.

	framebuffer_width = 0  #console framebuffer width in pixels.
	                       #Default matches display.
	framebuffer_height = 0 #console framebuffer height in pixels.
	                       #Default matches display.
	###Misc options
	test_mode = 0 #enable test sound/image during boot
	enable_l2cache = 0 #enable arm access to GPU's L2 cache.
					   #Needs corresponding L2 enabled kernel.Default 0
	###Non options variables
	configfile = '' #filename of the file to save into.
	parser = configparser.ConfigParser()
	#Write a header telling this app was used
	generated_config = (
	"#This config file was generated by rpiconf. rpiconf developper(s) may not\n\
#be held responsible for any damage caused by a malformated config file.\n\
#For more information visit our website \n\
#https://github.com/Huulivoide/rpiconf\n\n\n")
####End Variables#####################################################
####Start functions###################################################

	def read_config(self):
		# Thanks for user Tauran on stackowerflow for this hack
		config_str = io.StringIO()
		config_str.write("[dummy]\n")
		if os.path.isfile(self.configfile):
			config_str.write(open(self.configfile, 'r').read())
		config_str.seek(0, os.SEEK_SET)
		self.parser.read_file(config_str)

	def overscan_state(self):
		if self.overscan_bottom == 0 and self.overscan_top == 0 and \
		self.overscan_left == 0 and self.overscan_right == 0:
				self.disable_overscan = 1
		else:
			self.disable_overscan = 0

	def use_unified_voltages(self, use_individual):
		if use_individual == False:
			self.over_voltage_sdram = 0
		else:
			self.over_voltage_sdram_c = 0
			self.over_voltage_sdram_i = 0
			self.over_voltage_sdram_p = 0
	def use_unified_freq(self, use_individual):
		if use_individual == False:
			self.gpu_freq = 0
		else:
			self.core_freq = 0
			self.h264_freq = 0
			self.isp_freq = 0
			self.v3d_freq = 0

	def translate_hdmi_mode(self, raw_mode):
		if raw_mode[0] == "AUTO":
			self.hdmi_mode = 0
		elif raw_mode[0] == "VGA":
			self.hdmi_mode = 1
		elif raw_mode[0] == "":
			self.hdmi_mode = 0
		elif raw_mode[0] != "":
			self.hdmi_mode = hdtv_modes[str(raw_mode[0]) + \
										str(raw_mode[1])]

#Check if config file was giveb as argument or if a /boot/config.txt
#exists. Return the filename as a string.
	def get_configfile(self, _file):
		BOOT_FILE_EXIST = os.path.isfile("/boot/config.txt")
		FILE_EXISTS = os.path.isfile(_file)
		if FILE_EXISTS:
			self.configfile = _file
		elif BOOT_FILE_EXIST:
			self.configfile = "/boot/config.txt"
		else:
			self.configfile = "config.txt"

	def include_option(self):
		for option in options:
			#Make 100% sure we get the value in string format
			value = str(getattr(self, option))
			if value != "0":
				self.generated_config += (option + "=" + value + '\n')
			else:
				self.generated_config += ("#Value of '" + option
					+ "' not defined! Exluding it from config file!\n")

####End functions#####################################################
