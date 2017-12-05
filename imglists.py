import subprocess
import urllib, os

# C++ vector lines
cmd = ["ls", "./imgs"]
outF = open('Cpp_strVector', "w+")
wholeOut = "std::vector <String> ts;\n"
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
for line in proc.stdout.readlines():
	texto = line.decode("utf-8")
	texto = texto.rstrip('\n')
	wholeOut = wholeOut + "ts.push_back(\"home/sergio/cvws/imgs/" + texto + "\");\n"
	
outF.write(wholeOut)
outF.close()
# javaScript image collection file
cmd = ["pwd"]
locality = ''

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
for line in proc.stdout.readlines():
	texto = line.decode("utf-8")
	texto = texto.rstrip('\n')
	pathSplit = texto.split('/')
	locality = pathSplit[-1]
	print(locality)
path = 'set_' + locality + 'NoImgRepeated.js'
outF = open(path, "w+")
wholeOut = "var set_" + locality + "=[\n"
cmd = ["ls", "./imgs"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
for line in proc.stdout.readlines():
	texto = line.decode("utf-8")
	texto = texto.rstrip('\n')
	imgSplit = texto.split('_')
	lat = imgSplit[0]
	log = imgSplit[1]
	heading = imgSplit[1]
	heading = heading.split('.')[0]
	{"name":"4.63113230017_-74.0678258745_45.jpg", "lat":4.63113230017, "log":-74.0678258745, "sampletime":"2016-02", "heading":45},
	wholeOut = wholeOut + "{\"name\":" + '\"' + texto + '\",';
	wholeOut = wholeOut + "\"lat\":" + lat + ',';
	wholeOut = wholeOut + "\"log\":" + log + ',';
	wholeOut = wholeOut + "\"heading\":" + heading + '},\n';


wholeOut = wholeOut[:-2]
outF.write(wholeOut + '\n]')
outF.close()









