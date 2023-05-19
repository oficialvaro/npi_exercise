import sys
import sqlite3
import requests
import json
import pandas as pd

# Create NPI Database and it's connection
connection = sqlite3.connect('npi.db')
cursor = connection.cursor()

# Create records table
with open("tb_records_create.sql", "r") as sqlfile:
    tb_records_create = sqlfile.read()
cursor.execute(tb_records_create)
connection.commit()

# Write records on the Records table
def write_record(RECORD):
    with open("tb_records_insert.sql", "r") as sqlfile:
        tb_records_insert = sqlfile.read()
    cursor.execute(tb_records_insert,RECORD)
    connection.commit()


# Get NPI's information from API
def get_npi(NPI_NUMBER_RAW,IDX_NUM,LIST_LEN):
    try:
        NPI_NUMBER = int(NPI_NUMBER_RAW)
    except:
        print('NPI format is invalid.')
        return None

    if LIST_LEN > 1:
        print('\r'+str(IDX_NUM+1)+'/'+str(LIST_LEN)+' '+str(NPI_NUMBER)+' | .',end='')

    responses = []
    base_url = "https://npiregistry.cms.hhs.gov/api/"
    params = {
        "version": "2.1",
        "number": NPI_NUMBER
    }
    try:
        try:
            response = requests.get(f"{base_url}", params=params)
        except:
            print(str(NPI_NUMBER)+' is invalid.')
            return None

        if LIST_LEN > 1:
            print('\r'+str(IDX_NUM+1)+'/'+str(LIST_LEN)+' '+str(NPI_NUMBER)+' | ..',end='')

        response.raise_for_status()
        data = response.json()

        # Extract the relevant information from the response
        if data['result_count'] > 0 and "results" in data:
            result = data['results'][0]

            with open("raw/"+str(result['number'])+".json", "w") as outfile:
                json.dump(result, outfile)
            
            addresses = result['addresses']
            basic = result['basic']
            taxonomies = result['taxonomies']
            npi_number = result['number']
            created_epoch = result['created_epoch']
            enumeration_type = result['enumeration_type']
            last_updated_epoch = result['last_updated_epoch']
            
            organization_name = basic.get('organization_name',None)
            organizational_subpart = basic.get('organizational_subpart',None)
            parent_organization_legal_business_name = basic.get('parent_organization_legal_business_name',None)
            enumeration_date = basic.get('enumeration_date',None)
            last_updated = basic.get('last_updated',None)
            organization_status = basic.get('status',None)
            auth_official_first_nam = basic.get('authorized_official_first_nam',None)
            auth_official_last_name = basic.get('authorized_official_last_name',None)
            auth_official_telephone_number = basic.get('authorized_official_telephone_number',None)
            auth_official_title_or_position = basic.get('authorized_official_title_or_position',None)
            auth_official_name_prefix = basic.get('authorized_official_name_prefix',None)
            auth_official_credential = basic.get('authorized_official_credential',None)

            for addr in addresses:
                if addr['address_purpose'] == 'LOCATION':
                    addr_practice_country_code = addr.get('country_code',None)
                    addr_practice_country_name = addr.get('country_name',None)
                    addr_practice_address_type = addr.get('address_type',None)
                    addr_practice_1 = addr.get('address_1',None)
                    addr_practice_2 = addr.get('address_2',None)
                    addr_practice_city = addr.get('city',None)
                    addr_practice_state = addr.get('state',None)
                    addr_practice_postal_code = addr.get('postal_code',None)
                    addr_practice_telephone_number = addr.get('telephone_number',None)
                    addr_practice_fax_number = addr.get('fax_number',None)

                if addr['address_purpose'] == 'MAILING':
                    addr_mail_country_code = addr.get('country_code',None)
                    addr_mail_country_name = addr.get('country_name',None)
                    addr_mail_address_type = addr.get('address_type',None)
                    addr_mail_1 = addr.get('address_1',None)
                    addr_mail_2 = addr.get('address_2',None)
                    addr_mail_city = addr.get('city',None)
                    addr_mail_state = addr.get('state',None)
                    addr_mail_postal_code = addr.get('postal_code',None)
                    addr_mail_telephone_number = addr.get('telephone_number',None)
                    addr_mail_fax_number = addr.get('fax_number',None)

            for taxonomy in taxonomies:
                if taxonomy['primary'] == True:
                    primary_taxonomy_code = taxonomy.get('code',None)
                    primary_taxonomy_taxonomy_group = taxonomy.get('taxonomy_group',None)
                    primary_taxonomy_desc = taxonomy.get('desc',None)
                    primary_taxonomy_state = taxonomy.get('state',None)
                    primary_taxonomy_license = taxonomy.get('license',None)

            if LIST_LEN > 1:
                print('\r'+str(IDX_NUM+1)+'/'+str(LIST_LEN)+' '+str(NPI_NUMBER)+' | ...',end='')

            # Return the extracted information
            responses = (
                npi_number,
                created_epoch, 
                enumeration_type, 
                last_updated_epoch, 
                organization_name, 
                organizational_subpart, 
                parent_organization_legal_business_name, 
                enumeration_date, 
                last_updated, 
                organization_status, 
                auth_official_first_nam, 
                auth_official_last_name, 
                auth_official_telephone_number, 
                auth_official_title_or_position, 
                auth_official_name_prefix, 
                auth_official_credential, 
                addr_practice_country_code, 
                addr_practice_country_name, 
                addr_practice_address_type, 
                addr_practice_1, 
                addr_practice_2, 
                addr_practice_city, 
                addr_practice_state, 
                addr_practice_postal_code, 
                addr_practice_telephone_number, 
                addr_mail_country_code, 
                addr_mail_country_name, 
                addr_mail_address_type, 
                addr_mail_1, 
                addr_mail_2, 
                addr_mail_city, 
                addr_mail_state, 
                addr_mail_postal_code, 
                addr_mail_telephone_number, 
                primary_taxonomy_code, 
                primary_taxonomy_taxonomy_group, 
                primary_taxonomy_desc, 
                primary_taxonomy_state, 
                primary_taxonomy_license, 
            )

        else:
            if LIST_LEN > 1:
                print('\r'+str(IDX_NUM+1)+'/'+str(LIST_LEN)+' '+str(NPI_NUMBER)+' | Error\n',end='')
            else:
                print('\rNPI number: '+str(item)+' | Error\n',end='')
            return None
        if LIST_LEN > 1:
            print('\r'+str(IDX_NUM+1)+'/'+str(LIST_LEN)+' '+str(NPI_NUMBER)+' | Success\n',end='')
        else:
            print('\rNPI number: '+str(NPI_NUMBER)+' | Success\n',end='')
        return responses

    except requests.exceptions.RequestException as e:
        print('Unnable to request :', e)
        return None

