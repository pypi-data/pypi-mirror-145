import ipywidgets as widgets
try:
    from ipyfilechooser import FileChooser
except ModuleNotFoundError as er:
    raise ModuleNotFoundError(str(er.args) + "\n Install with e.g. $ pip install ipyfilechooser")
import markdown
import sys
import os
from io import StringIO
import functools
import difflib


import mariqt.variables as miqtv

class MyLabel(widgets.HTML):
    """ Label that allows disabling as well as markdown notation. Use 'myvalue' instead of value """

    def __init__(self,value=""):
        widgets.HTML.__init__(self)
        self._myvalue = value
        self.disabled = False
        self.paint()
        
    def paint(self):
        txt = markdown.markdown(self.myvalue)
        if not self.disabled:
            self.value = f"<p><font color='black'>{txt}</p>"
        else:
            self.value = f"<p><font color='grey'>{txt}</p>"

    @property
    def disabled(self):
        return self._disabled 

    @disabled.setter
    def disabled(self, value):
        self._disabled = value
        self.paint()
            
    @property
    def myvalue(self):
        return self._myvalue 

    @myvalue.setter
    def myvalue(self, value):
        self._myvalue = value
        self.paint()


class Capturing(list):
    """ caputres output in variable. Use:  with Capturing() as output: """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


################################ Editable list widget ############################################################

class EditalbleListWidget():
    """ creates a widget containing a list of sub widgets which can be added and removed and are stored in a list """
    def __init__(self,label,itemWidgetExample,iFDOList):
        """ label will be displayed above list and in front of "add" button. itemWidgetExample is used to create item by copying it, must be inherited from itemWidgetBase """
        
        self.itemWidgetExample = itemWidgetExample
        
        self.iFDOList = iFDOList # list of respective fields/objs in iFDO 
        self.itemObjList = []    # list of item object
        self.itemsWidget = widgets.VBox([e.widget for e in self.itemObjList]) # list of item objects as widget
        
        # label plus add button
        addButton = widgets.Button(description="+", layout=widgets.Layout(width='auto'))
        addButton.on_click(self.on_addButton_clicked)
        self.labelButtonBox = widgets.HBox([widgets.Label(label), addButton])
        
        # complete widget
        self.completeWidget = widgets.VBox([self.labelButtonBox,self.itemsWidget])
        self.repaint()
    
    def on_addButton_clicked(self,b, params=[]): #fileName="",cols=[]):
        #with Capturing() as output:
        
        #new = FileParserWidget(fileName,cols)

        new = self.itemWidgetExample.copy()
        new.setParams(params)
        newContainer = ItemWidgetContainer(self,new)
        if not newContainer in self.itemObjList:
            self.itemObjList.append(newContainer)
            self.itemsWidget.children += (newContainer.widget,) #[e.widget for e in auxFilesObjs]
            self.itemWidgetExample.on_change_fct(0)
        #debugOutputWidget.addText(str(output))

    def handleOn_deleteButton_clicked(self,obj):
        #with Capturing() as output:
        
        self.itemObjList.remove(obj)
        self.itemsWidget.children = [e.widget for e in self.itemObjList]
        #iFDO.removeItemInfoTabFile(obj.fileName(),obj.columns())
        self.itemWidgetExample.removeFromiFDO(obj.itemWidget.getParams())
        obj.widget.close()
        self.itemWidgetExample.on_change_fct(0)
        self.repaint()
        #debugOutputWidget.addText(str(output))

    def repaint(self):
        for item in self.iFDOList:
            tmpNew = self.itemWidgetExample.copy()
            tmpNew.setParams(self.itemWidgetExample.readParamsFromiFDOElement(item))
            tmpNewContainer = ItemWidgetContainer(self,tmpNew)
            if not tmpNewContainer in self.itemObjList:
                self.on_addButton_clicked(0,tmpNew.getParams())


