from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
	# dataDict={}
   if request.method == 'POST':
      result = request.form
      try:
      	import socket
      	import paramiko

      except:
      	print "###############"
      	print 'This script depends on one of python library paramiko. You can install this with "pip install paramiko"'
      	print "###############"
      	return render_template("result.html",result = {"data":False,"error":"Internal Server Error"})

      serverIP=result['serverip']
      username=result['username']
      passwd=result['password']
      try:
      	socket.inet_aton(serverIP)
      	print "legal"
      except socket.error:
      	print "IP address format is not correct !!!\n please enter the correct ip address."
      	return render_template("result.html",result = {"data":False,"error":"IP address entered is invalid or not in proper format"})      	


      # result=dict(result)

      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      
      try:
      	ssh.connect(serverIP, username=username,password=passwd)
      	# pass
      except paramiko.SSHException:
      	return render_template("result.html",result = {"data":False,"error":"Connection Failed"})      	      	
      	print "Connection Failed"
      except Exception as err:
      	return render_template("result.html",result = {"data":False,"error":"Connection Failed"+str(err)})
      	print "Connection Failed",str(err)

      try:
      	stdin,stdout,stderr = ssh.exec_command("cat /etc/passwd")
      	# pass
      except:
      	return render_template("result.html",result = {"data":False,"error":"Not able to read /etc/passwd file"})      	      	
      	print "Not able to read /etc/passwd file"

      root_users=[]
      interactive_shell_user={}
      for line in stdout.readlines():
      	single_user_info=line.rstrip("\n").split(":")
      	if int(single_user_info[2])==0:
      		root_users.append(single_user_info[0])
      	if single_user_info[6] in ["/usr/sbin/nologin", "/bin/false"]:
      		pass

      	else:
      		interactive_shell_user[single_user_info[0]]=single_user_info[6]
      result={}
      # result['root_users']=['root','dipankar']
      result['root_users']=root_users
      # result['interactive_shells']={'root':'/bin/bash','dipankar':'/bin/bash'}
      result['interactive_shells']=interactive_shell_user
      result['data']=True 
      return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug = False)