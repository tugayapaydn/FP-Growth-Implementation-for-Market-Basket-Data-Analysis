import time
import FPGrowth
import pyfpgrowth
import pyECLAT
from argparse import ArgumentParser
#from apyori import apriori
from apriori_python import apriori

import matplotlib.pyplot as plt
import pandas as pd

def EclatTest(dataset, min_supp):
    inst = pyECLAT.ECLAT(dataset)
    return inst.fit_all(min_support=min_supp, verbose=False)

def AprioriTest(dataset, min_supp, conf, prt=False):
    #rules = list(apriori(dataset, min_support=min_supp, min_confidence=conf))
    freqItemSet, rules = apriori(dataset, minSup=min_supp, minConf=conf)

    if (prt == True):
        for item in rules:
            # first index of the inner list
            # Contains base item and add item
            pair = item[0] 
            items = [x for x in pair]
            print("Rule: " + str(items))

            #second index of the inner list
            print("Support: " + str(item[1]))

            #third index of the list located at 0th
            #of the third index of the inner list

            print("Confidence: " + str(item[2][0][2]))
            print("Lift: " + str(item[2][0][3]))
            print("=====================================")
    
    return rules

def PyFPGrowthTest(dataset, min_supp, conf):
    freq = pyfpgrowth.find_frequent_patterns(dataset, min_supp)
    #rules = pyfpgrowth.generate_association_rules(freq, conf)
    return freq

def FPGrowthTest(dataset, labelfile, min_supp, prt=False):
    freqIt = FPGrowth.fpgrowth(dataset, min_supp)
    
    if (prt == True):
        if (labelfile != None):
            labels = FPGrowth.read_labels(labelfile)
            for key, value in freqIt.items() :
                klist = ""
                for k in key:
                    if (len(klist) > 0):
                        klist += ","  
                    klist += labels[k]
                
                print(klist + ": " + str(value))
        else:
            for key, value in freqIt.items() :
                print(str(key) + ": " + str(value))
    return freqIt

def TestWithDifferentTransactionFiles():
    filelist = [ "/home/tugayapaydn/Desktop/Project/uchoice-Instacart/testf_1",
                 "/home/tugayapaydn/Desktop/Project/uchoice-Instacart/testf_2",
                 "/home/tugayapaydn/Desktop/Project/uchoice-Instacart/testf_3",
                 "/home/tugayapaydn/Desktop/Project/uchoice-Instacart/testf_4",
                 "/home/tugayapaydn/Desktop/Project/uchoice-Instacart/testf_5"]
    
    exList = [[], [], []]
    translen = []
    rules = [[], []]
    for i in range(len(filelist)-1, 0, -1):
        dataset = FPGrowth.load_data(filelist[i])
        dataframe = pd.DataFrame(dataset)

        start_time = time.time()
        rulesFP = PyFPGrowthTest(dataset, 0.1, 0)
        rules[0].append(len(rulesFP))
        exList[0].append((time.time() - start_time))
        print("done1")

        start_time = time.time()
        rulesAp = AprioriTest(dataset, min_supp=0.1, conf=0, prt=False)
        rules[1].append(len(rulesAp))
        exList[1].append((time.time() - start_time))
        print("done2")

        #start_time = time.time()
        #EclatTest(dataframe, min_supp=0)
        #exList[2].append((time.time() - start_time))
        #print("done1")
                
        translen.append(len(dataset))
        print(exList)
        print(rules)
        print()
    
    plt.plot(translen, exList[0], label="PyFP-Growth")
    plt.plot(translen, exList[1], label="Apriori")
    #plt.plot(translen, exList[2], label="ECLAT")

    plt.legend()
    plt.ylabel('Execution Time')
    plt.xlabel('Transaction Size')
    plt.title('Execution Time / Transaction Size Analysis')
    plt.show()

    plt.clf()
    plt.plot(translen, rules[0], label="PyFP-Growth")
    plt.plot(translen, rules[1], label="Apriori")
    #plt.plot(translen, exList[2], label="ECLAT")

    plt.legend()
    plt.ylabel('# of Rules')
    plt.xlabel('Transaction Size')
    plt.title('Execution Time / Transaction Size Analysis')
    plt.show()

def TestWithDifferentSupportCounts():
    file = "/home/tugayapaydn/Desktop/Project/uchoice-Instacart/uiLess.txt"
    
    dataset = FPGrowth.load_data(file)
    dataframe = pd.DataFrame(dataset)

    exList = [[], [], [], []]
    rules = [[], [], [], []]
    supp_count = []

    i = 7
    j = 2
    k = -1
    while (i >= j):
        start_time = time.time()
        rulesFP = PyFPGrowthTest(dataset, min_supp=i, conf=0)
        rules[0].append(len(rulesFP))
        exList[0].append((time.time() - start_time))
        print("done1")

        start_time = time.time()
        rulesAp = AprioriTest(dataset, min_supp=i, conf=0)
        rules[1].append(len(rulesAp))
        exList[1].append((time.time() - start_time))
        print("done2")

        #start_time = time.time()
        #EclatTest(dataframe, min_supp=i)
        #exList[2].append((time.time() - start_time))
        #print("done1")

        #start_time = time.time()
        #rulesmyfp = FPGrowthTest(dataset, labelfile=None, min_supp=i)
        #exList[3].append((time.time() - start_time))
        #rules[3].append(len(rulesmyfp))
        #print("done2")

        supp_count.append(i)
        print(supp_count)
        print(exList)
        print(rules)
        i = i + k
    
    plt.plot(supp_count, exList[0], label="PyFP-Growth")
    plt.plot(supp_count, exList[1], label="Apriori")
    #plt.plot(supp_count, exList[2], label="ECLAT")
    #plt.plot(supp_count, exList[3], label="myFP-Growth")

    plt.legend()
    plt.xlabel('Support Count')
    plt.ylabel('Execution Time')
    plt.title('Execution Time / Support Count')
    plt.show()

    plt.clf()
    plt.plot(supp_count, rules[0], label="PyFP-Growth")
    plt.plot(supp_count, rules[1], label="Apriori")
    #plt.plot(translen, rules[2], label="ECLAT")
    #plt.plot(supp_count, rules[3], label="myFP-Growth")

    plt.legend()
    plt.xlabel('Support Count')
    plt.ylabel('# of Rules')
    plt.title('# of Rules / Support Count')
    plt.show()


if __name__ == "__main__":
    #TestWithDifferentTransactionFiles()
    TestWithDifferentSupportCounts()

    """
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename")
    parser.add_argument("-s", "--support", dest="supp", default=0.0005, type=float)
    parser.add_argument("-lf", "--labelfile", dest="labelfile", default=None)
    
    args = parser.parse_args()
    dataset = FPGrowth.load_data(args.filename)
    #print(dataset)
    #FPGrowthTest(dataset, args.labelfile, args.supp, True)
    """