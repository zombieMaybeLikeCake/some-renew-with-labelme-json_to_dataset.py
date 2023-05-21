# some-renew-with-labelme-json_to_dataset.py
這是一個改善labelme json_to_dataset.py 功能的程式碼 可以將src資料夾內的.json全部轉成maskrcnn所要求的規格
# Requirement
  you should have labelme 
  
  and replace this file to json_to_dataset.py in labelme/cli
  
  the path is like  C:\Users\username\AppData\Roaming\Python\Python310\site-packages\labelme
# The  command you should use
  labelme_json_to_dataset srcpath -o outpath
 
 example:labelme_json_to_dataset C:\\Users\\robert\\Desktop\\temp -o C:\\Users\\robert\\Desktop\\output
