#!/usr/bin/python
class Var:
      nameA='SH.py'  #nameA!  
      nameB=19.65  #nameB! 
class MD:
	pass
class PIP:
	pass
# class sdist(MD,PIP,initQ):
class sdist(MD,PIP):
      import os
      ########################################################################
      VVV=True
     
      dir = Var.nameA.rstrip(".py")  if Var.nameA!=None else "cmds"     
from pip._internal.cli.main import *
              


    
# # 抽出第一個 ###########################
# # sys.argv.pop(0)
# sys.argv=["(小貓檔案)",sys.argv.pop(1)]
# #########################################


print("@週期::","sys.argv")
import sys
print("@週期 BL::",  "sys.argv" in os.environ.keys()  )
###################################################
import os;
if not "TEMP" in os.environ.keys():
    os.environ[ "TEMP" ] = "/tmp" 
###################################################
import os,sys
# 會建立這兩個
# @ 建立tmp :: ['C:\\Users\\moon\\AppData\\Local\\Temp\\pip-install-oukmky1z\\sh-py_fbdafa43643a430fb77beb3cf30172f2\\setup.py', 'egg_info', '--egg-base', 'C:\\Users\\moon\\AppData\\Local\\Temp\\pip-pip-egg-info
# @ 建立tmp :: ['C:\\Users\\moon\\AppData\\Local\\Temp\\pip-install-oukmky1z\\sh-py_fbdafa43643a430fb77beb3cf30172f2\\setup.py', 'bdist_wheel', '-d', 'C:\\Users\\moon\\AppData\\Local\\Temp\\pip-wheel-l_q1vm4y']
# print("@ 建立tmp ::",sys.argv)
###############################################
# if not "Email" in os.environ.keys():
# if 'install' in sys.argv:


print("@週期9991111111111111111::",sys.argv)
if 'clean' in sys.argv:

    # if os.name=="nt":
        # open(__file__,"w").write("print(123456789)")
        # os.system("notepad "+__file__)

    pass
if 'egg_info' in sys.argv:
    os.system("notepad "+__file__) ## 打開文件
    if os.name=="nt":
        import os,re
        QFF = os.path.dirname(__file__).split("pip-install")[0]
        QPIP = os.environ[ "TEMP" ]
        # print("@ RE @...",  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i)]  )
        # # pip-unpack
        # print("@ RE @ pip-unpack...",  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i) if not re.findall("pip-install-.+",i) if not re.findall("pip-pip-egg-info-.+",i)]  )
        # # for i in  [i for i in os.listdir( QPIP )if re.findall("pip-unpack-.+",i)]:

        for i in  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i) if not re.findall("pip-install-.+",i) if not re.findall("pip-pip-egg-info-.+",i) if not re.findall("pip-req-tracker-.+",i)]:
            # print("@ DD @ ", f"rmdir /q /s  {QFF}{ i }" )
            os.system(f"rmdir /q /s  {QFF}{ i }") ## DEL
    
    if os.name=="posix":
        pass
        import os,re
        QFF = os.path.dirname(__file__).split("pip-install")[0]
        QPIP = os.environ[ "TEMP" ]
        # for i in  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i)]: ### 全部刪除
        for i in  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i) if not re.findall("pip-install-.+",i) if not re.findall("pip-pip-egg-info-.+",i) if not re.findall("pip-req-tracker-.+",i)]:
            print("@ DD @ ", f"rm -rf  {QFF}{ i }" )
            os.system(f"rm -rf {QFF}{ i }") ## DEL
        # ### 強制中斷
        # import os
        # from tempfile import NamedTemporaryFile as F
        # fp = F(suffix=".py",prefix="",delete = False ) ## 檔案不刪除
        # ################################################
#         test='''
# ###### win...比os.exit()  有效果!!
# ###### 注意的是程序要停止...才能關閉..刪除
# import subprocess,os
# ###### subprocess.Popen(f"cmd.exe /k taskkill /F /T /PID {'''+str(os.getppid())+'''}", shell=True)
# os.kill('''+str(os.getppid())+''',9)
# '''    
#         fp.write( test.encode(encoding="utf-8") )
#         fp.close()  
#         ###############################################
#         import os
#         # os.system(f"python {fp.name}") ## 必須關閉檔案 才能執行
#         # os.remove(fp.name)
#         # os.kill(str(os.getppid()) ,9)
#         os.exit()
#         ###############################################


