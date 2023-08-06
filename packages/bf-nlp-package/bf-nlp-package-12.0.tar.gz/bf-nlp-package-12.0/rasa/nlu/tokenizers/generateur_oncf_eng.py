import os
import json
def generateur_oncf_eng(direc): 
        os.remove("dictionaries/dict_oncf_eng.txt") 
        
        mon_fich = open("dictionaries/dict_oncf_eng.txt", "a") 
  
        for fichie in os.listdir(direc):
                
                with open(direc+'/'+fichie, "r",encoding="utf_8") as f:
                        list_dic = json.load(f)
                
                for i in list_dic["rasa_nlu_data"]["common_examples"]:
                        
                        mon_fich.write(i["text"]+"\n")
        
        f2 = open("dictionaries/dict_for_corr_eng.txt", encoding="utf8")

        for word in f2:
                
                mon_fich.write(word)
        
        mon_fich.close()