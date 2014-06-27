import os
import string
import codecs
import math

folder_in = 'wrl_files_here/'
filename_out = ""
gamma_factor = 2.2

def sRGB2Linear(_float_val):
	_linear_val = math.pow(_float_val, gamma_factor)
	return _linear_val

def main():
	filename_list = os.listdir(folder_in)
	for filename_in in filename_list:
		if filename_in.find('.wrl') >= 0:
			filename_out = filename_in.replace('.wrl', '_linear.wrl')
			f = codecs.open(folder_in + filename_in, 'r')
			f_out = codecs.open(folder_in + filename_out, 'w')
			vertex_color_start = False
			for line in f:
				line_out = ''
				if vertex_color_start:
					if line.find(']') >= 0 and line.find('}') >= 0:
						vertex_color_start = False
						print('End of color vertex block!')

					line_t = string.split(line.replace('\t', ' ').replace(']', ' ').replace('}', ' ').strip(), ' ')
					for word in line_t:
						word = word.replace(',', '')
						float_val = sRGB2Linear(float(word))
						line_out += str(float_val) + ' '

				if line_out != '':
					if vertex_color_start:
						line_out += ','
					else:
						line_out += '] }'
					line_out = '          ' + line_out + '\n'
				else:
					line_out = line

				f_out.write(line_out)

				if line.find('color') >= 0 and line.find('Color') >= 0 and line.find('{') >= 0 and line.find('['):
					vertex_color_start = True
					print('Found a color vertex block!')

			f.close()
			f_out.close()
main()