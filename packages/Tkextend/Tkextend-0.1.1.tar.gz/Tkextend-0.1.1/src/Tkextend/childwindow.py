from tkinter import *
import tkinter
import os
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
from tkinter import scrolledtext
from threading import Thread, RLock
'''lib'''
_img_index = 0
_all_=[]
_image = {'red':'red_button.png','yellow':'yellow_button.png','gray':'gray_button.png','green':'green_button.png'}
_image_s = {'red':'red_button_s.png','yellow':'yellow_button_s.png','gray':'gray_button_s.png','green':'green_button_s.png'}
_image_xp = {'red':'red_xp.png','yellow':'full_xp.png','green':'white_xp.png'}
old_x,old_y,new_event_x,root_event_y = 0,0,0,0
CAN_BIND_POINT = False
'''start'''
txt = ""
def EDITOR(window,args={'T_w':100,'T_h':100,'C_w':7,'C_bg':'#DCDCDC','C_fg':'black','T_bg':'white','font':("Consolas", 11,'bold'),'T_fg':'black','selectbackground': "#4E4E4E",'insertbackground':'black'}):
	global txt
	args_start:dict={'T_w':100,'T_h':100,'C_w':7,'C_bg':'#DCDCDC','C_fg':'black','T_bg':'white','font':("Consolas", 11,'bold'),'T_fg':'black','selectbackground': "#4E4E4E",'insertbackground':'black'}
	args_start.update(args)
	args=args_start
	T_w = args['T_w']
	T_h = args['T_h']
	C_w = args['C_w']
	thread_lock = RLock()
	def wheel(event):
	    line_text.yview_scroll(int(-1 * (event.delta / 120)), "units")
	    edit_text.yview_scroll(int(-1 * (event.delta / 120)), "units")
	    return "break"
	def scroll(*xy):
	    line_text.yview(*xy)
	    edit_text.yview(*xy)
	def get_txt_thread():
	    Thread(target=get_txt).start()
	def get_txt():
	    global txt
	    thread_lock.acquire()
	    if txt != edit_text.get("1.0", "end")[:-1]:
	        txt = edit_text.get("1.0", "end")[:-1]
	        show_line()
	    else:
	        thread_lock.release()
	def show_line():
	    sb_pos = edit_text.vbar.get()
	    line_text.configure(state="normal")
	    line_text.delete("1.0", "end")
	    txt_arr = txt.split("\n")
	    if len(txt_arr) == 1:
	        line_text.insert("1.1", " 1")
	    else:
	        for i in range(1, len(txt_arr) + 1):
	            line_text.insert("end", " " + str(i))
	            if i != len(txt_arr):
	                line_text.insert("end", "\n")
	    if len(sb_pos) == 4:
	        line_text.yview_moveto(0.0)
	    elif len(sb_pos) == 2:
	        line_text.yview_moveto(sb_pos[0])
	        edit_text.yview_moveto(sb_pos[0])
	    line_text.configure(state="disabled")
	    try:
	        thread_lock.release()
	    except RuntimeError:
	        pass
	    edit_text.see(edit_text.index('insert'))

	edit_frame = Canvas(window, height=T_h, width=T_w,
	                         bg="white", highlightthickness=0)
	line_text = Text(edit_frame, width=C_w, height=T_h, spacing3=5,
	                      bg=args['C_bg'], bd=0, font=args['font'], takefocus=0, state="disabled",
	                      cursor="arrow",fg=args['C_fg'])
	line_text.pack(side="left", expand="no")
	window.update()
	edit_text = scrolledtext.ScrolledText(edit_frame, height=1, wrap="none", spacing3=5,
	                                           width=window.winfo_width() - line_text.winfo_width(), bg=args['T_bg'],
	                                           bd=0, font=('Consolas',11), undo=True, insertwidth=1,fg=args['T_fg'],selectbackground=args['selectbackground'],insertbackground=args['insertbackground'])
	edit_text.vbar.configure(command=scroll)
	edit_text.pack(side="left", fill="both")
	line_text.bind("<MouseWheel>", wheel)
	edit_text.bind("<MouseWheel>", wheel)
	edit_text.bind("<Control-v>", lambda e: get_txt_thread())
	edit_text.bind("<Control-V>", lambda e: get_txt_thread())
	edit_text.bind("<Key>", lambda e: get_txt_thread())
	show_line()
	return edit_frame,edit_text
