# create a background image on a wxPython panel
# and show a button on top of the image
 
import wx
import os
import json
import json
import datetime
import subprocess
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
            image_file2 =os.path.join(main_path,'QUEUE','sourceImages','QUEUEREFRESH.jpg').replace("\\","/")
            image_file3 = os.path.join(main_path,'QUEUE','sourceImages','QUEUECHECKED.jpg').replace("\\","/")


            image1 =wx.Image(image_file2,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            image2 =wx.Image(image_file3,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            #image3 =wx.Image(image_file4,wx.BITMAP_TYPE_ANY).ConvertToBitmap()			
            #image111 =wx.Image(image_file5,wx.BITMAP_TYPE_ANY).ConvertToBitmap()			

            bmp1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            # image's upper left corner anchors at panel coordinates (0, 0)
            self.bitmap1 = wx.StaticBitmap(self, -1, bmp1, (0, 0))
            # show some image details
            str1 = "%s  %dx%d" % (image_file, bmp1.GetWidth(), bmp1.GetHeight()) 
            #parent.SetTitle(str1)
        except IOError:
            print "Image file %s not found" % imageFile
            raise SystemExit
        self.but_refresh = wx.BitmapButton(self.bitmap1, id=-1, bitmap=image1, pos=(5,5),size=(232,25))
        self.but_refresh.Bind(wx.EVT_BUTTON,self.refresh_proc) 
        # button goes on the image --> self.bitmap1 is the parent
        zone_list=[]
        self.artist_list = wx.ListBox(self.bitmap1, 50, ( 5,35), (232, 280), zone_list,wx.LB_HSCROLL
                                           | wx.LB_EXTENDED
                                           | wx.LB_NEEDED_SB
                                           | wx.LB_SORT)
        self.artist_list.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
        col=wx.NamedColor('RED')

        #self.artist_list.SetBackgroundColour('RED')
        self.artist_list.SetItemBackgroundColour(0, col)

        self.checked_artist_Review = wx.BitmapButton(self.bitmap1, id=-1, bitmap=image2, pos=(5,320),size=(232,30))
        self.devetext=wx.StaticText(self.bitmap1, id=-1, label="Developed By Vedanti Bhanuse", pos=(95,358))
        self.devetext.SetBackgroundColour((28,88,155))
        self.checked_artist_Review.Bind(wx.EVT_BUTTON,self.delete_artist) 

        self.artist_list.Bind(wx.EVT_LISTBOX_DCLICK	, self.explorer_path)
        artist_data=self.get_artist_list_by_sup(str(os.getenv("USERNAME")))
        i=0
        self.artist_list.Clear()
        try:
	
			for each_artist in  artist_data:
				self.artist_list.Insert(each_artist,i)
				i=i+1
				self.artist_list.SetItemBackgroundColour(i, col)

        except:
			pass
    def delete_artist(self, event):
		sup_name=os.getenv("USERNAME")
		artist_index=self.artist_list.GetSelections()
		for each_artist_index in artist_index:
			res=self.artist_list.GetString(int(each_artist_index))
			artist_nono=res.split(":> ")[0]
			artist_name=res.split(":> ")[1]
			self.delete_artist_from_json(sup_name,artist_name,artist_nono)
			sup_name=os.getenv("USERNAME")
		self.artist_list.Clear()
		artist_data=self.get_artist_list_by_sup(sup_name)
		i=0
		get_max_avail_no=0
		if sup_name!="":
			for each_artist in  artist_data:
				self.artist_list.Insert(each_artist,i)
				i=i+1		
    def delete_artist_from_json(self,sup_name,name,no):
		f=open(self.review_artist_list)
		json_data=json.loads(f.read())
		f.close()
		json_dailies=json_data['dailies']
		if sup_name in json_dailies.keys():
			sup_data=json_data['dailies'][sup_name]
			i=0
			for each_artist in sup_data:
				if (each_artist["name"]).encode('utf-8')==name and (each_artist["no"]).encode('utf-8')==no:
					sup_data.pop(i)
				i=i+1
			json_encoder=json.dumps(json_data,indent=4)
			if json_encoder!="":
				with open(self.review_artist_list,'w') as f:
					f.write(json_encoder)
					f.close()
		else:
			print sup_name , " Not Exists in database!"	

    def explorer_path(self, event):
        res=self.artist_list.GetString(int(self.artist_list.GetSelections()[0]))
        artist_nono=res.split(":> ")[0]
        artist_name=res.split(":> ")[1]
        artist_review_path=self.get_review_path(os.getenv("USERNAME"),artist_name,artist_nono)
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
		

    def refresh_proc(self, event):
        sup_name=os.getenv("USERNAME")
        print sup_name
        self.artist_list.Clear()
        artist_data=self.get_artist_list_by_sup(sup_name)
        i=0
        get_max_avail_no=0
        if sup_name!="":
			for each_artist in  artist_data:
				self.artist_list.Insert(each_artist,i)
				self.artist_list.SetItemForegroundColour(i,c='#0000FF')
				i=i+1
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
					value_append=str(each_artist['no'])+":> "+str(each_artist['name'])
					artist_listt.append(value_append)
				artist_listt.sort()
				print artist_listt
        return 	artist_listt

   

app = wx.PySimpleApp()
# create a window/frame, no parent, -1 is default ID
# change the size of the frame to fit the backgound sourceImages
frame1 = wx.Frame(None, -1, "QUEUE v1.23", size=(250, 420), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
main_path="C:/ReviewSoftware"
Icon_win=os.path.join(main_path,'QUEUE','sourceImages','QUEUE.ico').replace("\\","/")
frame1.SetIcon(wx.Icon(Icon_win, wx.BITMAP_TYPE_ICO))
# create the class instance
panel1 = review(frame1, -1,main_path)
frame1.Show(True)
app.MainLoop()
