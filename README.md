Até o momento o projeto conta com 3 apps em python com FLASK que expões interfaces REST
e internamente realizam chamadas para algoritmos do grupo do professor Rodrigo.

Os serviços são: 
- app_grafico_pre_processamento
- app_pre_processamento_output_maf.py 
- app_classificacao_variant.py

O código não se encontra production-ready e é uma sequencia de adaptações a fim de validar o MVP
da platforma pipegine.


É possivel executar local utilizando python 3.6, outras versões podem surgir conflitos de libs, todas as
depencias identificadas estão no arquivo requirements.txt. 

Para execução local com o python da própria maquina, recomendo o uso do https://docs.python.org/3/tutorial/venv.html.


Uma maneira mais simples é utilizando containers docker, na raiz do projeto se encontra um docker-compose que sobe os 3 serviços basta executar o comando abaixo, lembrando que as flagas --build e --remove-orphans são para forçar o build do container e remover containers orphans:

```
docker-compose up --build --remove-orphans
```

A flag -d também pode ser passada para que os containers rodem em background e o terminal seja liberado.

Para para os containers execute:

```
docker-compose down
```

Ou:

```
docker-compose stop
```


Para o cenário no qual é utilizado os serviços app_pre_processamento_output_maf.py e app_classificacao_variant.py é necessário passar quais as colunas serão utilizadas pelo app_pre_processamento_output_maf.py, o valor que antes estava hardcode nos scripts (antes de virar uma API) e pode ser usado é:
```
Hugo_Symbol,Chromosome,Start_Position,End_Position,Reference_Allele,Tumor_Seq_Allele2,Variant_Classification,Variant_Type,Tumor_Sample_Barcode
```