print("@ egg_info 階段 @",f"pip install {Var.nameA}=={Var.nameB} --compile --no-cache-dir")
if 'bdist_wheel' in sys.argv:

    import os,tempfile as T
    dir_name = T.mkdtemp(suffix="..\\",prefix="",dir=  os.environ[ "TEMP" ] ) 
    name = dir_name[len(os.environ[ "TEMP" ])+1::]                       

    # Author-email:
    import os
    os.environ[ "Email" ] = str(name[0:-3]+"@gmail.com")


if   sdist.VVV and (not "BLFF" in dir()):
  # if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install':


  ### win10 [ build ]  
  ### linux [ sdist ] 
  if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean'  or sys.argv[1]== 'build' :


    
    ##############################################
    from setuptools.command.install import install
    
    #####
    from subprocess import check_call
    
    
    nameA= f"{Var.nameA}" 
    nameB= f"{Var.nameB}"
    package= f"{sdist.dir}"
     

    #### pip-install
    from pip._internal.cli.main import *
    class PostCMD(install):
      """cmdclass={'install': XXCMD,'install': EEECMD }"""


      def  run(self):
        ###################################
        import os
        install.run(self)
        print(nameA,nameB)
         ################################################
        ################################################
        import os
        if not "sys.argv" in os.environ.keys():
            
            ################################################
            ################################################
            ################################################
            print("# 小貓 1 號")

            
            def DPIP(BL):
            #   ###########################################
            #   import os
            #   def showPIP():
            #         import os,re
            #         pip=os.popen("pip show pip")
            #         return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip().replace(os.path.sep,"/") 
            #     ##################################################################################################
            #   def mv(DIR,pathA,pathB):
            #     ####################################
            #     import os,subprocess as cmds
            #     home = os.getcwd()
            #     ####################################
            #     os.chdir(DIR)
            #     if   os.name=="posix":
            #         cmds.Popen('mv "'+pathA+'" "'+pathB+'" ',shell=True,stdout=open(os.devnull,"w") )
            #     elif os.name=="nt":
            #         cmds.Popen('move "'+pathA+'" "'+pathB+'" ',shell=True,stdout=open(os.devnull,"w") )
            #     os.chdir(home)

              if BL:
                # #########
                # ## A ##
                # #########
                # DIR = str(__file__).split("setup.py")[0]  
                # # DIR = showPIP()
                # FFQ = f"{Var.nameA}-{Var.nameB}.dist-info"
                # FFQB = f"{Var.nameA}-{Var.nameB}.dist-info"
                # mv(f"{DIR}{os.path.sep}{ FFQ }",f"{DIR}{os.path.sep}{ FFQB }")
                #########
                ## B ##
                #########
                ##################################################################
                import os
                ##################################################################
                FF = str(__file__).split("setup.py")[0]
                # print("@ pipQQ ::",FF)
                
                import os
                # print(os.popen("dir "+FF).read())
                ### 刪除1
                if os.name=="nt":     ## Win10    
                    print("@ DPIP-FF ::",FF )  
                    os.system(f"rmdir /q /s {FF}") ## DEL
                # else:    
                #     print("@ DPIP-FF333 ::",FF )  
                #     os.system(f"rm -rf {FF}") ## DEL

                    # import shutil
                    # shutil.move(FF,FF+"QQ")
                    ###################################### 

                    # print("@ DPIP ::",os.popen("dir "+FF).read() ) 
                ##################################################################
                # C:\Users\moon\AppData\Local\Temp\pip-install-vslm992c\sh-py_51683c691ba945329606fb3092157455 的目錄
              else:
               
                ##################################################################
                import os
                ##################################################################
                FF = str(__file__).split("setup.py")[0]
                import os
                # print(os.popen("dir "+FF).read())
                ### 刪除1
                if os.name=="nt":     ## Win10    
                    print("@ DPIP-FF ::",FF )  
                    os.system(f"rmdir /q /s  {FF+os.path.sep}UNKNOWN-0.0.0-py3.7.egg-info") ## DEL
                # else:     ## Win10    
                #     print("@ DPIP-FF333 ::",FF )  
                #     os.system(f"rm -rf  {FF+os.path.sep}UNKNOWN-0.0.0-py3.7.egg-info") ## DEL
             
             



            ##########################################################
            ## 只有 win10 會
            DPIP(True)
            # #########################################################
            # ### 只能是字串 陣列會錯誤
            # import sys , os
            # # os.environ[ "sys" ] = str(sys.argv)       
            # os.system("pip install git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/"+nameA+"/@v"+nameB+"#egg="+nameA+"")
            # ################???... 如果用...執行續???

            
            import os
            #### from pip install 
            #### 建立一個 .py檔案
            from tempfile import NamedTemporaryFile as F
            fp = F(suffix=".py",prefix="",delete = False ) ## 檔案不刪除
            ################################################
            
