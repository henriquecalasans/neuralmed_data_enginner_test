import os 
import pandas as pd 
import mysql.connector

os.system('clear')

#Directory
input = '/Users/henriquenascimento/Documents/work/neuralmed/neuralmed_data_enginner_test/resources/data/exam'

ddl_sql = '/Users/henriquenascimento/Documents/work/neuralmed/neuralmed_data_enginner_test/resources/sql/ddl'

#Database connection
config = {
    'user': 'root',
    'host': '127.0.0.1',
    'database': 'neuralmed',
    'raise_on_warnings': True
    }

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

def create_database():
    
    for file in os.listdir(ddl_sql):

        file = os.fsdecode(file)

        path = ddl_sql + '/' + file

        sql = open(path,'r')
    
        sql_file = sql.read()
        #sql_file = sql_file.decode('utf-8')

        try:
            cursor.execute(sql_file)
            print(file,'table created')
        
        except:
            print(file,'table already exists')
    
    read_files()


#Get file
origin_directory = os.fsdecode(input)

def read_files():

    #Counters
    qtd_origin_file = 0
    qtd_files_read = 0
    
    #Total files in current origin folder
    for path in os.listdir(input):
        if os.path.isfile(os.path.join(input, path)):
            qtd_origin_file += 1

    #Loop Files
    for file in os.listdir(origin_directory):

        file = os.fsdecode(file)
        print('File:', file)

        path = input + '/' + file 
    
        print('Path:',path)
        
        qtd_files_read += 1

        create_dataframe(path)


        #Total files read
        if qtd_files_read == qtd_origin_file:
            print('Files read:',qtd_files_read)
            print('Records loaded:',qtd_files_read)

    cursor.close()
    cnx.close()


#Create dataframe to manipulate data
def create_dataframe(path):
    exam_dataframe = pd.read_json(path)

    #Filter data
    exam_dict = exam_dataframe.to_dict()
    data = exam_dict.get('content')

    #Label data
    label = data[0]
    
    label_data = []
    label_data.append(label['labels'])

   

    label_list = str(label_data).replace('[','').replace(']','').replace('{','').replace('}','')
    label_list = label_list.replace('"','')
    
    res = []
    for sub in label_list.split(', '):
        if ':' in sub:
            res.append(map(str.strip, sub.split(':', 1)))
    

    label_data = dict(res)
    
    #Exam data
    exam_data = data[0]
    exam_data.pop('labels')
    
    
    insert(exam_data,label_data)


#Load into database:
def insert(exam_data,label_data):

    
    exam_table = 'exam'
    label_table = 'label'

    #Exam data columns
    exam_columns = ', '.join(exam_data.keys())
    
    #exam data content
    exam_content = str(list(exam_data.values())).replace('[','').replace(']','')
    exam_content = (''.join(exam_content))
    
    #Insert SQL, exam data
    exam_sql = "INSERT INTO {}   ({}) VALUES({})".format(exam_table, exam_columns, exam_content)


    #Label data columns
    exam_id = ''.join("'exam_id',")
    label_columns = exam_id + ' ' +  ', '.join(label_data.keys())
    label_columns = label_columns.replace("'","")
    print(label_columns)


    #Label data content
    exam_id = exam_data['id']
    exam_id = "'" + str(exam_id) + "', "
    
    label_content = str(list(label_data.values())).replace('[','').replace(']','').replace('"','')

    if 'True' in label_content:
        label_content = label_content.replace('True', '1')
    
    if 'False' in label_content:
        label_content =  label_content.replace('False', '0')

    
    label_content = exam_id + (''.join(label_content))
    print(label_content)
    
    label_sql = "INSERT INTO {}   ({}) VALUES({})".format(label_table, label_columns, label_content)

    #Load exam table
    cursor.execute(exam_sql)
    cnx.commit()

    #Load label table 
    cursor.execute(label_sql)
    cnx.commit()



def main():
    create_database()

main()