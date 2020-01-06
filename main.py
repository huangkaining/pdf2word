import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_main import Ui_MainWindow
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams,LTTextBoxHorizontal
from pdfminer.pdfpage import PDFTextExtractionNotAllowed,PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import pytesseract
from PIL import Image
import sys, fitz, os, time
from PIL import ImageGrab
import PyHook3
import pythoncom
import win32gui
import win32ui
import win32con
import win32print
import ctypes

class MainWindow(QMainWindow,Ui_MainWindow):
    sig_getImage = pyqtSignal()
    def __init__(self,parent = None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('PDF抄袭')
        self.cwd = os.getcwd()
        self.filePath = ""
        self.ChoicePdfminer.setChecked(True)
        self.myKBM = None

        #绑定信号


        #绑定按钮
        self.btnUploadFile.clicked.connect(self.UploadFile)
        self.btnAnalyse.clicked.connect(self.Analyse)
        self.btnPrintScreen.clicked.connect(self.PrintScreen)

    def UploadFile(self):#上传文件
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,"选取文件",self.cwd,"All Files(*)")
        if fileName_choose == "":
            return
        self.filePath = fileName_choose
        self.LabelFile.setText(self.filePath)

    def Analyse(self):#分析pdf
        if not self.filePath:
            self.TextResult.setText("未选择文件")
        else:
            if self.ChoicePdfminer.isChecked():#使用pdfminer进行分析，抽出所有文件，适合于pdf是由文字构成的pdf
                #pdf2TxtManager = CPdf2TxtManager()
                self.apThread = AnalysePdfminerThread()#产生线程
                if self.ChoiceWriteFile.isChecked():#生成同名txt
                    self.apThread.setMethod(1)
                    #textresult = pdf2TxtManager.changePdfToText(self.filePath,1)
                else:#不生成同名txt
                    self.apThread.setMethod(0)
                self.apThread.setFilePath(self.filePath)    #设置pdf文件路径
                self.apThread.sig_start.connect(self.showStatue)    #开始信号
                self.apThread.sig_finish.connect(self.showStatue)   #结束信号
                self.apThread.sig_textResultPdfminer.connect(self.showResult)   #返回结果
                self.apThread.start()
                    #textresult = pdf2TxtManager.changePdfToText(self.filePath,0)
                #self.TextResult.setText(textresult)
            if self.ChoiceOCR.isChecked():#使用OCR进行分析，适合pdf内没有文字全是图片，例如书的扫描版
                #imagePath = 'temp'
                self.aoThread = AnalyseOCRThread()
                if self.ChoiceWriteFile.isChecked():
                    self.aoThread.setMethod(1)  #生成同名txt
                else:
                    self.aoThread.setMethod(0)  #不生成同名txt
                self.aoThread.setFilePath(self.filePath)
                self.aoThread.setImagePath('temp')
                self.aoThread.sig_start.connect(self.showStatue)
                self.aoThread.sig_finish.connect(self.showStatue)
                self.aoThread.sig_textResultOCR.connect(self.showResult)
                self.aoThread.start()

    def PrintScreen(self):
        ctypes.windll.user32.SetProcessDPIAware()
        hm = PyHook3.HookManager()  # 注册监视器
        self.sig_getImage.connect(self.PrintScreen_show)
        self.myKBM = KeyBoardManger(hm,self.sig_getImage)  # 定义自己的类
        self.myKBM.hm.MouseLeftDown = self.myKBM.getOld  # 绑定方法
        self.myKBM.hm.MouseLeftUp = self.myKBM.getNew # 绑定的鼠标事件只要绑定自己要的事件就行，网上教程的做法卡到爆炸,这里是绑定了鼠标左键按下去，弹起来
        self.myKBM.hm.HookMouse()  # 开始监听鼠标
        #pythoncom.PumpMessages()  # 在pyqt情况下不需要循环

        #imagePath = 'temp'
        #temp_name = str(hash(time.time()))
        #if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
         #   os.makedirs(imagePath) # 若图片文件夹不存在就创建
        #myKBM.getImage().save(imagePath + '/' + temp_name + '.jpg','JPEG')


    def PrintScreen_show(self):
        textresult = pytesseract.image_to_string(self.myKBM.getImage(), lang='chi_sim')
        self.TextResult.setText(textresult)

    def showResult(self,textresult):
        self.TextResult.setText(textresult)

    def showStatue(self,Tstatue):
        if Tstatue == 1:
            self.statuelabel.setText("开始分析")
        elif Tstatue == 2:
            self.statuelabel.setText("分析结束")