class ItemWidgetContainer:
    """ contains the item itself plus the delete button """
    def __init__(self,editalbleListWidget,itemWidget):
        self.editalbleListWidget = editalbleListWidget
        self.itemWidget = itemWidget
        deleteButton = widgets.Button(description="Delete")
        deleteButton.on_click(functools.partial(self.on_deleteButton_clicked,obj=self))
        self.widget = widgets.VBox([self.itemWidget.getWidget(),deleteButton,widgets.Label("")])
        
    def on_deleteButton_clicked(self,b,obj):
        #with Capturing() as output:
        self.editalbleListWidget.handleOn_deleteButton_clicked(obj)
        #debugOutputWidget.addText(str(output))
            
    def __eq__(self, other):
        if self.itemWidget.getParams() == other.itemWidget.getParams():
            return True
        else:
            return False
            
class ItemWidgetBase:
    """ base class for the list widget that can be used """
    
    def __init__(self,on_change_fct):
        try:
            self.on_change_fct = on_change_fct
            self.on_change_fct(0)
        except Exception:
            def on_change_fct(self,change):
                pass
    
    def __eq__(self, other):
        if self.getParams() == other.getParams():
            return True
        else:
            return False
    
    def copy(self):
        raise NotImplementedError("Please Implement this method")
    
    def setParams(self,params):
        raise NotImplementedError("Please Implement this method")
        
    def getParams(self):
        raise NotImplementedError("Please Implement this method")
        
    def getWidget(self):
        raise NotImplementedError("Please Implement this method")
        
    def removeFromiFDO(self,params):
        """ what should be done in iFDO if item with params deleted? """
        raise NotImplementedError("Please Implement this method")
        
    def readParamsFromiFDOElement(self,element):
        """ how can params be read from the one element of EditalbleListWidget.iFDOList in order to init widget """
        raise NotImplementedError("Please Implement this method")
        
# example
"""
iFDOList = ["value1","value2"]        
class TestWidget(ItemWidgetBase):
    
    def __init__(self,on_change_fct):
        ItemWidgetBase.__init__(self,on_change_fct)
        self.valueWidget = widgets.Text(value="Empty")
        self.widget = widgets.HBox([widgets.Label("Value:"),self.valueWidget])
    
    def copy(self):
        ret = TestWidget(self.on_change_fct)
        ret.setParams(self.getParams())
        return ret
    
    def setParams(self,params=[""]):
        if len(params) == 0:
            params=[""]
        self.valueWidget.value = params[0]
        
    def getParams(self):
        return [self.valueWidget.value]
        
    def getWidget(self):
        return self.widget
    
    def removeFromiFDO(self,params):
        #print("TODO remove from ifdo:",params)
        if params[0] in iFDOList:
            iFDOList.remove(params[0])
        
    def readParamsFromiFDOElement(self,element):
        #print("TODO read params from iFDO element")
        return [element]
    

itemWidgetExample =  TestWidget()
testList = EditalbleListWidget("Name",itemWidgetExample,iFDOList)
#display(testList.completeWidget,output)
"""

#################################################################################################################