print('Welcome to NPI Importer v1.0.')
print(' ')
print('Please select the option that best suits your import needs:')
print('#A | Manually input NPI number')
print('#B | Import numbers from CSV')
print('#C | Import numbers from Excel')
print('#D | Import numbers from jSon')

while True:
    import_mode = input().upper()
    if import_mode in ['A','B','C','D']:
        break
    else:
        print('Please enter a valid option to continue.')
        continue


# Importing from manual input
if import_mode == 'A':
    print('\nEnter a NPI number, one at a time.')
    print('Type "STOP" to stop the process anytime.')
    print('#------------------------------#')
    while True:
        npi_to_import = input('NPI number: ')
        if npi_to_import.upper() in ['STOP','EXIT']:
            connection.close()
            break
        response = get_npi(npi_to_import,1,1)
        if response != None:
            write_record(response)
        continue


# Importing from file
else:
    to_import_format = {
        'B': [pd.read_csv('to_import.csv'),'CSV'],
        'C': [pd.read_excel('to_import.xlsx'),'Excel'],
        'D': [pd.read_json('to_import.json'),'jSon']
    }
    list_to_import = list(to_import_format[import_mode][0]['numbers'])
    print('\nImporting '+str(len(list_to_import))+' NPI Numbers from '+to_import_format[import_mode][1]+' file')
    print('#------------------------------#')
    for idx,item in enumerate(list_to_import):
        print(str(idx+1)+'/'+str(len(list_to_import))+' '+str(item)+' |',end='')
        response = get_npi(item,idx,len(list_to_import))
        if response != None:
            write_record(response)
    connection.close()    
    print('Done!')
    print('\n')