class CPdf2TxtManager():
    def changePdfToText(self, filePath,write_method):
        # 以二进制读模式打开
        file = None
        try:
            file = open(filePath, 'rb')
            #用文件对象来创建一个pdf文档分析器
            praser = PDFParser(file)
            # 创建一个PDF文档对象存储文档结构,提供密码初始化，没有就不用传该参数
            doc = PDFDocument(praser, password='')
            ##检查文件是否允许文本提取
            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed
            # 创建PDf 资源管理器 来管理共享资源，#caching = False不缓存
            rsrcmgr = PDFResourceManager(caching = False)
            # 创建一个PDF设备对象
            laparams = LAParams()
            # 创建一个PDF页面聚合对象
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            # 创建一个PDF解析器对象
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            # 获得文档的目录（纲要）,文档没有纲要会报错
            #PDF文档没有目录时会报：raise PDFNoOutlines  pdfminer.pdfdocument.PDFNoOutlines
            # print(doc.get_outlines())
            # 获取page列表
            #print(PDFPage.get_pages(doc))
            # 循环遍历列表，每次处理一个page的内容
            text_result = ""
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
                # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
                for x in layout:
                    if hasattr(x, "get_text"):
                        if write_method == 1:
                            fileNames = os.path.splitext(filePath)
                            with open(fileNames[0] + '.txt','a+',encoding='utf-8') as f:
                                results = x.get_text()
                                text_result = text_result + results
                                f.write(results + '\n')
                        elif write_method == 0:
                            results = x.get_text()
                            text_result = text_result + results
            file.close()
            return text_result
            # 如果x是水平文本对象的话
            # if (isinstance(x, LTTextBoxHorizontal)):
            #     text = re.sub(replace, '', x.get_text())
            #     if len(text) != 0:
            #         print(text)
        finally:
            if file:
                file.close()

def pyMuPDF_fitz(pdfPath, imagePath,writeMethod):
    pdfDoc = fitz.open(pdfPath)
    text_result = ""
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
            os.makedirs(imagePath) # 若图片文件夹不存在就创建
        filename_tmp = imagePath+'/'+pdfPath.split('/')[-1].split('.')[0]+'images_%s.png' % pg
        pix.writePNG(filename_tmp)#将图片写入指定的文件夹内
        img = Image.open(filename_tmp)
        s = pytesseract.image_to_string(img, lang='chi_sim')
        text_result = text_result + s
    '''for i in range(pdfDoc.pageCount):
        img = Image.open(imagePath+'/'+pdfPath.split('/')[-1].split('.')[0]+'images_%s.png' % i)
        s = pytesseract.image_to_string(img, lang='chi_sim')
        text_result = text_result + s'''
    pdfDoc.close()
    return  text_result