def set(window,args={'back_move':False,'pass_through':True,'point':True},fun=None):
	global CAN_BIND_POINT
	args_start:dict={'back_move':False,'pass_through':True,'point':True}
	args_start.update(args)
	args=args_start
	pass_through = args['pass_through']
	if args['back_move'] == True:
		def newstart(event):
			for i in _all_:
				Widgets = i
				globals()['old_y'+str(i)],globals()['old_x'+str(i)] = int(Widgets.place_info()['y']),int(Widgets.place_info()['x'])
				globals()['old_event_y'+str(i)],globals()['old_event_x'+str(i)] = event.y_root,event.x_root
		def newonmotion(event):
			for i in _all_:
				Widgets = i
				_x,_y = event.x_root,event.y_root
				yd,xd = _y-globals()['old_event_y'+str(i)]+globals()['old_y'+str(i)],_x-globals()['old_event_x'+str(i)]+globals()['old_x'+str(i)]
				if pass_through == False:
					if xd < 0:
						xd = 0
					elif xd > window.winfo_width() - width-bd*2:
						xd = window.winfo_width() - width-bd*2
					if yd > window.winfo_height() - height-bd*2-title_height:
						yd = window.winfo_height() - height-bd*2-title_height
					elif yd < 0:
						yd = 0
					Widgets.place(x=xd,y=yd)
				else:
					Widgets.place(x=xd,y=yd)
		window.bind('<2>',newstart)
		window.bind("<B2-Motion>",newonmotion)
#f -> set
def hex_to_rgb(hex_color):
	r = int('0x' + hex_color[1:3],16)
	g = int('0x' + hex_color[3:5],16)
	b = int('0x' + hex_color[5:7],16)
	return (r,g,b)
def button_image_make(color,_button={'style':'_mac','IfReturn':True,'use':('red','yellow','green')})->str:
	_button_={'style':'_mac','IfReturn':True,'use':('red','yellow','green')}
	_button_.update(_button)
	_button = _button_
	global _img_index
	rgb = hex_to_rgb(color)
	_return = []
	button_list = []
	if _button['style'] == '_mac':
		for i in _button['use']:
			button_list.append(_image[i])
	elif _button['style'] == '_simple':
		for i in _button['use']:
			button_list.append(_image_s[i])
	elif _button['style'] == '_winxp':
		for i in _button['use']:
			button_list.append(_image_xp[i])
	for i in button_list:
		img = Image.open(i)
		img = img.convert("RGB")
		pixdata = img.load()
		for y in range(img.size[1]): 
			for x in range(img.size[0]):
				if pixdata[x, y] == (0,0,0):
					pixdata[x, y] = rgb
		img.save('temp_'+str(_img_index)+''.join(i.split('.')[:-1])+'.png')
		_return.append('temp_'+str(_img_index)+''.join(i.split('.')[:-1])+'.png')
	_img_index += 1
	return _return
class HoverButton(tkinter.Button):
	def __init__(self, master, **kw):
		tkinter.Button.__init__(self,master=master,**kw)
		self.defaultBackground = self['background']
		self.bind("<Enter>", self.on_enter)
		self.bind("<Leave>", self.on_leave)
	def on_enter(self, e):
		self['background'] = self['activebackground']
	def on_leave(self, e):
		self['background'] = self.defaultBackground
