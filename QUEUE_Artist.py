# create a background image on a wxPython panel
# and show a button on top of the image
 
import wx
import os
import json
import datetime
class review(wx.Panel):
    """class Panel1 creates a panel with an image on it, inherits wx.Panel"""
    def __init__(self, parent, id,main_path):
        # create the panel
        self.parent=parent
        self.review_path=''
        self.panel=wx.Panel.__init__(self, self.parent, id)
        try:
            self.main_path = main_path
            self.review_artist_list=os.path.join(self.main_path ,'QUEUE','database','QUEUE_Artists.json').replace("\\","/")
            self.review_sup=os.path.join(self.main_path ,'QUEUE','database','QUEUE_Sups.json').replace("\\","/")
            # pick an image file you have in the working folder
            # you can load .jpg  .png  .bmp  or .gif files

            image_file = os.path.join(main_path,'QUEUE','sourceImages','QUEUEBG.jpg').replace("\\","/") 
            #print image_file
            image_file2 =os.path.join(main_path,'QUEUE','sourceImages','QUEUEREFRESH.jpg').replace("\\","/")
            image_file3 =os.path.join(main_path,'QUEUE','sourceImages','QUEUEARROW.jpg').replace("\\","/")
            image_file4 =os.path.join(main_path,'QUEUE','sourceImages','QUEUESETPATH.jpg').replace("\\","/")

            image_file5 = os.path.join(main_path,'QUEUE','sourceImages','QUEUESUBMIT.jpg').replace("\\","/")
			
			
            image1 =wx.Image(image_file2,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            image2 =wx.Image(image_file3,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            image11 =wx.Image(image_file4,wx.BITMAP_TYPE_ANY).ConvertToBitmap()			
            image111 =wx.Image(image_file5,wx.BITMAP_TYPE_ANY).ConvertToBitmap()			

            bmp1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            # image's upper left corner anchors at panel coordinates (0, 0)
            self.bitmap1 = wx.StaticBitmap(self, -1, bmp1, (0, 0))
            # show some image details
            str1 = "%s  %dx%d" % (image_file, bmp1.GetWidth(), bmp1.GetHeight()) 
            #parent.SetTitle(str1)
        except IOError:
            print "Image file %s not found" % imageFile
            raise SystemExit
        self.but_refresh = wx.BitmapButton(self.bitmap1, id=-1, bitmap=image1, pos=(5,3),size=(232,25))
        self.but_refresh.Bind(wx.EVT_BUTTON,self.refresh_proc) 
        # button goes on the image --> self.bitmap1 is the parent
        zone_list=[]
        #self.artist_list = wx.ListBox(self.bitmap1, 50, ( 5,32), (232, 260), zone_list, wx.LB_SINGLE)
        self.artist_list = wx.ListCtrl(self.bitmap1,style=wx.LC_LIST,pos=( 5,32), size=(232, 260))
        self.artist_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.explorer_path)
		
        #self.artist_list.InsertColumn(, "Artist Name")
        #self.artist_list.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
		
        self.resize_window = wx.BitmapButton(self.bitmap1, id=-1, bitmap=image2, pos=(212,297),size=(20,20))
        self.resize_window.Bind(wx.EVT_BUTTON,self.resize_window_proc)
        self.devetext=wx.StaticText(self.bitmap1, id=-1, label="Developed By Vedanti Bhanuse", pos=(95,455))
        self.devetext.SetBackgroundColour((28,88,155))
        self.spin_no = wx.TextCtrl(self.bitmap1, -1, value=str("5"), pos=(5, 380), size=(35, 20))
		
        self.spin_no.Enable(False)
        #self.avipath=wx.TextCtrl(self.bitmap1,id=-1,pos=(5,320),size=(20,20))
        self.file_browser = wx.BitmapButton(self.bitmap1, id=-1, bitmap=image11, pos=(5,325),size=(232,25))
        self.file_browser.Bind(wx.EVT_BUTTON,self.browse_review_path)				
        #wx.StaticBox(self.bitmap1, -1, ' Info', (5, 320), size=(230, 330))
        review_sup_list=self.review_sup_list()
        review_sup_list.sort()

        self.sup_list=wx.ComboBox(self.bitmap1,-1,pos=(5,354),size=(232,20),choices=review_sup_list,style=wx.CB_DROPDOWN)
        self.sup_list.SetEditable(False)
        self.sup_list.SetStringSelection(str(review_sup_list[0]))
        self.username_txt=os.getenv('USERNAME')
        self.username=wx.TextCtrl(self.bitmap1,id=-1,pos=(48,380),size=(120,20))
        self.spin_no.Bind(wx.EVT_TEXT, self.onAction)
        self.username.SetValue(self.username_txt)
        self.cb_upload = wx.CheckBox(self.bitmap1, -1, 'UPLOAD', (176,384))
        self.cb_upload.SetBackgroundColour((29,91,152))
        self.btn_submit_to_dailies = wx.BitmapButton(self.bitmap1, id=-1, bitmap=image111, pos=(5,410),size=(232,25))
        self.cb_upload.Bind(wx.EVT_CHECKBOX,self.user_upload_for_dailis)
        self.sup_list.Bind(wx.EVT_TEXT,self.update_list)	
        self.btn_submit_to_dailies.Bind(wx.EVT_BUTTON,self.submit_to_dailies)				
        artist_data=self.get_artist_list_by_sup(str(review_sup_list[0]))
        i=0
        get_max_avail_no=0
        self.artist_list.ClearAll()
        try:
			get_max_avail_no=str(artist_data[len(artist_data)-1]).split(" :> ")[0]
			print get_max_avail_no
		
			for each_artist in  artist_data:
				print 'adding item ',each_artist
			
				self.artist_list.InsertStringItem(i,each_artist)
				i=i+1
				self.spin_no.ChangeValue(str(int(get_max_avail_no)+1))
				self.get_max_avail_no_fwd=0
				self.get_max_avail_no_fwd=int(get_max_avail_no)+1
        except:
			self.spin_no.ChangeValue(str(int(get_max_avail_no)+1))
			self.get_max_avail_no_fwd=0
			self.get_max_avail_no_fwd=int(get_max_avail_no)+1


    def onAction(self, event):
        print "Enter in onAction Proc--->",self.get_max_avail_no_fwd, "  ", type(self.get_max_avail_no_fwd)
        pre_val =self.get_max_avail_no_fwd
        raw_value = self.spin_no.GetValue()
        if all(x in '0123456789' for x in raw_value):
			self.value = raw_value
			#self.spin_no.ChangeValue(str(pre_val))
        else:
			Boxdlg = wx.MessageDialog(self, 'Required input is number only !! ', 'Error', wx.OK | wx.ICON_ERROR)
			Boxdlg.ShowModal()
			sup_name=self.sup_list.GetValue()
			all_occupied_no=self.get_artist_occupied_review_no(sup_name)
			no=int(all_occupied_no[len(all_occupied_no)-1])+1
			self.spin_no.ChangeValue(str(no))
			Boxdlg.Destroy()			
    def update_list(self, event):
        print "update color font"
        sup_name=self.sup_list.GetValue()
        self.artist_list.ClearAll()
        artist_data=self.get_artist_list_by_sup(sup_name)
        print len(artist_data)
        i=0
        get_max_avail_no=0
        if sup_name!="" and len(artist_data)>0:
			for each_artist in  artist_data:
				self.artist_list.InsertStringItem(i,each_artist)
				#self.artist_list.SetItemBackgroundColour(i,'RED')
				i=i+1
			get_max_avail_no=str(artist_data[len(artist_data)-1]).split(" :> ")[0]
        self.spin_no.ChangeValue(str(int(get_max_avail_no)+1))
			
    def browse_review_path(self, event):
        dlg=wx.DirDialog(None,message="Open_path",style=wx.DEFAULT_DIALOG_STYLE)
        res=dlg.ShowModal()
        if  res== wx.ID_OK:
			print dlg.GetPath()
			self.review_path=dlg.GetPath()
			if self.review_path=="" or os.path.exists( self.review_path)==False:
				Boxdlg = wx.MessageDialog(self, 'Failed to set review path ', 'Error', wx.OK | wx.ICON_ERROR)
				Boxdlg.ShowModal()
        elif res == wx.ID_CANCEL:
			Boxdlg = wx.MessageDialog(self, 'Review Path is not correctly!! ', 'Error', wx.OK | wx.ICON_ERROR)
			Boxdlg.ShowModal()
			dlg.Destroy()

        else:
			dlg.Destroy()

    def explorer_path(self, event):
        item=self.artist_list.GetFirstSelected()
        print item
	
        print self.artist_list.GetItemText(item)
        res=self.artist_list.GetItemText(item)
        artist_nono=res.split(" :> ")[0]
        artist_name=res.split(" :> ")[1]
        sup_name=self.sup_list.GetValue()

        artist_review_path=self.get_review_path(sup_name,artist_name,artist_nono)
        explorer_cmd="explorer"+ " "+artist_review_path
        if os.path.exists( artist_review_path):
			os.startfile(artist_review_path)#proc = subprocess.Popen(explorer_cmd, shell=True)		#print artist_review_path
        elif not os.path.exists( artist_review_path):
			msg=artist_review_path + " , Incorrect Path !!!"	
			Boxdlg = wx.MessageDialog(self, msg, 'Error', wx.OK | wx.ICON_ERROR)
			Boxdlg.ShowModal()
			dlg.Destroy()
    def get_review_path(self,sup_name,name,no):
		f=open(self.review_artist_list)
		json_data=json.loads(f.read())
		f.close()
		review_path=""
		json_dailies=json_data['dailies']
		if sup_name in json_dailies.keys():
			sup_data=json_data['dailies'][sup_name]
			for each_artist in sup_data:
				if each_artist["name"]==name and each_artist["no"]==str(no):
					#print each_artist["daily_folder"]
					review_path=each_artist["daily_folder"]
					break;
		return review_path	
    def resize_window_proc(self, event):
        sizewin=self.parent.GetSizeTuple()
        if int(sizewin[1])==350:
        	self.parent.SetSizeWH(250,500)
        else:
        	self.parent.SetSizeWH(250,350)
			
        sup_name=self.sup_list.GetValue()
        self.artist_list.ClearAll()
        artist_data=self.get_artist_list_by_sup(sup_name)
        i=0
        get_max_avail_no=0
        if sup_name!="" and len(artist_data)>0:
			for each_artist in  artist_data:
				self.artist_list.InsertStringItem(i,each_artist)
				i=i+1
			get_max_avail_no=str(artist_data[len(artist_data)-1]).split(" :> ")[0]
        self.spin_no.ChangeValue(str(int(get_max_avail_no)+1))
        self.review_path=""
        self.username.SetValue(self.username_txt)
        self.cb_upload.SetValue(False)
        
    def user_upload_for_dailis(self, event):
        if self.cb_upload.IsChecked():
        	value_txt=self.username.GetValue()+"_UPLOAD"
        	self.username.SetValue(value_txt)
        	
        else:
					upload_trim=self.username.GetValue().split("_UPLOAD")[0]
					self.username.SetValue(upload_trim)
     
    def submit_to_dailies(self, event):
        print "submit_to_dailies"
        user_name=self.username.GetValue()
        user_sup_name=self.sup_list.GetValue()
        user_dailies_no=str(self.spin_no.GetValue()).zfill(2)
		
        if self.review_path!="" and user_name!="" and user_sup_name!="" and user_dailies_no!="":
			print "succeed"
			self.write_review_json_by_artist(user_sup_name,user_name,self.review_path,user_dailies_no)
			self.parent.SetSizeWH(250,350)
			sup_name=self.sup_list.GetValue()
			self.artist_list.ClearAll()
			artist_data=self.get_artist_list_by_sup(sup_name)
			i=0
			get_max_avail_no=0
			if sup_name!="" and len(artist_data)>0:
				for each_artist in  artist_data:
					self.artist_list.InsertStringItem(i,each_artist)
					i=i+1
				get_max_avail_no=str(artist_data[len(artist_data)-1]).split(" :> ")[0]
			self.spin_no.ChangeValue(str(int(get_max_avail_no)+1))
			self.review_path=""
			self.username.SetValue(self.username_txt)
			self.cb_upload.SetValue(False)
			
        else:
			Boxdlg = wx.MessageDialog(self, 'Required input is not provided correctly!! ', 'Error', wx.OK | wx.ICON_ERROR)
			Boxdlg.ShowModal()

		
    def refresh_proc(self, event):
        print "Hello", self.sup_list.GetValue()
        sup_name=self.sup_list.GetValue()
        self.artist_list.ClearAll()
        artist_data=self.get_artist_list_by_sup(sup_name)
        i=0
        get_max_avail_no=0
        if sup_name!="":
			for each_artist in  artist_data:
				self.artist_list.InsertStringItem(i,each_artist)
				i=i+1
			try:
				get_max_avail_no=str(artist_data[len(artist_data)-1]).split(" :> ")[0]
				print get_max_avail_no
				self.spin_no.ChangeValue(str(int(get_max_avail_no)+1))
			except:
				self.spin_no.ChangeValue(str(int(get_max_avail_no)+1))
        else:
			Boxdlg = wx.MessageDialog(self, 'Please select supervisor name!! ', 'Error', wx.OK | wx.ICON_ERROR)
			Boxdlg.ShowModal()
    def get_artist_list_by_sup(self,sup_name):
        artist_listt=[]
        if sup_name!="":	
			f=open(self.review_artist_list)
			json_data=json.loads(f.read())
			f.close()
			json_dailies=json_data['dailies']
			if sup_name in json_dailies.keys():
				all_data=json_data['dailies'][sup_name]
				for each_artist in all_data:
					value_append=str(each_artist['no'])+" :> "+str(each_artist['name'])
					artist_listt.append(value_append)
				artist_listt.sort()
				print artist_listt
        return artist_listt

    def get_artist_occupied_review_no(self,sup_name):
        artist_no=[]
        if sup_name!="":	
			f=open(self.review_artist_list)
			json_data=json.loads(f.read())
			f.close()
			json_dailies=json_data['dailies']
			if sup_name in json_dailies.keys():
				all_data=json_data['dailies'][sup_name]
				for each_no in all_data:
					value_append=int(each_no['no'])
					artist_no.append(value_append)
				artist_no.sort()
        return artist_no		
    def review_sup_list(self):
		f=open(self.review_sup)
		json_sup=json.loads(f.read())
		list_review_sup=json_sup['review_sup']
		sup_list=[]
		for each_sup in list_review_sup.keys():
			print each_sup
			sup_list.append(each_sup.encode('utf-8'))
		return sup_list
    
    def write_review_json_by_artist(self,sup_name,user_name,review_path,no):
		all_occupied_no=self.get_artist_occupied_review_no(sup_name)
		print all_occupied_no
		no=int(no)
		if int(no) in  all_occupied_no:
			print "Sup Name ", sup_name ," already exists with no " , no
			while  int(no)  in all_occupied_no:
				print "Enter in while"
				no=int(no)+1
				print no
			print "new no" ,str(no).zfill(2)
			no=str(no).zfill(2)
		f=open(self.review_artist_list)
		json_data=json.loads(f.read())
		f.close()
		json_dailies=json_data['dailies']
		artist_data={}
		artist_data['name']=user_name
		artist_data['daily_folder']=review_path
		artist_data['no']=str(no).zfill(2)
		artist_data['status']="review"

		if sup_name in  json_dailies.keys():
			print "Sup Name Exists"
			sup_data=json_data['dailies'][sup_name]
			sup_data.append(artist_data)

			json_encoder=json.dumps(json_data,indent=4)
			#print json_encoder
			if json_encoder!="":
				with open(self.review_artist_list,'w') as f:
					f.write(json_encoder)
					f.close()
		else:
			print "Sup Name Not Exists---"
			#print "Sup Name \"" ,sup_name,"\" Not Exists in database \r\n please contact Vedanti to update Database "
			list_of_artist=[]
			list_of_artist.append(artist_data)
			new_sup={}
			new_sup[sup_name]=list_of_artist
			#print new_sup
			json_dailies.update(new_sup)
			json_encoder=json.dumps(json_data,indent=4)
			#print json_encoder
			if json_encoder!="":
				with open(self.review_artist_list,'w') as f:
					f.write(json_encoder)
					f.close()
app = wx.PySimpleApp()
# create a window/frame, no parent, -1 is default ID
# change the size of the frame to fit the backgound sourceImages
frame1 = wx.Frame(None, -1, "QUEUE v1.23", size=(250, 350), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
main_path="C:/ReviewSoftware"
Icon_win=os.path.join(main_path,'QUEUE','sourceImages','QUEUE.ico').replace("\\","/")
frame1.SetIcon(wx.Icon(Icon_win, wx.BITMAP_TYPE_ICO))
# create the class instance
panel1 = review(frame1, -1,main_path)
frame1.Show(True)
app.MainLoop()
