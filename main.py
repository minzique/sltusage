import sltusage
import os
import json

if __name__ == '__main__':
    #Credentials for SLT portal
    username = os.environ['UNAME']
    password = os.environ['PASS']

    slt = sltusage.SLT(username, password)
    usage = slt.get_usage()
    if not usage['isSuccess']:
        print('Error occurred')
        quit()    
    
    for x in usage['dataBundle']['usageDetails']:
        print(f'{x["name"]}:')
        if x['limit']: 
            print(f'\tLimit: {x["limit"]}')
        if x['remaining']:
            print(f'\tRemaining: {x["remaining"]}')
        print(f'\tUsed: {x["used"]}\n')