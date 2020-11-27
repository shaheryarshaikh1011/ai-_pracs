import math
class DataSet:
    def __init__(self ,ds):
        self.dataset=ds

    def print(self):
        print(self.dataset)

    def uniqueAns(self):
        ans_set=set(self.dataset["Ans"])
        return len(ans_set)

    def getMaxOccur(self):
        d={self.dataset["Ans"].count(x):x for x in self.dataset["Ans"]}
        keys=list(d.keys())
        keys.sort(reverse=True)
        if len(keys) >1 and keys[0]!=keys [1]:
            return d[keys[0]]
        else:
            return None

    def copy(self):
        newdataset = dict()
        keys = list(self.dataset.keys())
        newdataset = dict.fromkeys(keys,0)
        for key in keys:
            newdataset[key] = self.dataset[key].copy()
        return DataSet(newdataset)

    def maxInfoGain(self): 
        features = self.dataset["Features"]
        if len(features) >=0:
            maxinfogain=self.infoGain(features[0])
            maxfeat=features[0]
            i=0
            while i<len(features):
                ig = self.infoGain(features[0])
                if ig>= maxinfogain:
                    maxinfogain = ig
                    maxfeat=features[i]
                i=i+1    
            return maxfeat
        else:
            return None
        
    def infoGain(self, feat): 
        if feat in self.dataset.keys():
            featlist1 = self.dataset[feat]
            total=len(featlist1)
            featset=set(featlist1)
            d=dict.fromkeys(featset, 0)
            for item in featlist1:
                d[item]=d[item]+1
                branches=self.splitOnFeature(feat)
                gain=0
            for key in branches:
                dsobj = branches[key]
                gain = gain+((d[key]/total)*(dsobj.getEntropy()))
            return self.getEntropy()-gain
        else:
            print("feature does not exists")
            return None
        
    def getEntropy(self) :
        list1=self.dataset["Ans"]
        total=len(list1)
        aset=set(list1)
        d=dict.fromkeys(aset,0)
        for item in list1:
            d[item]=d[item]+1
        ent=0
        for k in aset:
            x=d[k]/total
            ent=ent+(x*math.log(x,2))
        return ent

    def splitOnFeature(self, feat):
        if feat in self.dataset["Features"]:
            ans_set=set(self.dataset[feat])
            newfeatures=self.dataset["Features"].copy()
            newfeatures.remove(feat)
            keys=list(self.dataset.keys())
            newdataset=dict()
            for akey in keys:
                newdataset[akey]=list()
            newdataset["Features"]=newfeatures.copy()
            newdataset.pop(feat)
            branches=dict()
            for akey in ans_set:
                branches[akey]=dict()
                for key in list(newdataset.keys()):
                    branches[akey][key]=newdataset[key].copy()
            i=-1
            for featval in self.dataset[feat]:
                i=i+1
                if featval in list(branches.keys()):
                    branches[featval]["Ans"].append(self.dataset["Ans"][i])
                    for nfeat in newfeatures:
                        branches[featval][nfeat].append(self.dataset[nfeat][i])
            for key in branches:
                branches[key]=DataSet(branches[key])
            return branches
        else:
            print(feat,"feature is not available")
            return None
def calculateAns(dsobj,feature,maxoccur,descr):
    branches=dsobj.splitOnFeature(feature)
    for key in list(branches.keys()):
        newdsobj=branches[key]
    for key in list(branches.keys()):
        newdsobj=branches[key]
        if(newdsobj.uniqueAns()==1):
            print ("Answer for ",descr+" - "+feature," with values =",key," is : ",newdsobj.dataset["Ans"][0])
        elif(newdsobj.uniqueAns()==0):
            print("Answer for ",descr+" - "+feature," with values =",key," is ", maxoccur)
        elif(newdsobj.uniqueAns()>1 and len(newdsobj.dataset["Features"])==0):
            print("Answer for ",descr+" - "+feature," with values =",key," is ", maxoccur)
        else:
            newfeat= newdsobj.maxInfoGain()
            newmaxoccur=newdsobj.getMaxOccur()
            if(newmaxoccur==None):
                newmaxoccur=maxoccur
            calculateAns(newdsobj, newfeat, newmaxoccur, descr+":"+feature+":->"+key+"")


dataset={
"Ans":["Wait", "Wait", "Leave", "Wait", "Wait", "Wait", "Leave", "Leave", "Wait", "Leave"],
"Features":["Reservation", "Raining", "BadService"],
"Reservation":["T", "T", "T", "F", "T", "T", "T", "T", "T", "F"],
"Raining": ["T", "F", "T", "T", "T","T", "E", "T", "T", "F"],
"BadService":["F", "F", "T", "F", "F","F", "T", "T", "F", "F"]
}
d1=DataSet(dataset)
if d1.uniqueAns()!=1:
    feat=d1.maxInfoGain()
    calculateAns(d1, feat, d1.getMaxOccur(),"")