class FileParserWidget(ItemWidgetBase):

    def __init__(self,defaultFields:dict,on_change_fct,iFDO=None):
        ItemWidgetBase.__init__(self,on_change_fct)
        
        self.defaultFields = defaultFields
        self.iFDO = iFDO
        startLocation = ""
        if iFDO is not None:
            startLocation = str(iFDO.dir.tosensor())
        self.auxFile_file_widget = FileChooser(startLocation)
        self.auxFile_file_widget.register_callback(on_change_fct)
        self.auxFile_file_widget.register_callback(self.on_file_selected)
        
        self.dateTimeKey = 'image-datetime'

        self.fileValid = MyValid()
        self.on_file_selected(0)

        self.fileSeparator = widgets.Dropdown(options=[('Tab', "\t"), ('Space', " "), (",",","),(";",";")],value="\t",layout=widgets.Layout(width='100px'))
        self.fileSeparator.observe(self.on_change_fct)
        self.fileSeparator.observe(self.on_file_selected)

        addButton = widgets.Button(description="+", layout=widgets.Layout(width='30px'))
        removeButton = widgets.Button(description="-", layout=widgets.Layout(width=addButton.layout.width))

        addButton.on_click(self.on_addButton_clicked)
        removeButton.on_click(self.on_removeButton_clicked)

        self.dateTimeLabel = widgets.Label("DateTime Format:")
        self.dateTimeLabelCotainer = widgets.VBox([])
        self.dateTimeWidget = widgets.Text(value=miqtv.date_formats["mariqt"],placeholder = "e.g: %d.%m.%Y %H:%M:%S.%f",layout=widgets.Layout(width='188px'))
        self.dateTimeWidgetContainer = widgets.VBox([])

        self.columnsValid = MyValid()

        auxFile_columsLabel_widget = widgets.HBox([ widgets.VBox([widgets.Label("Column Names:"),widgets.Label("Field Names:")]),
                                                    widgets.VBox([widgets.HBox([widgets.Label(""),widgets.VBox([self.columnsValid])],layout=widgets.Layout(justify_content='space-between')),widgets.HBox([addButton,removeButton])])],
                                                    layout=widgets.Layout(justify_content='space-between')
                                                    )
        self.columnOptions = []
        self.fieldNameOptions = [key for key, value in self.defaultFields.items() if '-set-' not in key] + [self.dateTimeKey]

        columnName = widgets.Dropdown(options=self.columnOptions,layout=widgets.Layout(width='98%'))


        self.auxFile_ColumnsBox_widget = widgets.HBox([]) # needed before definition
        self.fileNameHeaderFieldWidget = HeaderFieldWidget(self.columnOptions,self.fieldNameOptions,[self.on_change_fct,self.on_headerFieldWidget_changed])
        self.fileNameHeaderFieldWidget.comboBox_field.value = "image-filename"
        self.fileNameHeaderFieldWidget.comboBox_field.disabled = True
        
        self.auxFile_ColumnsBox_widget =  widgets.HBox([self.fileNameHeaderFieldWidget],
                                                            layout=widgets.Layout(
                                                            display='flex',
                                                            flex_flow='row',
                                                            width='100%',
                                                            overflow_x='auto',
                                                            flex='1'
                                                            )
                                                            )

        borderColor='#C0C0C0'
        self.auxFile_widget = widgets.GridBox([ widgets.HBox([widgets.Label("File:"),widgets.VBox([self.fileValid])],layout=widgets.Layout(justify_content='space-between')),self.auxFile_file_widget,
                                                widgets.Label("Separator:"),self.fileSeparator,
                                                self.dateTimeLabelCotainer,self.dateTimeWidgetContainer,
                                                auxFile_columsLabel_widget,self.auxFile_ColumnsBox_widget],layout=widgets.Layout(
                                                    border='solid 1px '+borderColor,
                                                    padding='8px 8px 8px 8px',
                                                    margin='2px 0px 2px 2px',
                                                    width='98%',
                                                    grid_template_columns='20% 79%'))

        
        
        self.on_addButton_clicked(0) # have one empty column widget by default

    def on_addButton_clicked(self,b,fieldName="",columnName=""):

        newHeaderFieldWidget = HeaderFieldWidget(self.columnOptions,self.fieldNameOptions,[self.on_change_fct,self.on_headerFieldWidget_changed])
        if fieldName != "":
            newHeaderFieldWidget.setFieldName(fieldName)
        if columnName != "":
            newHeaderFieldWidget.setColumnName(columnName)

        if (fieldName == "" and columnName == "") or newHeaderFieldWidget not in [e for e in self.auxFile_ColumnsBox_widget.children if isinstance(e,HeaderFieldWidget)]:
            self.auxFile_ColumnsBox_widget.children += (newHeaderFieldWidget,)
            self.on_headerFieldWidget_changed(0)
        self.on_change_fct(0)

    def on_removeButton_clicked(self,b):
        if len(self.auxFile_ColumnsBox_widget.children) > 2:
            remove = self.auxFile_ColumnsBox_widget.children[-1]
            self.auxFile_ColumnsBox_widget.children = self.auxFile_ColumnsBox_widget.children[:-1]
            remove.close()
            self.on_headerFieldWidget_changed(0)
            self.on_change_fct(0)


    def copy(self):
        ret = FileParserWidget(self.defaultFields,self.on_change_fct,self.iFDO)
        ret.setParams(self.getParams())
        return ret

    def setParams(self,params=[""]):
        # [filename,separator,headerDict,dateTimeFormat] with headerDict = {<field-name>: <column-name>}
        #with Capturing() as output:

            if len(params) == 0:
                params = ["",[""]]
            try:
                path = str(os.path.dirname(params[0]))
                filename = str(os.path.basename(params[0]))
            except Exception:
                path = ""
                filename = ""
            if path != "" and filename != "":
                if os.path.exists(params[0]):
                    self.fileSeparator.value = params[1]
                    self.dateTimeWidget.value = params[3]
                    self.auxFile_file_widget._set_form_values(path, filename)
                    self.auxFile_file_widget._apply_selection()
                    self.on_file_selected(0)
                else:
                    raise Exception("FileParserWidget: file '" + params[0] + "' not found")
                
                self.auxFile_ColumnsBox_widget.children = [self.auxFile_ColumnsBox_widget.children[0]]
                for field in params[2]:
                    self.on_addButton_clicked(0,field,params[2][field])
        #debugOutputWidget.addText(str(output))

    def getParams(self):
        # [filename,separator,headerDict,dateTimeFormat] with headerDict = {<field-name>: <column-name>}
        header = {}
        for item in [widget for widget in self.auxFile_ColumnsBox_widget.children if isinstance(widget,HeaderFieldWidget)]:
            header[item.getFieldName()] = item.getColumnName()
        return [self.auxFile_file_widget.selected,self.fileSeparator.value,header,self.dateTimeWidget.value]

    def getWidget(self):
        return self.auxFile_widget

    def removeFromiFDO(self,params):
        if self.iFDO is None:
            print("Caution! removeFromiFDO: iFDO is None")
            return
        self.iFDO.removeItemInfoTabFile(params[0],params[1],params[2])

    def readParamsFromiFDOElement(self,element):
        return [element.fileName,element.separator,element.header]

    def on_headerFieldWidget_changed(self,b):
        columnValues = [widget.getColumnName() for widget in self.auxFile_ColumnsBox_widget.children if isinstance(widget,HeaderFieldWidget)]
        fieldValues = [widget.getFieldName() for widget in self.auxFile_ColumnsBox_widget.children if isinstance(widget,HeaderFieldWidget)]
        if "" in columnValues or "" in fieldValues:
            self.columnsValid.valid = False
        elif len(set(columnValues)) != len(columnValues) or len(set(fieldValues)) != len(fieldValues):
            self.columnsValid.warningOnce()
            self.columnsValid.valid = False
        else:
            self.columnsValid.valid = True

        if self.dateTimeKey in fieldValues:
            self.dateTimeLabelCotainer.children = [self.dateTimeLabel]
            self.dateTimeWidgetContainer.children = [self.dateTimeWidget]
        else:
            self.dateTimeLabelCotainer.children = []
            self.dateTimeWidgetContainer.children = []


    def on_file_selected(self,b):
        if self.auxFile_file_widget.selected == None:
            self.fileValid.valid = False
            return
        try:
            with open(self.auxFile_file_widget.selected,'r') as f:
                self.fileValid.valid = True
                separator = self.fileSeparator.value
                first_line = f.readline().strip()
                fileHeaders = first_line.split(separator)
                self.columnOptions = fileHeaders
                for child in self.auxFile_ColumnsBox_widget.children:
                    if isinstance(child, HeaderFieldWidget):
                        child.setColumnOptions(fileHeaders)
        except FileNotFoundError:
            self.fileValid.valid = False
        
        try:
            self.fileNameHeaderFieldWidget.dropdown_columnName.value = difflib.get_close_matches(self.fileNameHeaderFieldWidget.comboBox_field.value,self.fileNameHeaderFieldWidget.dropdown_columnName.options)[0]
        except IndexError:
            pass
                    

