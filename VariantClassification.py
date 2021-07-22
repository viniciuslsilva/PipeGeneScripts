import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 18

def read_maf(maf_file_name):
    maf_fields = ["Hugo_Symbol", "Chromosome", "Start_Position", "End_Position", "Reference_Allele", "Tumor_Seq_Allele2", "Variant_Classification", "Variant_Type", "Tumor_Sample_Barcode"]
    maf = pd.read_csv(maf_file_name, sep="\t", usecols=maf_fields,comment="#")
    return maf

def runVariantClassification(input_file_name, upload_dir=''):
    #O Input Desse aqui é o arquivo MAF que foi salvo em "PreprocessamentoCompleto.py". 
    # input_file_name = "./inputData/BRCA2_data_mutations_extended.maf"
    name = "BRCA1"

    fig, ax = plt.subplots(1,figsize=(15, 15),dpi=200)
    preproc_maf = read_maf(input_file_name)
    numberOfMutations=len(list(preproc_maf['Hugo_Symbol']))

    #Variant types and their quantities 
    variantsType = set(preproc_maf["Variant_Classification"])    
    cont=0
    variantQuantityDic={}
    for v in variantsType:        
        amount=preproc_maf[preproc_maf["Variant_Classification"]==v].shape[0]
        #Adjust the variant name
        if(v=='Missense_Mutation'):
            v='Missense'
        elif(v=='Splice_Region'):
            v='Splice_R'
        elif(v=='Nonsense_Mutation'):
            v='Nonsense'
        elif(v=='Splice_Site'):
            v='Splice_S'
        elif(v=='Frame_Shift_Del'):
            v='Deletion'
        elif(v=='Frame_Shift_Ins'):
            v='Insertion'
        elif(v=='non-coding-exon'):
            v='NCE'
        elif(v=='Nonstop_Mutation'):
            v='Nonstop'
        elif(v=='Translation_Start_Site'):
            v='Translation'
        elif(v=='In_Frame_Ins'):
            v='InframeI'
        elif(v=='In_Frame_Del'):
            v='InframeD'            
        variantQuantityDic[v]=amount
        cont+=amount

    #===USE THIS IF YOU WANT THE GRAPH SORTED BY NUMBER OF MUTATION    
    #Order the dic, by value, into a list
    #variantQuantity=sorted(variantQuantityDic.items(), key=lambda x: x[1])

    #===USE THIS IF YOU WANT THE GRAPH SORTED BY THE CLASSIFICATION NAME
    variantQuantity=[]
    for elem in sorted(variantQuantityDic.items(), reverse=True):
        variantQuantity.append(elem)
    variantQuantity

    variantsName=[]
    variantsQtty=[]
    variantsQttyOrdered=[]

    for v in variantQuantity:
        variantsName.append(v[0])
        variantsQtty.append(v[1])
        variantsQttyOrdered.append(v[1])


    #variantsQtty=sorted(variantsQtty,reverse=True)
    #variantsName=sorted(variantsName,reverse=True)
    y_pos = np.arange(len(variantsName))
    #y_pos = sorted(y_pos,reverse=True)

    variantsNameSorted=[]
    for indice in y_pos:
        variantsNameSorted.append(variantsName[indice])

    colorList=[]
    #Keep add the colors in the same order that is used in the top10 graph
    for v in variantsNameSorted:
        if(v=='Missense'):
            colorList.append('tab:blue')
        elif(v=='Splice_R'):
            colorList.append('tab:cyan')
        elif(v=='Nonsense'):
            colorList.append('tab:purple')
        elif(v=='Splice_S'):
            colorList.append('tab:gray')
        elif(v=='Deletion'):
            colorList.append('tab:orange')
        elif(v=='Insertion'):
            colorList.append('tab:red')
        elif(v=='NCE'):
            colorList.append('lightcyan')
        elif(v=='Nonstop'):
            colorList.append('salmon')
        elif(v=='Translation'):
            colorList.append('wheat')
        elif(v=='InframeI'):
            colorList.append('fuchsia')
        elif(v=='InframeD'):
            colorList.append('tab:olive')
        elif(v=='IGR'):
            colorList.append('tab:green') 
        elif(v=='Silent'):
            colorList.append('tab:brown')
        elif(v=='Intron'):
            colorList.append('tab:pink')
        elif(v=='3\'Flank'):
            colorList.append('midnightblue')
        elif(v=='5\'Flank'):
            colorList.append('tomato')
        elif(v=='RNA'):
            colorList.append('yellow')
        elif(v=='3\'UTR'):
            colorList.append('goldenrod')
        elif(v=='5\'UTR'):
            colorList.append('indigo')
        elif(v=='coding'):
            colorList.append('violet')

    # Select the actual subplot


    # Create horizontal bars
    ax.barh(y_pos, variantsQtty, height=0.75, color=colorList)
    ax.set_title(name+' - Variant Classification')
    # Create names on the y-axis
    plt.yticks(y_pos, variantsNameSorted)

    #Add the % in the end
    for x, v in enumerate(variantsQttyOrdered):
        ax.text(v, x, str(round(v/numberOfMutations*100))+'%', color='black')

    #Increase the X axis to fit %
    xmin, xmax = plt.xlim()
    plt.xlim(xmin, xmax+xmax*0.05)

    #Set the number of ticks
    plt.locator_params(axis='x', nbins=7)

    #Plot grid
    plt.grid(color='gray', linestyle='--', linewidth=0.5)

    plt.tight_layout(h_pad=2.5, w_pad=1)
        
    # Save the Plot
    filename = upload_dir + name + '_variant_classification.png'
    plt.savefig(filename, format='png', dpi=250,bbox_inches='tight')
    plt.close()

    return filename  