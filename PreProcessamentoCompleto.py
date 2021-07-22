import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json


plt.rcParams['font.size'] = 18

def preprocess(maf_file_name, maf_fields, output_file_name):
    maf = read_maf(maf_file_name, maf_fields)
    mutations_per_patient = get_mutations_per_patient(maf)
    
    maf = remove_hipermutated_patients(maf, mutations_per_patient)
    mutations_per_patient = get_mutations_per_patient(maf)
    write_maf(maf, output_file_name)
    

def read_maf(maf_file_name, maf_fields):
    # maf_fields = ["Hugo_Symbol", "Chromosome", "Start_Position", "End_Position", "Reference_Allele", "Tumor_Seq_Allele2", "Variant_Classification", "Variant_Type", "Tumor_Sample_Barcode"]
    print("aqui: {}".format(maf_fields))
    maf = pd.read_csv(maf_file_name, sep="\t", usecols=maf_fields,comment="#")
    return maf

def write_maf(maf, output_file_name):
    maf.to_csv(output_file_name, sep='\t')
    
def get_mutations_per_patient(maf):
    mutations_per_patient = {}
    patients = set(maf["Tumor_Sample_Barcode"])
    for patient in patients:
        maf_one_gene = maf[maf.Tumor_Sample_Barcode.isin([patient])]
        mutations_per_patient[patient] = len(maf_one_gene)
    return mutations_per_patient


def remove_hipermutated_patients(maf, mutations_per_patient):
    mutations_per_patient_count = list(mutations_per_patient.values())
    q1 = np.quantile(mutations_per_patient_count, .25)
    q2 = np.quantile(mutations_per_patient_count, .50)
    q3 = np.quantile(mutations_per_patient_count, .75)
    iqr = q3 - q1
    threshold_hm = q3 + 4.5*iqr
    mutations_per_patient_filtered = dict(filter(lambda elem: elem[1] <= threshold_hm, mutations_per_patient.items()))
    maf = maf[maf.Tumor_Sample_Barcode.isin(list(mutations_per_patient_filtered))]
    return maf
    
def get_indicators_from_maf(maf):
    mutations = maf["Hugo_Symbol"]
    genes = set(maf["Hugo_Symbol"])
    patients = set(maf["Tumor_Sample_Barcode"])
    mutations_count = len(mutations)
    genes_count = len(genes)
    patients_count = len(patients)
    return mutations_count, genes_count, patients_count

#MAIN

def runPreProcessamento(maf_file_name, maf_fields, output_file_name, upload_dir=''):
    ####INPUT
    # maf_file_name = "./inputData/BRCA2_data_mutations_extended.txt"
    # output_file_name = "./inputData/BRCA2_data_mutations_extended.maf"
    name='BRCA'

    #---Pega o arquivo grande, remove colunas e hypermutados
    preprocess(maf_file_name, maf_fields, output_file_name)

    #---Indicadores

    #Apresenta textualmente a diferença entre a original e preprocessado
    
    # print("antes de original maf\n {} \n {}".format(maf_file_name, maf_fields))
    
    original_maf = read_maf(maf_file_name, maf_fields)
    preproc_maf = read_maf(output_file_name, maf_fields)

    mutations_count, genes_count, patients_count = get_indicators_from_maf(original_maf)
    indicator={}
    indicator['Original '+name]={
        "Mutations":mutations_count,
        "Mutated Genes":genes_count,
        "Mutated patients":patients_count,
    }
    mutations_count, genes_count, patients_count = get_indicators_from_maf(preproc_maf)
    indicator['Preprocessed '+name]={
        "Mutations":mutations_count,
        "Mutated Genes":genes_count,
        "Mutated patients":patients_count,
    }


    #---Plot Indicadores

    data = []

    mutations_per_patient = get_mutations_per_patient(original_maf)
    data.append(mutations_per_patient)
    mutations_per_patient = get_mutations_per_patient(preproc_maf)
    data.append(mutations_per_patient)

    num_cancer = 1
    num_graphs = num_cancer * 2

    fig, a =  plt.subplots(num_cancer, num_graphs, figsize=(12, 6),dpi=200)
    x = 0

    for i in range(num_graphs):
        mutations_per_patient = data[x]
        x = x + 1
        mutations_per_patient_count = list(mutations_per_patient.values())
        mutations_per_patient_count = sorted(mutations_per_patient_count, reverse=True)
        x_axis = list(range(0, len(mutations_per_patient_count)))
        a[i].bar(x_axis, mutations_per_patient_count, width=1.0, facecolor='dimgray', edgecolor='dimgray')
        a[i].set_xticks([])
                    
    for i in range(num_graphs):
        a[i].set_xlabel("patients")  

    a[0].set_ylabel(name)

    a[0].set_title("Original")
    a[1].set_title("Preprocessed")


    ####OUTPUTS


    #Indicadores como json
    print(json.dumps(indicator))

    # Salva o plot em arquivo.
    plt.title("Hypermutation Removal")
    fig.tight_layout(h_pad=1.5, w_pad=1)
    filename = upload_dir + name+'_withAndWithoutHypermutated.png'
    plt.savefig(filename, format='png', dpi=500)
    #plt.show()
    plt.close()

    return filename