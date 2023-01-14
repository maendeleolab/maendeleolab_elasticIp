#!/usr/bin/python3

Goal = '''
to create elastic ip in aws
Author: Pat@Maendeleolab
'''
#Module imports
import logging, sys, os, json
from datetime import datetime
from time import sleep

#Path to local home and user folder
FPATH = os.environ.get('ENV_FPATH')

#logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p ',\
        filename=FPATH+'/maendeleolab_elasticIp/elastic_ip.log', level=logging.INFO)

#adding flexibility for regions
def region_id(name='us-east-1'):
    return name # e.g: 'us-east-1'

def verify_eip(eip_name, region='us-east-1'):
    ''' Verifies if Elastic IP name already exists '''
    try:
        output = os.popen('aws ec2 describe-addresses --filters Name=tag:Name,Values=' + eip_name + ' --region '+ region).read()
        eip_data = json.loads(str(output))
        if len(eip_data['Addresses']) > 0:
            print(f'{eip_name} already exists in {region}...')
            return 1
    except Exception as err:
        logging.info('Logging "verify_eip" error to elastic_ip.log...')
        print('Logging "verify_eip" error to elastic_ip.log...')

def make_elastic_ip(**kwargs):
    try:
        if verify_eip(kwargs['Elastic_Ip'],kwargs['Region']) == 1:
            pass
        else:
            os.system("aws ec2 allocate-address \
                    --tag-specifications 'ResourceType=elastic-ip,Tags=[{Key=Name,Value=" + kwargs['Elastic_Ip'] + "},\
                                              {Key=" + kwargs['Tag_key'] + ",Value=" + kwargs['Tag_value'] + "}]'\
                    --region " + kwargs['Region'] 
            )
            logging.info(f'Created Elastic IP: {kwargs["Elastic_Ip"]} in {kwargs["Region"]}...')
            print(f'Created Elastic IP:{kwargs["Elastic_Ip"]} in {kwargs["Region"]}...')
    except Exception as err:
        logging.info(f'Logging "make_elastic_ip" error: {err}...')
        print('Logging "make_elastic_ip" error in elastic_ip.log...')

def get_EipId(Eip_name, region='us-east-1'):
    ''' Gets resource id from json output and can be used in deploy scripts '''
    try:
        output = os.popen('aws ec2 describe-addresses --filters Name=tag:Name,Values=' + Eip_name + ' --region '+ region).read()
        eip_data = json.loads(str(output))
        data = eip_data['Addresses']
        for info in data:
                return info['PublicIp']
    except Exception as err:
        logging.info(f'Logging "get_EipId" error to elastic_ip.log error: {err}...')
        print('Logging "get_EipId" error to elastic_ip.log...')

def get_AllocationId(Eip_name, region='us-east-1'):
    ''' Gets resource id from json output and can be used in deploy scripts '''
    try:
        output = os.popen('aws ec2 describe-addresses --filters Name=tag:Name,Values=' + Eip_name + ' --region '+ region).read()
        eip_data = json.loads(str(output))
        data = eip_data['Addresses']
        for info in data:
            return info['AllocationId']
    except Exception as err:
        logging.info('Logging "get_AllocationId" error: {err}...')
        print('Logging "get_AllocationId" error to elastic_ip.log...')

#create association
def make_association(**kwargs):
    try:
        os.system("aws ec2 associate-elastic-ip \
                --instance-id " + kwargs['Instance_Id'] + "},\
                --elastic-ip " + kwargs['Elastic_Ip'] + "},\
                --region " + kwargs['Region'] 
        )
        logging.info('Associated Elastic_IP: ' + kwargs['Elastic_Ip'] + 'with Instance_ID: ' + kwargs['Instance_Id'])
        print(f'Associated Elastic_IP: {kwargs["Elastic_Ip"]} with Instance_ID: {kwargs["Instance_Id"]} in {kwargs["Region"]}...')
    except Exception as err:
        logging.info(f'Logging "make_association" error: {err}...')
        print('Logging "make_association" error to elastic_ip.log...')

def destroy_eip(Allocation_Id, region='us-east-1'):
    try:
        os.system("aws ec2 release-address --allocation-id " + Allocation_Id + ' --region '+ region)
        logging.info("Deleted Elastic_IP: " + Allocation_Id)
    except Exception as err:
        logging.info(f'Logging "destroy_eip" error: {err}...')
        print('Logging "destroy_eip" error to elastic_ip.log...')

def erase_eip(region='us-east-1'):
    try:
        ''' Deletes all Elastic Ips that do not have any dependencies '''
        output = os.popen('aws ec2 describe-addresses  --region ' + region).read()
        eip_data = json.loads(str(output))
        for data in eip_data['Addresses']:
            print(f'Delete {data["AllocationId"]} in {region}...')
            destroy_eip(data['AllocationId'], region=region)
            logging.info('Logging erase_eip: ' + data['AllocationId'] + ' in region: '+ region)

        new_data = json.dumps(data, indent=2)
        print(new_data)
    except Exception as err:
        logging.info(f'Logging "erase_eip" error: {err}...')
        print('Logging "erase_eip" error to elastic_ip.log...')

# ---------------------------------------------------- End -----------------------------------------------------------