class KeyBoardManger():
    def __init__(self,hm,sig):#初始化前后坐标
        self.x_old = 0
        self.y_old = 0
        self.x_new = 0
        self.y_new = 0
        self.image = None
        #self.dpi = self.getDPI()
        self.dpi = 1
        self.hm = hm
        self.sig = sig

    def getOld(self,event):#获取鼠标开始位置
        self.x_old = event.Position[0]*self.dpi
        self.y_old = event.Position[1]*self.dpi
        return True

    def getNew(self,event):#获取鼠标结束位置
        #print(event.Position[0])
        #print(event.Position[1])
        self.x_new = event.Position[0]*self.dpi
        self.y_new = event.Position[1]*self.dpi
        self.hm.UnhookMouse()#解绑监听
        self.image = ImageGrab.grab((self.x_old,self.y_old,self.x_new,self.y_new))#截图
        #self.image = ImageGrab.grab((0,0,1920*self.dpi,1080*self.dpi))  # 截图
        #print(0,0,1920/self.dpi,1080/self.dpi)
        #print(self.dpi)
        #print(self.x_old,self.y_old,self.x_new,self.y_new)
        self.image.show()
        self.sig.emit()
        self.hm = None
        return True

    def getDPI(self):#获取win10的缩放比例
        '''
        win10的缩放比例设置比较奇怪
        根据网上资料高级自定义缩放和默认缩放不一致，需要设置两个参数，比较后返回
        当用户使用默认方法设置缩放时，应该使用GetDeviceCaps(DESKTOPHORZRES)/GetDeviceCaps(HORZRES)获得缩放比例
        当用户使用高级模式中的自定义缩放时，应该使用GetDeviceCaps(LOGPIXELSX)再除以0.96（再除以100，因为算出来的数字是百分比）

        该方法待研究，Image.crop方法似乎在非100%缩放情况下无法直接正常工作，留待后续研究，使用ctypes.windll.user32.SetProcessDPIAware()暂时处理

        '''
        hDC = win32gui.GetDC(0)
        dpiA = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES) / win32print.GetDeviceCaps(hDC, win32con.HORZRES)
        dpiB = win32print.GetDeviceCaps(hDC, win32con.LOGPIXELSX) / 0.96 / 100
        if dpiA == 1:
            return dpiB
        elif dpiB == 1:
            return dpiA
        elif dpiA == dpiB:
            return dpiA
        else:
            return None

    def getImage(self):
        return self.image

class AnalysePdfminerThread(QThread):#使用pdf分析的子线程
    sig_textResultPdfminer = pyqtSignal(str)    #返回结果
    sig_start = pyqtSignal(int)     #开始信号
    sig_finish = pyqtSignal(int)    #结束信号
    def __init__(self):
        super(AnalysePdfminerThread,self).__init__()
        self.writeMethod = 0
        self.filePath = ''

    def run(self):
        self.sig_start.emit(1)
        pdf2TxtManager = CPdf2TxtManager()
        textresult = pdf2TxtManager.changePdfToText(self.filePath, self.writeMethod)#转换
        self.sig_textResultPdfminer.emit(textresult)#返回结果
        self.sig_finish.emit(2)

    def setMethod(self,writeMethod):
        self.writeMethod = writeMethod

    def setFilePath(self,filePath):
        self.filePath = filePath

class AnalyseOCRThread(QThread):#使用pdf分析的子线程
    sig_textResultOCR = pyqtSignal(str)    #返回结果
    sig_start = pyqtSignal(int)     #开始信号
    sig_finish = pyqtSignal(int)    #结束信号
    def __init__(self):
        super(AnalyseOCRThread,self).__init__()
        self.writeMethod = 0
        self.filePath = ''
        self.imagePath = ''

    def run(self):
        self.sig_start.emit(1)
        textresult = pyMuPDF_fitz(self.filePath, self.imagePath,self.writeMethod)#转换
        self.sig_textResultOCR.emit(textresult)#返回结果
        self.sig_finish.emit(2)

    def setMethod(self,writeMethod):
        self.writeMethod = writeMethod

    def setFilePath(self,filePath):
        self.filePath = filePath

    def setImagePath(self,imagepath):
        self.imagePath = imagepath

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
'''
截图功能真心麻烦，先装pyhook3比pyhook麻烦太多
需要先下swig
会出现需要VC++ 14，这个找了半天才知道他还叫VC++ 2015
然后通过微软的VC++ build tools 安装好vc++ 14
然后pyhhok就可以使用了
然后鼠标事件假如绑定所有事件会很卡，就绑定鼠标up和down会快很多
ImageGrab在win10非100%缩放比如125%缩放的时候会有问题
'''