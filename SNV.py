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
    
#There are many types of alleles in MAF (print(reference_Alleles)). Most of them are unique.
reference_Alleles=set(preproc_maf['Reference_Allele'])
#print('Total Ref: '+str(len(reference_Alleles)))
#Get only the 1 lenght/size allele
aux_df = preproc_maf[[ x in ('A', 'C', 'G', 'T') for x in preproc_maf['Reference_Allele']]]
reference_Alleles_Lenght1=set(aux_df['Reference_Allele'])

#The same thing with the Tumor Seq Allele
tumor_Seq_Allele2=set(preproc_maf['Tumor_Seq_Allele2'])
#print('Total Ref: '+str(len(tumor_Seq_Allele2)))
#Get only the 1 lenght/size allele
aux_df = preproc_maf[[ x in ('A', 'C', 'G', 'T') for x in preproc_maf['Tumor_Seq_Allele2']]]
tumor_Seq_Allele2_Lenght1=set(aux_df['Tumor_Seq_Allele2'])

reference_Alleles_Lenght1=sorted(reference_Alleles_Lenght1)
tumor_Seq_Allele2_Lenght1=sorted(tumor_Seq_Allele2_Lenght1)

#Combine the two lists
snvClass={}
for r in reference_Alleles_Lenght1:
    for t in tumor_Seq_Allele2_Lenght1:
        if(r != t):
            key=str(r)+'>'+str(t)
            snvClass[key]=len(preproc_maf.loc[(preproc_maf['Reference_Allele']==r) & (preproc_maf['Tumor_Seq_Allele2']==t)])

#Plot only the C>* e T>*
snvToPlot={}
for r in ['C','T']:
    for t in ['A', 'C', 'G', 'T']:
        if(r != t):
            key=str(r)+'>'+str(t)
            snvToPlot[key]=snvClass[key]
#sum the "mirror" SNV
snvToPlot['C>A']+=snvClass['G>T']
snvToPlot['C>G']+=snvClass['G>C']
snvToPlot['C>T']+=snvClass['G>A']
snvToPlot['T>A']+=snvClass['A>T']
snvToPlot['T>C']+=snvClass['A>G']
snvToPlot['T>G']+=snvClass['A>C']

#print(snvClass)
y_pos=np.arange(len(snvToPlot))
snvValues=list(snvToPlot.values())
snvKeys=list(snvToPlot.keys())
snvKeys.reverse()
snvValues.reverse()

# Create horizontal bars
ax.barh(y_pos, snvValues, height=0.75)

# Create names on the y-axis
plt.yticks(y_pos, snvKeys)

#Add the number at the end
for x, v in enumerate(snvValues):
    ax.text(v, x, v, color='black')

#Increase the X axis to fit %
xmin, xmax = plt.xlim()
plt.xlim(xmin, xmax+xmax*0.135)

#Plot grid
plt.grid(color='gray', linestyle='--', linewidth=0.5)

plt.title(name+"_SNV")
plt.tight_layout(h_pad=1.5, w_pad=1)   
# Save the plot
plt.savefig(name+"_SNV.png", format='png', dpi=250,bbox_inches='tight')
plt.close()