def Bind_Move(widget,window,pass_through=True,width=0,height=0,bd=0,title_height=15,func=None):
	def StartMove(event):
		global old_x,old_y,old_event_x,old_event_y
		Widgets = event.widget
		old_y,old_x = int(Widgets.place_info()['y']),int(Widgets.place_info()['x'])
		old_event_y,old_event_x = event.y_root,event.x_root
	def OnMotion(event):
		global old_x,old_y#new_event_x,new_event_y
		Widgets = event.widget
		_x,_y = event.x_root,event.y_root
		yd,xd = _y-old_event_y+old_y,_x-old_event_x+old_x
		if pass_through == False:
			if xd < 0:
				xd = 0
			elif xd > window.winfo_width() - width-bd*2:
				xd = window.winfo_width() - width-bd*2
			if yd > window.winfo_height() - height-bd*2-title_height:
				yd = window.winfo_height() - height-bd*2-title_height
			elif yd < 0:
				yd = 0
			Widgets.place(x=xd,y=yd)
		else:
			Widgets.place(x=xd,y=yd)
		Widgets.tkraise()
	widget.bind("<ButtonPress-1>",StartMove)
	widget.bind("<B1-Motion>", OnMotion)
	return widget
'''window creator method start'''
def _if(a,v,b):
	if a == v:
		return a
	else:
		return b
