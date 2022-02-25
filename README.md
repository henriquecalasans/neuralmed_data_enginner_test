# Neuralmed - Realização do desafio para engenharia de dados.
A arquitetura dessa aplicação é bem simples, ela possui dois scripts escritos em Python:
load_exam_files.py e load_medical_report_files que são responsáveis por lerem arquivos .json de um diretório especifico e carregar os respectivos dados em um banco de dados.

# - Banco de dados
Para armezenar os dados coletados foi utilizado para uma imagem docker, banco de dados Mysql latest version.

# - SQL
O diretório sql possui os respectivos ddls utilizados para a criação das tabelas solicitadas, antes da aplicação ser executado o database chamado neuralmed deve ser criado.

# - Evidências
No diretório evidencies pode ser encontrado evidências de carregamentos e registros de dados presentes no Mysql.