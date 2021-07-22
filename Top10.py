##Esse código precisa de mais testes... talvez compense fazer dnovo, pq tive que tirar a lógica deixar em negrito os genes q aparecem nos 3 estudos

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 18

def read_maf(maf_file_name):
    maf_fields = ["Hugo_Symbol", "Chromosome", "Start_Position", "End_Position", "Reference_Allele", "Tumor_Seq_Allele2", "Variant_Classification", "Variant_Type", "Tumor_Sample_Barcode"]
    maf = pd.read_csv(maf_file_name, sep="\t", usecols=maf_fields,comment="#")
    return maf

input_file_name = "./inputData/BRCA2_data_mutations_extended.maf"
name = "BRCA1"
fig, ax = plt.subplots(1,figsize=(15, 15),dpi=200)
preproc_maf = read_maf(input_file_name)


numberOfMutations=len(list(preproc_maf['Hugo_Symbol']))    

top10GenesNames=[]
variantClassificationType=[]
#The Ideia here is to create a dataframe with the topgenes as rows, and the variant as columns
#Foreach gene
for g in preproc_maf['Hugo_Symbol'].value_counts()[:10].index.tolist():
    top10GenesNames.append(g)
    #foreach variant type of this genes
    for v in preproc_maf[preproc_maf["Hugo_Symbol"]==g]["Variant_Classification"].value_counts().index.tolist():
        variantClassificationType.append(v)

#remove the repeted variation type
variantClassificationType=set(variantClassificationType)
#create a dataframe
topGenesVariations_df = pd.DataFrame(0, index=top10GenesNames, columns=variantClassificationType)

##########

#fill the dataframe
for g in preproc_maf['Hugo_Symbol'].value_counts()[:10].index.tolist():
    #foreach variant type of this genes
    for v in preproc_maf[preproc_maf["Hugo_Symbol"]==g]["Variant_Classification"].value_counts().items():
        topGenesVariations_df[v[0]][g]=v[1]
topGenesVariations_df=topGenesVariations_df.append(topGenesVariations_df.agg(['sum']))
topGenesVariations_df=topGenesVariations_df.sort_values(by ='sum', axis=1,ascending=False)
#https://stackoverflow.com/questions/44309507/stacked-bar-plot-using-matplotlib
bars=[]
for c in topGenesVariations_df.columns:
    bars.append(list(topGenesVariations_df[c][:10]))

npBars=np.array(bars)

numOfLines=10
plotBars=[]
cont=0
ind = [9,8,7,6,5,4,3,2,1,0]
colorList=['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan','midnightblue','yellow','fuchsia']

# Select the actual subplot
for index in range(len(bars)):
    if(index==0):        
        plotBars.append(ax.barh(ind,bars[index],color=colorList[index]))
        sumPrevious=npBars[index]
    else:
        plotBars.append(ax.barh(ind,bars[index],left=sumPrevious,color=colorList[index]))
        sumPrevious+=npBars[index]


plotBarsColor=plotBars
plotVariantType=topGenesVariations_df.columns

#Aumento o eixo x, para caber o %
xmin, xmax = plt.xlim()
plt.xlim(xmin, xmax+xmax*0.03)
#Add the Y Label
plt.yticks(ind, top10GenesNames)
    
plt.title(name+"_top_10_genes_reduced")
fig.legend(plotBarsColor, plotVariantType,loc='upper center', bbox_to_anchor=(0.516, 1.05),ncol=7)
fig.tight_layout(h_pad=1.5, w_pad=1)
plt.savefig(name+"_top_10_genes.png", format='png', dpi=200, bbox_inches='tight')
plt.close() 