def Create_Window(master,name,width,height,x,y,bg='white',tc='',style='_window',args={'Shadow_color':'','font':'Microsoft JhengHei','button_color':'#7F7F7F','font_size':15,'title_x':3,'title_color':'white','ico':'','title_height':25,'bd':1,'exit':True,'name':True,'bd_x':0,'bd_y':0,'pass_through':True,'full_screen':False,'change_size':False,'Shadow':False,'exit_color':'white','fullscreen_color':'white','max_size':(0,0),'min_size':(0,0)},bd=2,fullscreen=False,can_move=True,func=None,binding_function=None,exit_function=None):
	global _img_index,_all_
	'''>len(Creat_Window) -> 6*Necessary , 6*Optional [Optional.args : dict => len:17 ] ==> (29)
		There is some interaction between them (parameters) ，I try to extend the function of subwindow on tkinter，
		This function is very big, and I can't guarantee that it will run well :( , I will try my best...'''
	args_start:dict={'Shadow_color':'','window_bd_color':'#BBBBBB','font':'Microsoft JhengHei','button_color':'#7F7F7F','font_size':15,'title_x':3,'title_color':'white','ico':'','title_height':25,'bd':1,'exit':True,'name':True,'bd_x':0,'bd_y':0,'pass_through':True,'full_screen':False,'change_size':False,'Shadow':False,'exit_color':'white','fullscreen_color':'white','max_size':(0,0),'min_size':(0,0),'window_bd_color':'#BBBBBB'}
	args_start.update(args)
	args=args_start
	#print(args)
	if style == '_window':
		if args['font'] == '':
			args['font'] == 'Microsoft JhengHei'
		if args['bd_x'] != 0 and args['bd_y'] != 0:
			globals()[name+'_window'] = Frame(master,width=width+bd*2,height=height+bd*2+args['title_height'],bg=tc,highlightthickness=bd,highlightbackground=args['window_bd_color'],highlightcolor=args['window_bd_color'])
				# Initialize the main window -> Tkinter.Frame :[name + '_window']
			globals()[name] = Frame(globals()[name+'_window'],bg=bg,width=width,height=height)
			globals()[name].place(x=bd,y=bd+args['title_height'],width=width,height=height)
			globals()[name+'_window'].place(x=x,y=y)
		else:
			globals()[name+'_window'] = Frame(master,width=width+args['bd_x']*2+args['bd']*2,height=height+args['bd_y']*2+args['bd']*2+args['title_height'],bg=tc,highlightthickness=args['bd'],highlightbackground=args['window_bd_color'],highlightcolor=args['window_bd_color'])
				# Initialize the main window -> Tkinter.Frame :[name + '_window']
			globals()[name] = Frame(globals()[name+'_window'],bg=bg,width=width,height=height)
			# Initialize the personal window -> Tkinter.Frame :[name]
			globals()[name].place(x=args['bd_x'],y=args['bd_y']+args['title_height'],width=width,height=height)
			globals()[name+'_window'].place(x=x,y=y)
			#Draw the windows
		def _exit():
			globals()[name+'_window'].destroy()
			if exit_function != None:
				exit_function()
		def _full_screen():
			pass
		def _small():
			pass
		exit = HoverButton(globals()[name+'_window'],text='x',font=('Consolas',args['font_size']),command=_exit,activeforeground=args['title_color'],activebackground=args['button_color'],bd=0,bg=tc,fg=args['title_color'])
		exit.place(x=width-24,y=0,height=args['title_height'])
		HoverButton(globals()[name+'_window'],text='□',font=('Consolas',args['font_size']),command=_full_screen,activeforeground=args['title_color'],activebackground=args['button_color'],bd=0,bg=tc,fg=args['title_color']).place(x=width-48,y=0,height=args['title_height'])
		HoverButton(globals()[name+'_window'],text='-',font=('Consolas',args['font_size']),command=_small,bd=0,activeforeground=args['title_color'],activebackground=args['button_color'],bg=tc,fg=args['title_color']).place(x=width-72,y=0,height=args['title_height'])
		Label(globals()[name+'_window'],text=name,font=(args['font'],args['font_size']-5),bd=0,bg=tc,fg=args['title_color']).place(x=args['title_x'],y=0,height=args['title_height'])
		if can_move == True:
			Bind_Move(globals()[name+'_window'],master,pass_through=args['pass_through'],width=width,height=height,bd=bd,title_height=args['title_height'],func=func)
		_all_.append(globals()[name+'_window'])
		if binding_function != None:
			binding_function(globals()[name+'_window'])
		return globals()[name],exit,globals()[name+'_window']
			#return [name] and [name+'_window']
	elif style == '_mac':
		if args['font'] == '':
			args['font'] == 'Consolas'
		globals()[name+'_mac'] = Frame(master,width=width+bd*2,height=height+bd*1+args['title_height'],bg=tc)
			# Initialize the main window -> Tkinter.Frame :[name + '_window']
		'''made style'''
		_list = [12,9,7,6,5]
		Label(globals()[name+'_mac'],bd=2,bg='#CCCCCC').place(x=0,y=args['title_height']+1,width=width+bd*2,height=1)
		Label(globals()[name+'_mac'],bd=2,bg='#BBBBBB').place(x=0,y=args['title_height']+2,width=width+bd*2,height=1)
		_height=height+args['title_height']+bd*2
		if args['Shadow_color'] == '':
			mbg = master['background']
		else:
			mbg = args['Shadow_color']
		for i in range(5):
			Label(globals()[name+'_mac'],bg=mbg).place(x=0,y=i,width=_list[i],height=1)
		for i in range(5):
			Label(globals()[name+'_mac'],bg=mbg).place(x=i,y=0,width=1,height=_list[i])
		for i in range(5):
			Label(globals()[name+'_mac'],bg=mbg).place(x=width+bd*2-_list[i],y=i,width=_list[i],height=1)
		for i in range(5):
			Label(globals()[name+'_mac'],bg=mbg).place(x=width+bd*2-i-1,y=0,width=1,height=_list[i])
		'''made end'''
		globals()[name] = Frame(globals()[name+'_mac'],bg=bg,width=width,height=height)
			# Initialize the personal window -> Tkinter.Frame :[name]
		globals()[name].place(x=0,y=bd+args['title_height'],width=width+bd*2,height=height)
		globals()[name+'_mac'].place(x=x,y=y,height=height+bd*1+args['title_height'])
			#Draw the windows
		_button_get = button_image_make(tc)
			#get the button files
		globals()['imgOne'+str(_img_index)] = ImageTk.PhotoImage(Image.open(_button_get[0]))#red
		globals()['imgTwo'+str(_img_index)] = ImageTk.PhotoImage(Image.open(_button_get[1]))
		globals()['imgThr'+str(_img_index)] = ImageTk.PhotoImage(Image.open(_button_get[2]))
		def _exit():
			globals()[name+'_mac'].destroy()
			if exit_function != None:
				exit_function()
		def _full_screen():
			pass
		def _small():
			pass
		exit = HoverButton(globals()[name+'_mac'],image=globals()['imgOne'+str(_img_index)],command=_exit,activeforeground=args['title_color'],activebackground=args['button_color'],bd=0,bg=tc,fg=args['exit_color'])
		exit.place(x=15,y=bd,height=args['title_height']-5)
		HoverButton(globals()[name+'_mac'],image=globals()['imgTwo'+str(_img_index)],command=_full_screen,activeforeground=args['title_color'],activebackground=args['button_color'],bd=0,bg=tc,fg=args['title_color']).place(x=15+2+23,y=bd,height=args['title_height']-5)
		HoverButton(globals()[name+'_mac'],image=globals()['imgThr'+str(_img_index)],command=_small,bd=0,activeforeground=args['title_color'],activebackground=args['button_color'],bg=tc,fg=args['title_color']).place(x=17+23+2+23,y=bd,height=args['title_height']-5)
		Label(globals()[name+'_mac'],text=name,font=('Consolas',args['font_size']-5),bd=0,bg=tc,fg=args['title_color']).place(x=width/2-len(name)*4,y=bd)
		if can_move == True:
			Bind_Move(globals()[name+'_mac'],master,pass_through=args['pass_through'],width=width,height=height,bd=bd,title_height=args['title_height'],func=func)
		_img_index += 1
		_all_.append(globals()[name+'_mac'])
		if binding_function != None:
			binding_function(globals()[name+'_mac'])
		return globals()[name],exit,globals()[name+'_mac']
			#return [name] and [name+'_window']
	elif style == '_simple':
		def _exit():
			globals()[name+'_simple'].destroy()
			if exit_function != None:
				exit_function()
		def _full_screen():
			pass
		def _small():
			pass
		_button_get = button_image_make(tc,_button={'style':'_simple','use':('red','yellow','gray')})
		print(_button_get)
		globals()['imgOne'+str(_img_index)] = ImageTk.PhotoImage(Image.open(_button_get[0]))#red
		globals()['imgTwo'+str(_img_index)] = ImageTk.PhotoImage(Image.open(_button_get[1]))
		globals()['imgThr'+str(_img_index)] = ImageTk.PhotoImage(Image.open(_button_get[2]))
		globals()[name+'_simple'] = Frame(master,width=width+bd*2,height=height+bd*4+args['title_height'],bg=tc)
		globals()[name] = Frame(globals()[name+'_simple'],bg=bg,width=width,height=height)
			# Initialize the personal window -> Tkinter.Frame :[name]
		globals()[name].place(x=bd,y=bd+args['title_height'],width=width,height=height)
		globals()[name+'_simple'].place(x=x,y=y,height=height+bd*4+args['title_height'])
		Label(globals()[name+'_simple'],text=name,font=(args['font'],args['font_size']-5),bd=0,bg=tc,fg=args['title_color']).place(x=args['title_x'],y=0,height=args['title_height'])
		exit = HoverButton(globals()[name+'_simple'],image=globals()['imgOne'+str(_img_index)],command=_exit,activeforeground=args['title_color'],activebackground=args['button_color'],bd=0,bg=tc,fg=args['exit_color'])
		exit.place(x=width-24,y=bd,height=args['title_height']-5)
		HoverButton(globals()[name+'_simple'],image=globals()['imgTwo'+str(_img_index)],command=_full_screen,activeforeground=args['title_color'],activebackground=args['button_color'],bd=0,bg=tc,fg=args['title_color']).place(x=width-48,y=bd,height=args['title_height']-5)
		HoverButton(globals()[name+'_simple'],image=globals()['imgThr'+str(_img_index)],command=_small,bd=0,activeforeground=args['title_color'],activebackground=args['button_color'],bg=tc,fg=args['title_color']).place(x=width-72,y=bd,height=args['title_height']-5)
		if can_move == True:
			Bind_Move(globals()[name+'_simple'],master,pass_through=args['pass_through'],width=width,height=height,bd=bd,title_height=args['title_height'],func=func)
		_img_index += 1
		_all_.append(globals()[name+'_simple'])
		if binding_function != None:
			binding_function(globals()[name+'_simple'])
		return globals()[name],exit,globals()[name+'_simple']
	elif style == '_winxp':
		if tc == '':
			tc = '#436EEE'
		def _exit():
			globals()[name+'_winxp'].destroy()
			if exit_function != None:
				exit_function()
		def _full_screen():
			pass
		def _small():
			pass
		_button_get = button_image_make(tc,_button={'style':'_winxp'})
		print(_button_get)
		globals()['imgOne'+str(_img_index)] = ImageTk.PhotoImage(Image.open(_button_get[0]))#red
		globals()['imgTwo'+str(_img_index)] = ImageTk.PhotoImage(Image.open(_button_get[1]))
		globals()['imgThr'+str(_img_index)] = ImageTk.PhotoImage(Image.open(_button_get[2]))
		globals()[name+'_winxp'] = Frame(master,width=width+bd*2,height=height+bd*2+args['title_height'],bg=tc)
		globals()[name] = Frame(globals()[name+'_winxp'],bg=bg,width=width,height=height)
			# Initialize the personal window -> Tkinter.Frame :[name]
		globals()[name].place(x=bd,y=bd+args['title_height'],width=width,height=height)
		globals()[name+'_winxp'].place(x=x,y=y,height=height+bd*2+args['title_height'])
		Label(globals()[name+'_winxp'],text=name,font=(args['font'],args['font_size']-5),bd=0,bg=tc,fg=args['title_color']).place(x=args['title_x'],y=0,height=args['title_height'])
		exit = HoverButton(globals()[name+'_winxp'],image=globals()['imgOne'+str(_img_index)],command=_exit,activeforeground=args['title_color'],activebackground=args['button_color'],bd=0,bg=tc,fg=args['exit_color'])
		exit.place(x=width-20,y=bd,height=args['title_height']-5)
		HoverButton(globals()[name+'_winxp'],image=globals()['imgTwo'+str(_img_index)],command=_full_screen,activeforeground=args['title_color'],activebackground=args['button_color'],bd=0,bg=tc,fg=args['title_color']).place(x=width-40,y=bd,height=args['title_height']-5)
		HoverButton(globals()[name+'_winxp'],image=globals()['imgThr'+str(_img_index)],command=_small,bd=0,activeforeground=args['title_color'],activebackground=args['button_color'],bg=tc,fg=args['title_color']).place(x=width-60,y=bd,height=args['title_height']-5)
		if can_move == True:
			Bind_Move(globals()[name+'_winxp'],master,pass_through=args['pass_through'],width=width,height=height,bd=bd,title_height=args['title_height'],func=func)
		_img_index += 1
		_all_.append(globals()[name+'_winxp'])
		if binding_function != None:
			binding_function(globals()[name+'_winxp'])
		return globals()[name],exit,globals()[name+'_winxp']
	elif style == '_win11':
		if args['font'] == '':
			args['font'] == 'Consolas'
		globals()[name+'_win11'] = Frame(master,width=width+bd*2,height=height+bd*4+args['title_height'],bg=tc)
			# Initialize the main window -> Tkinter.Frame :[name + '_window']
		'''made style'''
		_list = [8,6,4,3]
		_height=height+args['title_height']+bd*2
		if args['Shadow_color'] == '':
			mbg = master['background']
		else:
			mbg = args['Shadow_color']
		for i in range(4):
			Label(globals()[name+'_win11'],bg=mbg).place(x=0,y=i,width=_list[i],height=1)
		for i in range(4):
			Label(globals()[name+'_win11'],bg=mbg).place(x=i,y=0,width=1,height=_list[i])
		for i in range(4):
			Label(globals()[name+'_win11'],bg=mbg).place(x=width+bd*2-_list[i],y=i,width=_list[i],height=1)
		for i in range(4):
			Label(globals()[name+'_win11'],bg=mbg).place(x=width+bd*2-i-1,y=0,width=1,height=_list[i])
		for i in range(4):
			Label(globals()[name+'_win11'],bg=mbg).place(x=0,y=_height+bd*2-i-1,width=_list[i],height=1)
		for i in range(4):
			Label(globals()[name+'_win11'],bg=mbg).place(x=i,y=_height+bd*2-_list[i],width=1,height=_list[i])
		for i in range(4):
			Label(globals()[name+'_win11'],bg=mbg).place(x=width+bd*2-_list[i],y=_height+bd*2-i-1,width=_list[i],height=1)
		for i in range(4):
			Label(globals()[name+'_win11'],bg=mbg).place(x=width+bd*2-i-1,y=_height+bd*2-_list[i],width=1,height=_list[i])
		'''made end'''
		globals()[name] = Frame(globals()[name+'_win11'],bg=bg,width=width,height=height)
			# Initialize the personal window -> Tkinter.Frame :[name]
		globals()[name].place(x=bd,y=bd+args['title_height'],width=width,height=height)
		globals()[name+'_win11'].place(x=x,y=y,height=height+bd*4+args['title_height'])
			#Draw the windows
		def _exit():
			globals()[name+'_win11'].destroy()
			if exit_function != None:
				exit_function()
		def _full_screen():
			pass
		def _small():
			pass
		exit = HoverButton(globals()[name+'_win11'],text='x',font=('Consolas',args['font_size']),command=_exit,activeforeground=args['title_color'],activebackground=args['button_color'],bd=0,bg=tc,fg=args['title_color'])
		exit.place(x=width-27-5,y=0,height=args['title_height'])
		HoverButton(globals()[name+'_win11'],text='□',font=('Consolas',args['font_size']),command=_full_screen,activeforeground=args['title_color'],activebackground=args['button_color'],bd=0,bg=tc,fg=args['title_color']).place(x=width-54-5,y=0,height=args['title_height'])
		HoverButton(globals()[name+'_win11'],text='-',font=('Consolas',args['font_size']),command=_small,bd=0,activeforeground=args['title_color'],activebackground=args['button_color'],bg=tc,fg=args['title_color']).place(x=width-81-5,y=0,height=args['title_height'])
		Label(globals()[name+'_win11'],text=name,font=(args['font'],args['font_size']-5),bd=0,bg=tc,fg=args['title_color']).place(x=args['title_x']+9,y=0,height=args['title_height'])
		if can_move == True:
			Bind_Move(globals()[name+'_win11'],master,pass_through=args['pass_through'],width=width,height=height,bd=bd,title_height=args['title_height'],func=func)
		_img_index += 1
		_all_.append(globals()[name+'_win11'])
		if binding_function != None:
			binding_function(globals()[name+'_win11'])
		return globals()[name],exit,globals()[name+'_win11']
			#return [name] and [name+'_window']
	elif style == '_board':
		globals()[name+'_board'] = Frame(master,width=width+bd*2,height=height+args['title_height'],bg=tc)
		globals()[name] = Frame(globals()[name+'_board'],bg=bg,width=width,height=height)
			# Initialize the personal window -> Tkinter.Frame :[name]
		globals()[name].place(x=bd,y=bd+args['title_height'],width=width,height=height)
		globals()[name+'_board'].place(x=x,y=y,height=height+args['title_height'])
		Label(globals()[name+'_board'],text=name,font=(args['font'],args['font_size']-5),bd=0,bg=tc,fg=args['title_color']).place(x=args['title_x']+9,y=0,height=args['title_height'])
		if can_move == True:
			Bind_Move(globals()[name+'_board'],master,pass_through=args['pass_through'],width=width,height=height,bd=bd,title_height=args['title_height'],func=func)
		_all_.append(globals()[name+'_board'])
		if binding_function != None:
			binding_function(globals()[name+'_board'])
	else:
		return None,None