#             ####################################################################
#             textOP='''
# ##[startOP]
# import builtins as B
# def dirOP():
#    return os.environ["LOCALAPPDATA"]+ r"\pip\cache\http\b\b" if os.name=="nt" else ( os.environ["HOME"]+"/.cache/pip/http/b/b" if os.name=="posix" else "None" )
              
# B.__dict__["dirOP"]= dirOP
# ##[startOP]
# '''
#             ######## 這是寫入 site.py import 模組時....自刪除重新安裝 程序
#             import sys,pip
#             readOP = open(pip.__file__,"r").read() ## 讀取
#             open(pip.__file__,"a+").write(textOP)   ## 寫入
#             del sys.modules["pip"]
#             ####################################################################



            #### 後面的OP.py應用
            

            # ###########################################  SH.py-12.97.dist-info
            # ###########################################  SH.py-12.97.dist-info
            # ############################################ 
            # nameA= f"{Var.nameA}" 
            # nameB= f"{Var.nameB}"
            # # # package= f"{sdist.dir}"
            import os
            # os.system(f'start cmd /c "timeout /nobreak /t 13&& echo {str(nameB)} && pause"')
            ############################################ 
            cmd_scripts=[                                                        
            'cmdsSQL=SQL.databasesB:main',  
            'databases=md.databases:main',                      
            ]
            ###########################################
            import os
            def showPIP():
                import os,re
                pip=os.popen("pip show pip")
                return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip().replace(os.path.sep,"/") 
            ##################################################################################################
            # nameQ = showPIP() + os.path.sep + nameA+ r"-" +nameB+ r".dist-info"  
            ############################################
            dirQX = [i.split("=")[1].split(".")[0]   for i in cmd_scripts] 
            ####################################################################################################
            #################################################################################################
          
       
      
            textSQ='''
##['''+nameA+''']

# https://iter01.com/585035.html

import sys
from types import ModuleType
from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder, Loader
 

from pip._internal.cli.main import *
class Module(ModuleType):
   def __init__(self, name):
      ################################################
      #print("!B!",name)
      self.x = 1
      self.name = name
      #### pip-install

from pip._internal.cli.main import * 
from pip._internal.commands.install import *
from pip._internal.metadata.pkg_resources import *


    
def mv(DIR,pathA,pathB):
    ####################################
    import os,subprocess as cmds
    home = os.getcwd()
    ####################################
    os.chdir(DIR)
    if   os.name=="posix":
        cmds.Popen('mv "'+pathA+'" "'+pathB+'" ',shell=True,stdout=open(os.devnull,"w") )
    elif os.name=="nt":
        cmds.Popen('move "'+pathA+'" "'+pathB+'" ',shell=True,stdout=open(os.devnull,"w") )
    os.chdir(home)


class ExampleLoader(Loader):
   ### 宣告-設值
   def create_module(self, spec):
      ###########################################  
      import os ,re,sys 
      if os.name=="posix":     ## Linux
        DIR = r"'''+showPIP()+'''"
        for i in [i for i in os.listdir( DIR )if re.findall("'''+nameA+'-'+nameB+'''",i)]:
            mv(f"{DIR}{os.path.sep}{i}",f"{DIR}{os.path.sep}{i}_del")

      elif os.name=="nt":     ## Win10
         DIR = r"'''+showPIP()+'''"
         for i in [i for i in os.listdir( DIR )if re.findall("'''+nameA+'-'+nameB+'''",i)]:
            mv( DIR,f"{DIR}{os.path.sep}{i}",f"{DIR}{os.path.sep}{i}_del")
      ###########################################
      os.environ["sys.argv"]= str(spec.name)  
      ##################################################
      return Module(spec.name) ## self.name 
      ##################################################


   ### 運作
   def exec_module(self, module):
      import os , sys
      print("!C!",  module , module.name , os.getpid() , os.getppid())
      import sys,os

      ## [ str ][0] 取出
      '''+f"cmd_scripts={cmd_scripts}"+'''
      cmdsONE = [i for i in cmd_scripts if i.startswith( sys.argv[0].split(os.path.sep).pop().split(".")[0] )  ][0] 

      import os
      os.environ['sys.argv']= str(sys.argv)  
      os.environ['sys.cmds']= str(cmdsONE)


      import subprocess,os
      ### 注意屬性[pip -v]
      sproc = subprocess.Popen("pip install '''+nameA+'=='+nameB+''' --compile --no-cache-dir",shell=True,stdout=open(os.devnull,"w") )
      sproc.wait() ##

      import re,os
      DIR = r"'''+showPIP()+'''"
      for i in [i for i in os.listdir( DIR )if re.findall("'''+nameA+'-'+nameB+'''",i)]:
        mv( DIR,i,i[0:-4] ) 



      import os
      ##########################################
      import os
      del os.environ["sys.argv"]
      ##########################################
      ################### pp.resume() ## 繼續跑

      ###### 直接關閉..
      import os
      os._exit(0)
      

# class ExampleFinder(MetaPathFinder):
class '''+nameA.replace(".","_")+'''(MetaPathFinder):
   def find_spec(self, moduleQ , path, target=None): 
      
      if moduleQ in '''+str(dirQX)+''':
        ################### 會顯示 模組名 'moduleQ'
        print("@Finde:", moduleQ , path )
        return ModuleSpec( moduleQ , ExampleLoader())
     


import os,sys
if not "sys.argv" in os.environ.keys():
     sys.meta_path.append('''+nameA.replace(".","_")+'''())

###########################################
### pip uninstall SH.py -y
##########################################
import sys
if "'''+nameA+'''" in [i if len(i.split("=="))==1 else i.split("==")[0] for i in sys.argv]:
    
    if "uninstall" in sys.argv:
        ### 清除 os.path  ##[tag標籤]
        ##########################
        import re
        R=re.findall("##\['''+nameA+'''\].*##\['''+nameA+'''\]",open(__file__,"r").read(),re.S)
        S="".join(open(__file__,"r").read().split(R[0]))
        ## del
        open(__file__,"w").write(S)
        ########################### 
  

##[''' +nameA+''']
'''
   
            
   
            
            ###############################################
            ################################################
            import os,sys
            ## 設定::PYTHONPATH 變數 .........pip install 預設路徑在 HOME??? 所以建檔位置在這
            ## 讓 import OP 可以讀取到
            os.environ["PYTHONPATH"] = os.environ["LOCALAPPDATA"] if os.name=="nt" else os.environ["HOME"]
            
       

            # fpB = F(suffix=".py",prefix="",delete = False ,dir= os.environ["PYTHONPATH"] ) ## 檔案不刪除
            
            ###############################################
            ################################################
            ###############################################
            ################################################
            test='''

import sys , os
###### os.system("python -m pip install psutil")
###### os.system(f"notepad {__file__}")


##os.system("pip install git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v'''+nameB+'''#egg='''+nameA+'''")


#### pause-main
#### import psutil , os
####pp = psutil.Process( '''+str(os.getpid())+''' )   
####pp.suspend() ## 子程序 暫停 ......... 站亭子程序 但是 子孫不聽話


################################# 關閉 print !!
import sys,os
SS=sys.stdout
sys.stdout=open(os.devnull,"w")





# def wowID():
#     import os
#     home = os.getcwd()
#     homeSS= (os.environ["LOCALAPPDATA"]+".pip.cache.http.b.b".replace(".","\\\\")  ) if os.name=="nt" else ( os.environ["HOME"]+"/.cache/pip/http/b/b") 
#     os.chdir(homeSS)        
#     wow = os.popen("git config root.dir").read().rstrip()
#     os.chdir(home)     
#     return wow   
def wowID():
    import os
    wow= (os.environ["LOCALAPPDATA"]+".pip.cache.http.b.b".replace(".","\\\\")  ) if os.name=="nt" else ( os.environ["HOME"]+"/.cache/pip/http/b/b") 
    return wow   
import os
os.environ["sys.wow"] =  wowID()


############################################### 加密預設
import os;
if not "TEMP" in os.environ.keys():
    os.environ[ "TEMP" ] = "/tmp" 
############################################### 加密預設

################ 註冊信箱 ########################
def strQ(N=10):
    import random, string
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
    # Generate [0-9, a-z, A-Z] ten words
##############################################################################################
import os
os.environ[ "Email" ] = strQ(8) +"@gmail.com"
####################################################




# # print("!#################!" ,str("git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v'''+nameB+'''#egg='''+nameA+'''") )

#### pip-install ####1 ...成功版
from pip._internal.cli.main import *
main(["install","git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v'''+nameB+'''#egg='''+nameA+'''" ])
# main(["install","git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v17.35#egg='''+nameA+'''" ])


# main(["install","git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v12.91#egg='''+nameA+'''" ])
# import os
# os.system("pip install git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v12.11#egg='''+nameA+'''")
# #### pip-install ####2 ...還是測試失敗了
# import subprocess,os
# sproc = subprocess.Popen("pip install git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v18.47#egg='''+nameA+'''",shell=True,stdout=open(os.devnull,"w"),stdin=open(os.environ["PYTHONPATH"]+os.path.sep+"OP.py","r") )
# sproc.wait() ## 




########## 移除:cryptocode 模組 #################
import os
os.system("pip uninstall cryptocode -y> log.py")
os.remove("log.py")
#####################################################


################################# 打開 print !!
sys.stdout=SS
###################################################


### start-main
################### pp.resume() ## 繼續跑

###### win...比os.exit()  有效果!!
###### 注意的是程序要停止...才能關閉..刪除
import subprocess,os
###### subprocess.Popen(f"cmd.exe /k taskkill /F /T /PID {'''+str(os.getppid())+'''}", shell=True)
os.kill('''+str(os.getppid())+''',9)
'''
            
            fp.write( test.encode(encoding="utf-8") )
            fp.close()  ## close 關閉檔案::則才會刪除檔案!!   os.remove(fp.name) 才有效果
            ###############################################


            # ################################################
            # ################################################
            # fpB.write( testB.encode(encoding="utf-8") );fpName=fpB.name
            # fpB.name=os.environ["PYTHONPATH"] +os.path.sep+ "OP.py"
            # import os;os.rename(fpName,fpB.name);
            # fpB.close()  ## close 關閉檔案::則才會刪除檔案!!   os.remove(fp.name) 才有效果
            # os.remove(fpB.name) 
            # ###############################################
            # ###############################################

            import os
            os.system(f"python {fp.name}") ## 必須關閉檔案 才能執行
            # print( os.popen(f"python {fp.name}").read()) ## 必須關閉檔案 才能執行
            os.remove(fp.name)

            
            import os
            OPS = os.environ["PYTHONPATH"] +os.path.sep+ "OP.py"
            os.remove( OPS )            
            ######################
            # https://blog.csdn.net/happyjacob/article/details/112385665
            DPIP(False)
            #############################################
            ###########################################
            #############################################

      


    ##############
    import site,os
    siteD =  os.path.dirname(site.__file__)
    # +os.sep+"siteR.py"
    print("@siteD: ",siteD)
    #### setup.py ################################
    from setuptools import setup, find_packages
    
    setup(
          # name  =  "cmd.py"  ,
          name  =   f"{Var.nameA}"  ,
          version=  f"{Var.nameB}"  ,

          author="我是一隻小貓",
          description="[setup.py專案]",
          author_email =   str(os.environ[ "Email" ])  if "Email" in os.environ.keys() else "999@gmial.com" ,
          
          
          #long_description=long_description,
          long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
          long_description_content_type="text/markdown",
        #   author="moon-start",
        #   author_email="login0516mp4@gmail.com",
          # url="https://gitlab.com/moon-start/cmd.py",
          license="LGPL",
          
        #   packages=find_packages(include= ["cmdsSQL","cmdsSQL.*"] ), 
          packages = find_packages(), 
          ################################
          data_files=[
            (r'Scripts', ['QQ/K.dd']),
            # (r'Scripts', ['bin/pypi-t.exe'])
            # (r'/', ['bin/git.exe'])
          ],
          cmdclass={
                'install': PostCMD
                # 'develop':  PostCMD
          },
          #########################
          ## https://setuptools.pypa.io/en/latest/userguide/datafiles.html
          include_package_data=True, # 將數據文件也打包
          zip_safe=True
    )
   

### B



