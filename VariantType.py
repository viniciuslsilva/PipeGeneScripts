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
#Variant types and their quantities 
variantsType = set(preproc_maf["Variant_Type"])    
cont=0
variantQuantity={}
for v in variantsType:        
    amount=preproc_maf[preproc_maf["Variant_Type"]==v].shape[0]
    variantQuantity[v]=amount
    cont+=amount
#Visual Verification
#print("This numbers must match "+str(numberOfMutations)+" = "+str(cont))

#Order the dic into a list
variantQuantity=sorted(variantQuantity.items(), key=lambda x: x[1])
#print(variantQuantity)

variantsName=[]
variantsQtty=[]
variantsQttyOrdered=[]

for v in variantQuantity:
    variantsName.append(v[0])
    variantsQtty.append(v[1])
    variantsQttyOrdered.append(v[1])


variantsQtty=sorted(variantsQtty,reverse=True)
#variantsName=sorted(variantsName,reverse=True)
y_pos = np.arange(len(variantsName))
y_pos = sorted(y_pos,reverse=True)

variantsNameSorted=[]
for indice in y_pos:
    variantsNameSorted.append(variantsName[indice])



# Create horizontal bars
ax.barh(y_pos, variantsQtty, color=['lightsalmon','lightblue','lightgreen','pink','red','tan'])
# Create names on the y-axis
plt.yticks(y_pos, variantsNameSorted)

#Adiciono os textos de % no final
for x, v in enumerate(variantsQttyOrdered):
    ax.text(v, x, str(round(v/numberOfMutations*100))+'%', color='black')

#Aumento o eixo x, para caber o %
xmin, xmax = plt.xlim()
plt.xlim(xmin, xmax+xmax*0.05)

#Plot grid
plt.grid(color='gray', linestyle='--', linewidth=0.5)

plt.title(name+'_variantType')
plt.tight_layout(h_pad=2.5, w_pad=1)
plt.savefig(name+'_variantType.png', format='png', dpi=250,bbox_inches='tight')
plt.close()