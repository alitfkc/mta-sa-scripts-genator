from tkinter import filedialog
import os
import shutil
#Global Args
global create_type
create_type = False

global acl_group_mode
acl_group_mode = False

global data_mode
data_mode = False

global save_location
save_location = False

type_list= {
    1:"Vehicle",
    2:"Ped",
    3:"Object",
    4:"Weapon"
}

meta_type = {
    1:'<meta>\n  <info author="Meta Scripts" version="1.0" type="script" name="{}"/>\n  <script src="client.lua" type="client" />\n  <file src="{}" />\n     <file src="{}" />\n</meta>',
    2:'<meta>\n  <info author="Meta Scripts" version="1.0" type="script" name="{}"/>\n  <script src="client.lua" type="client" />\n   <script src="server.lua" type="server" />\n  <file src="{}" />\n     <file src="{}" />\n</meta>'
}


data_type = {
    #Client
    1:"addEventHandler('onClientVehicleStartEnter', root, function(player,seat,door)\n	if (player == localPlayer and seat == 0 and getElementModel(source) == {id})then\n        if not getElementData(localPlayer,'{data_name}') then \n            cancelEvent()\n        end\n	end\nend)",
    2:"function informPlayerOnModelChange(oldModel, newModel)\n    if  source == localPlayer and newModel == {id} then \n        if not getElementData(localPlayer,'{data_name}') then \n            setElementModel(localPlayer,oldModel)\n        end\n    end\nend\naddEventHandler('onClientElementModelChange', root, informPlayerOnModelChange) ",
    #Server
    4:"addEventHandler ( 'onPlayerWeaponSwitch', getRootElement (),function ( previousWeaponID, currentWeaponID )\n    if currentWeaponID ==  {id} then\n        if not getElementData(source,'{data_name}') then \n            takeWeapon(source,'{id}')\n        end\n    end\nend)"
}


acl_type = {
    1:"addEventHandler('onVehicleStartEnter', root, function(player,seat,door)\n	if  seat == 0 and getElementModel(player) == {id}then\n        if not isObjectInACLGroup ('user.'..getAccountName ( getPlayerAccount ( player ) ), aclGetGroup ( '{acl_name}' ) ) then \n            cancelEvent()\n        end\n	end\nend)",
    2:"function informPlayerOnModelChange(oldModel, newModel)\n    if  ( getElementType(source) == 'player' ) and newModel == {id} then \n        if not isObjectInACLGroup ('user.'..getAccountName ( getPlayerAccount ( source ) ), aclGetGroup ( '{acl_name}' ) ) then \n            setElementModel(source,oldModel)\n        end\n    end\nend\naddEventHandler('onElementModelChange', root, informPlayerOnModelChange) ",
    4:"addEventHandler ( 'onPlayerWeaponSwitch', getRootElement (),function ( previousWeaponID, currentWeaponID )\n    if currentWeaponID ==  {id} then\n        if not isObjectInACLGroup ('user.'..getAccountName ( getPlayerAccount ( source ) ), aclGetGroup ( '{acl_name}' ) ) then  \n            takeWeapon(source,'{id}')\n        end\n    end\nend)"
}

client_code_block = "function {name}()\n    local txd = engineLoadTXD ('{object_txd}')\n    engineImportTXD(txd,{id})\n    local dff = engineLoadDFF('{object_dff}',{id})\n    engineReplaceModel(dff,{id})\nend\naddEventHandler('onClientResourceStart',getResourceRootElement(getThisResource()),{name})"

#file selector
def select_file(state):
    if state:
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("txd files", "*.txd"),))
        return filename
    else:
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("dff files", "*.dff"),))
        return filename
    


#MTA:SA Script creator
def create(create_type,id,txd_file,dff_file,acl_group,mode_acl,data_name,mode_data):
    global save_location
    if save_location:
        folder_name = type_list[create_type]+"_"+ str(id)
        way = save_location +"/"+ folder_name
        os.mkdir(way)
        folder_name = way
    else:
        folder_name = type_list[create_type]+"_"+ str(id)
        os.mkdir(folder_name)

    #Transfer TXD and DFF File
    shutil.copy(txd_file, folder_name)
    shutil.copy(dff_file, folder_name)

    #Model file 
    model_txd = os.path.basename(txd_file)
    model_dff = os.path.basename(dff_file)

    #Create Meta
    os.path.join(folder_name,"meta.xml") 
    if mode_acl:
        file = open(folder_name+"/"+"meta.xml", "w")
        file.write(meta_type[2].format(type_list[create_type]+"_"+ str(id),model_txd,model_dff))
        file.close()
    elif mode_data and create_type == 4 :
        file = open(folder_name+"/"+"meta.xml", "w")
        file.write(meta_type[2].format(type_list[create_type]+"_"+ str(id),model_txd,model_dff))
        file.close()
    else:
        file = open(folder_name+"/"+"meta.xml", "w")
        file.write(meta_type[1].format(type_list[create_type]+"_"+ str(id),model_txd,model_dff))
        file.close()

    #Create Client
    client_code = client_code_block.format(name = folder_name,id = id,object_txd = model_txd,object_dff= model_dff)

    if mode_data and float(create_type) <= 2:
        client_code = client_code +"\n\n\n"+ data_type[create_type].format(id = id,data_name = data_name)
    os.path.join(folder_name,"client.lua") 
    file = open(folder_name+"/"+"client.lua", "w")
    file.write(client_code)
    file.close()

    #Create Server
    if mode_acl and create_type != 3:
        server_code = acl_type[create_type].format(id = id ,acl_name = acl_group)
        if mode_data and create_type == 4:
            server_code = server_code + "\n\n\n" + data_type[create_type].format(id = id,data_name = data_name)
        os.path.join(folder_name,"server.lua") 
        file = open(folder_name+"/"+"server.lua", "w")
        file.write(server_code)
        file.close()
    else:
        if mode_data and create_type == 4:
            server_code = "\n\n\n" + data_type[create_type].format(id = id,data_name = data_name)
            os.path.join(folder_name,"server.lua") 
            file = open(folder_name+"/"+"server.lua", "w")
            file.write(server_code)
            file.close()


#Select save location
def select_save_location():
    filename = filedialog.askdirectory()
    global save_location
    save_location = filename