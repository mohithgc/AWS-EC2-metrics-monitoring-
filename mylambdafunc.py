import boto3
import csv
import datetime
from pprint import pprint
def lambda_handler(event, context):
 ec2_cli=boto3.client(service_name='ec2')
 cw = boto3.client('cloudwatch')
 s3 = boto3.resource('s3')
 bucket = s3.Bucket('mybucketname')
 key = 'mymetricsfilename.csv'
 ti = datetime.datetime.now()
 c1= cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Maximum'],
        Dimensions=[{'Name':'InstanceId', 'Value':'i-00457d74c0e7fdd8a'}]
        )
 c2= cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='DiskReadOps',
        Namespace='AWS/EC2',
        Statistics=['Maximum'],
        Dimensions=[{'Name':'InstanceId', 'Value':'i-00457d74c0e7fdd8a'}]
        )
 c3= cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='DiskWriteOps',
        Namespace='AWS/EC2',
        Statistics=['Maximum'],
        Dimensions=[{'Name':'InstanceId', 'Value':'i-00457d74c0e7fdd8a'}]
        )
 c4= cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='NetworkIn',
        Namespace='AWS/EC2',
        Statistics=['Maximum'],
        Dimensions=[{'Name':'InstanceId', 'Value':'i-00457d74c0e7fdd8a'}]
        )
 c5= cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='NetworkOut',
        Namespace='AWS/EC2',
        Statistics=['Maximum'],
        Dimensions=[{'Name':'InstanceId', 'Value':'i-00457d74c0e7fdd8a'}]
        )       
 c6= cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUCreditUsage',
        Namespace='AWS/EC2',
        Statistics=['Maximum'],
        Dimensions=[{'Name':'InstanceId', 'Value':'i-00457d74c0e7fdd8a'}]
        )   
 c7= cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUCreditBalance',
        Namespace='AWS/EC2',
        Statistics=['Maximum'],
        Dimensions=[{'Name':'InstanceId', 'Value':'i-00457d74c0e7fdd8a'}]
        )              
 c=[c1,c2,c3,c4,c5,c6,c7]
 collect_all_regions=[]
 for each_region in ec2_cli.describe_regions()['Regions']: 
  collect_all_regions.append(each_region['RegionName'])
 print(collect_all_regions)

 fo=open('/tmp/mymetricsfilename.csv','w+',newline='')   

 data_obj=csv.writer(fo)
 data_obj.writerow(['SLno','Time when your program ran','EC2 instance ID',"InstanceType","Metric Name","Metric Value"])

 cnt=1
 for each_region in collect_all_regions:
  ec2_re=boto3.resource(service_name='ec2',region_name=each_region)
  for each_ins_in_reg in ec2_re.instances.all():
   for each in c :
    
    
    
    
     

      data_obj.writerow([cnt," %s" %ti,each_ins_in_reg.instance_id,each_ins_in_reg.instance_type,each["Label"],each["Datapoints"][0]["Maximum"],each["Datapoints"][0]["Unit"]])
   
      cnt+=1
 fo.close()
 bucket.upload_file('/tmp/mymetricsfilename.csv', key)