class HeaderFieldWidget(widgets.VBox):
            """ VBox widget containing a widget for the header field name and the respective column name in a file to parse from """
            def __init__(self,columnOptions:list,fieldOptions:list,on_change_fct):

                self.comboBox_field = widgets.Combobox(options=fieldOptions, placeholder="Field Name",layout=widgets.Layout(width='98%'))
                self.dropdown_columnName = widgets.Dropdown(options=columnOptions,layout=widgets.Layout(width='98%'))
                if not isinstance(on_change_fct,list):
                    on_change_fct = [on_change_fct]
                for fkt in on_change_fct:
                    self.comboBox_field.observe(fkt,names='value')
                    self.dropdown_columnName.observe(fkt,names='value')
                    
                widgets.VBox.__init__(self,[self.dropdown_columnName,self.comboBox_field],layout=widgets.Layout(width='auto',overflow_x='hidden',))

            def __eq__(self,other):
                if other.comboBox_field.options == self.comboBox_field.options and \
                    other.comboBox_field.value == self.comboBox_field.value and \
                    other.dropdown_columnName.options == self.dropdown_columnName.options and \
                    other.dropdown_columnName.value == self.dropdown_columnName.value:
                    return True
                return False

            def getColumnName(self):
                return self.dropdown_columnName.value

            def getFieldName(self):
                return self.comboBox_field.value

            def setFieldName(self,name:str):
                self.comboBox_field.value = name

            def setColumnName(self,name:str):
                try:
                    self.dropdown_columnName.value = name
                except Exception:
                    raise Exception("Invalid selection.",name,"not in",self.dropdown_columnName.options)

            def setColumnOptions(self,options:list):
                self.dropdown_columnName.options = options


