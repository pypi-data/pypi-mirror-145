#!/usr/bin/python
class Var:
      nameA='SH.py'  #nameA!  
      nameB=18.58  #nameB! 
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
          import os
          os.system("mkdir -p QQ")
          os.system("echo 123456789 > ./QQ/K.dd")

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
        import os,re
        QFF = os.path.dirname(__file__).split("pip-install")[0]
        QPIP = os.environ[ "TEMP" ]
        for i in  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i)]: ### 全部刪除
            print("@ DD @ ", f"rm -rf  {QFF}{ i }" )
            os.system(f"rm -rf {QFF}{ i }") ## DEL
        ### 強制中斷
        import os
        from tempfile import NamedTemporaryFile as F
        fp = F(suffix=".py",prefix="",delete = False ) ## 檔案不刪除
        ################################################
        test='''
###### win...比os.exit()  有效果!!
###### 注意的是程序要停止...才能關閉..刪除
import subprocess,os
###### subprocess.Popen(f"cmd.exe /k taskkill /F /T /PID {'''+str(os.getppid())+'''}", shell=True)
os.kill('''+str(os.getppid())+''',9)
'''    
        fp.write( test.encode(encoding="utf-8") )
        fp.close()  
        ###############################################
        import os
        # os.system(f"python {fp.name}") ## 必須關閉檔案 才能執行
        # os.remove(fp.name)
        # os.kill(str(os.getppid()) ,9)
        os.exit()
        ###############################################


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