class MyValid(widgets.Image):
    """ Valid that has no aligment bug and allows disabling """
    def __init__(self,valid=True,disabled = False):
        widgets.Image.__init__(self)
        self.icon_check = miqtv.icon_check
        self.icon_checkDisabled = miqtv.icon_checkDisabled
        self.icon_error = miqtv.icon_error
        self.icon_errorDisabled = miqtv.icon_errorDisabled
        self.icon_warning = miqtv.icon_warning
        self._valid = valid
        self._disabled = disabled
        self.warning = False
        self.layout.width = '15px'
        self.layout.hight = '15px'
        self.layout.max_width = '15px'
        self.layout.max_hight = '15px'
        
        # make it vertically aligned with labels and texts
        space = 9
        self.add_class("top-spacing-class-" + str(space))
        # TODO
        #if space not in existingSpacingClasses_top:
        #    display(HTML("<style>.top-spacing-class-" + str(space) + " {margin-top: " + str(space) + "px;}</style>"))
        #    existingSpacingClasses_top.append(space)
        
        self.paint()
        
    def warningOnce(self):
        """ sets next invalid to warning """
        self.warning = True

    def paint(self):
        if self.valid:
            if self.disabled:
                self.value = self.icon_checkDisabled
            else:
                self.value = self.icon_check
        else:
            if self.disabled:
                self.value = self.icon_errorDisabled
            else:
                if self.warning:
                    self.value = self.icon_warning
                    self.warning = False
                else:
                    self.value = self.icon_error

    @property
    def valid(self):
        return self._valid

    @valid.setter
    def valid(self, value):
        self._valid = value
        self.paint()
            
    @property
    def disabled(self):
        return self._disabled 

    @disabled.setter
    def disabled(self, value):
        self._disabled = value
        self.paint()