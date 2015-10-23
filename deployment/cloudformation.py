#!/usr/bin/env python
# Converted from EC2InstanceSample.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/
from troposphere import (
    Base64, FindInMap, GetAtt, GetAZs, Name,
    Parameter, Output, Ref, Template, Tags, Join,
    ec2, elasticloadbalancing as elb, autoscaling, rds,
    elasticache, route53, s3, Equals
)

template = Template()
template.add_version("2010-09-09")

project = template.add_parameter(Parameter(
    "Project",
    Description="Name of the Project",
    Type="String",
))

environment = template.add_parameter(Parameter(
    "Environment",
    Description="Name of the Environment",
    AllowedValues=['Prod', 'Test'],
    Default='Test',
    Type="String",
))

# if provided, will create a db with the snapshot
db_snapshot = template.add_parameter(Parameter(
    "DB",
    Description="ID of db snapshot to restore",
    Type="String",
    Default='', #not sure if actually optional, make it so
))

all_layers = template.add_parameter(Parameter(
    "CreateAllLayers",
    Description="True if creating Webapp/Varnish Layers, False if just Admin",
    Type="String",
    Default="False",
))

# This branch gets tied to the resulting Stack, which is used for
# deploying updates from that branch and determining endpoints. The
# default Stack is tied to the 'develop' branch, and this uses
# predefined endpoints
branch = template.add_parameter(Parameter(
    "Branch",
    Description="Branch to deploy",
    Type="String",
    Default='develop',
))

varnish_subdomain = template.add_parameter(Parameter(
    "VarnishSubDomain",
    Description="Subdomain for Varnish ELB",
    Type="String",
))

webapp_subdomain = template.add_parameter(Parameter(
    "WebappSubDomain",
    Description="Subdomain for the Webapp ELB",
    Type="String",
))

admin_subdomain = template.add_parameter(Parameter(
    "AdminSubDomain",
    Description="Subdomain for the Admin ELB",
    Type="String",
))

template.add_condition(
    "AllLayers",
    Equals(
        Ref("CreateAllLayers"),
        "True"
    ),
)

VPC = template.add_resource(
    ec2.VPC(
        "VPC",
        EnableDnsSupport="true",
        CidrBlock="10.1.1.0/16",
        EnableDnsHostnames="true",
        Tags=Tags(
            Project=Ref(project),
            Environment=Ref(environment),
        )
    )
)

CacheSG = template.add_resource(
    ec2.SecurityGroup(
        "CacheSecurityGroup",
        VpcId=Ref(VPC),
        GroupDescription="Cache Security Group",
    )
)

PublicSG = template.add_resource(
    ec2.SecurityGroup(
        "SecurityGroup",
        VpcId=Ref(VPC),
        GroupDescription="Security Group",
        Tags=Tags(
            Project=Ref(project),
            Environment=Ref(environment),
        )
    )
)

PrivateSG = template.add_resource(
    ec2.SecurityGroup(
        "PrivateSecurityGroup",
        VpcId=Ref(VPC),
        GroupDescription="Private Security Group",
    )
)

PrivatePostgresIngress = template.add_resource(
    ec2.SecurityGroupIngress(
        "PrivatePostgresIngress",
        IpProtocol='tcp',
        FromPort='5432',
        ToPort='5432',
        GroupId=Ref(PrivateSG),
        SourceSecurityGroupId=Ref(PublicSG),
    )
)

PublicSGhttpIngress = template.add_resource(
    ec2.SecurityGroupIngress(
        "PublicSGhttpIngress",
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=80,
        ToPort=80,
        GroupId=Ref(PublicSG)
    )
)

PublicSGsshIngress = template.add_resource(
    ec2.SecurityGroupIngress(
        "PublicSGsshIngress",
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22,
        GroupId=Ref(PublicSG)
    )
)

PublicSGcacheIngress = template.add_resource(
    ec2.SecurityGroupIngress(
        "CacheSGcacheIngress",
        FromPort=11211,
        IpProtocol='tcp',
        ToPort=11211,
        SourceSecurityGroupId=Ref(PublicSG),
        GroupId=Ref(CacheSG)
    )
)

public_subnet = template.add_resource(
    ec2.Subnet(
        "PublicSubnet",
        AvailabilityZone='us-east-1d',
        CidrBlock="10.1.1.0/24",
        VpcId=Ref(VPC),
    )
)

private_subnet1 = template.add_resource(
    ec2.Subnet(
        "PrivateSubnet1",
        AvailabilityZone='us-east-1e',
        CidrBlock="10.1.2.0/24",
        VpcId=Ref(VPC),
    )
)

private_subnet2 = template.add_resource(
    ec2.Subnet(
        "PrivateSubnet2",
        AvailabilityZone='us-east-1c',
        CidrBlock="10.1.3.0/24",
        VpcId=Ref(VPC),
    )
)

route_table = template.add_resource(
    ec2.RouteTable(
        "RouteTable",
        VpcId=Ref(VPC),
    )
)

vpc_gateway = template.add_resource(
    ec2.InternetGateway(
        "VPCGateway",
    )
)

public_route = template.add_resource(
    ec2.Route(
        "GatewayRoute",
        DestinationCidrBlock="0.0.0.0/0",
        GatewayId=Ref(vpc_gateway),
        RouteTableId=Ref(route_table),
    )
)

subnetRouteTableAssociation = template.add_resource(
    ec2.SubnetRouteTableAssociation(
        "SubnetRouteTableAssociation",
        SubnetId=Ref(public_subnet),
        RouteTableId=Ref(route_table),
    )
)

gatewayAttachment = template.add_resource(
    ec2.VPCGatewayAttachment(
        'AttachGateway',
        VpcId=Ref(VPC),
        InternetGatewayId=Ref(vpc_gateway)
    )
)

db_subnet = template.add_resource(
    rds.DBSubnetGroup(
        "DBSubnetGroup",
        DBSubnetGroupDescription='DB Subnet group for MNN DB',
        SubnetIds=[Ref(private_subnet1), Ref(private_subnet2)],
    )
)

django_database = template.add_resource(
    rds.DBInstance(
        "djangoDB",
        AllocatedStorage='100',
        AllowMajorVersionUpgrade=True,
        AutoMinorVersionUpgrade=True,
        BackupRetentionPeriod='3',
        DBInstanceClass='db.m3.medium',
        DBSnapshotIdentifier=Ref(db_snapshot),
        DBSubnetGroupName=Ref(db_subnet),
        Engine='postgres',
        EngineVersion='9.3.5',
        Iops=1000,
        MasterUsername='bob',
        MasterUserPassword='tales_test',
        Port=5432,
        StorageType='io1',
        VPCSecurityGroups=[Ref(PrivateSG)]
    )
)

static_s3 = template.add_resource(
    s3.Bucket(
        "StaticBucket",
    )
)


###############
# Admin Layer #
###############

admin_load_balancer = template.add_resource(
    elb.LoadBalancer(
        "TestAdminLB",
        ConnectionDrainingPolicy=elb.ConnectionDrainingPolicy(
            Enabled=True,
            Timeout=60
        ),
        CrossZone=True,
        LoadBalancerName=Join('', [Ref(project), Ref(environment),
                                   'Admin', Ref(branch)]),
        Listeners=[
            elb.Listener(
                InstancePort='80',
                InstanceProtocol='HTTP',
                LoadBalancerPort='80',
                Protocol='HTTP'
            ),
        ],
        SecurityGroups=[Ref(PublicSG)],
        Subnets=[
            Ref(public_subnet),
        ],
        Tags=Tags(
            Project=Ref(project),
            Environment=Ref(environment),
            Layer='Admin',
        ),
    )
)

admin_lc = template.add_resource(
    autoscaling.LaunchConfiguration(
        "TestAdminLaunchConfig",
        AssociatePublicIpAddress=True,
        ImageId='ami-9aec9ff2',
        InstanceType='m3.medium',
        KeyName='MNN Default Key Pair',
        SecurityGroups=[Ref(PublicSG)]
    )
)

admin_asg = template.add_resource(
    autoscaling.AutoScalingGroup(
        "TestAdminAutoScaleGroup",
        AvailabilityZones=['us-east-1d'],
        DesiredCapacity='1',
        LaunchConfigurationName=Ref(admin_lc),
        LoadBalancerNames=[Ref(admin_load_balancer)],
        MaxSize='1',
        MinSize='1',
        Tags=autoscaling.Tags(
            Project=Ref(project),
            Environment=Ref(environment),
            Layer='Admin',
            Branch=Ref(branch),
        ),
        VPCZoneIdentifier=[Ref(public_subnet)],
    )
)

################
# Webapp Layer #
################

webapp_load_balancer = template.add_resource(
    elb.LoadBalancer(
        "TestWebappLB",
        ConnectionDrainingPolicy=elb.ConnectionDrainingPolicy(
            Enabled=True,
            Timeout=60
        ),
        Condition="AllLayers",
        CrossZone=True,
        LoadBalancerName=Join('', [Ref(project), Ref(environment),
                                   'Webapp', Ref(branch)]),
        Listeners=[
            elb.Listener(
                InstancePort='80',
                InstanceProtocol='HTTP',
                LoadBalancerPort='80',
                Protocol='HTTP'
            ),
        ],
        SecurityGroups=[Ref(PublicSG),],
        Subnets=[
            Ref(public_subnet),
        ],
        Tags=Tags(
            Project=Ref(project),
            Environment=Ref(environment),
            Layer='Webapp',
        ),
    )
)

webapp_lc = template.add_resource(
    autoscaling.LaunchConfiguration(
        "TestWebappLC",
        AssociatePublicIpAddress=True,
        Condition="AllLayers",
        ImageId='ami-9aec9ff2',
        InstanceType='m3.medium',
        KeyName='MNN Default Key Pair',
        SecurityGroups=[Ref(PublicSG)]
    )
)

webapp_asg = template.add_resource(
    autoscaling.AutoScalingGroup(
        "TestWebappASG",
        AvailabilityZones=['us-east-1d'],
        Condition="AllLayers",
        DesiredCapacity='1',
        LaunchConfigurationName=Ref(webapp_lc),
        LoadBalancerNames=[Ref(webapp_load_balancer)],
        MaxSize='1',
        MinSize='1',
        Tags=autoscaling.Tags(
            Project=Ref(project),
            Environment=Ref(environment),
            Layer='Webapp',
            Branch=Ref(branch),
        ),
        VPCZoneIdentifier=[Ref(public_subnet)],
    )
)

#################
# Varnish Layer #
#################

varnish_load_balancer = template.add_resource(
    elb.LoadBalancer(
        "TestVarnishLB",
        Condition="AllLayers",
        ConnectionDrainingPolicy=elb.ConnectionDrainingPolicy(
            Enabled=True,
            Timeout=60
        ),
        CrossZone=True,
        LoadBalancerName=Join('', [Ref(project), Ref(environment),
                                   'Varnish', Ref(branch)]),
        Listeners=[
            elb.Listener(
                InstancePort='80',
                InstanceProtocol='HTTP',
                LoadBalancerPort='80',
                Protocol='HTTP'
            ),
        ],
        SecurityGroups=[Ref(PublicSG),],
        Subnets=[
            Ref(public_subnet),
        ],
        Tags=Tags(
            Project=Ref(project),
            Environment=Ref(environment),
            Layer='Varnish',
        ),
    )
)

varnish_lc = template.add_resource(
    autoscaling.LaunchConfiguration(
        "TestVarnishLC",
        AssociatePublicIpAddress=True,
        Condition="AllLayers",
        ImageId='ami-9aec9ff2',
        InstanceType='t2.micro',
        KeyName='MNN Default Key Pair',
        SecurityGroups=[Ref(PublicSG)]
    )
)

varnish_asg = template.add_resource(
    autoscaling.AutoScalingGroup(
        "TestVarnishASG",
        AvailabilityZones=['us-east-1d'],
        Condition="AllLayers",
        DesiredCapacity='1',
        LaunchConfigurationName=Ref(varnish_lc),
        LoadBalancerNames=[Ref(varnish_load_balancer)],
        MaxSize='1',
        MinSize='1',
        Tags=autoscaling.Tags(
            Project=Ref(project),
            Environment=Ref(environment),
            Layer='Varnish',
            Branch=Ref(branch),
        ),
        VPCZoneIdentifier=[Ref(public_subnet)],
    )
)


#################
# Cache Cluster #
#################

cache_subnet_group = template.add_resource(
    elasticache.SubnetGroup(
        "TestCacheSubnetGroup",
        Description='Subnet Group for cache cluster.',
        SubnetIds=[Ref(public_subnet),
                   Ref(private_subnet1),
                   Ref(private_subnet2)],
    )
)


cache_cluster = template.add_resource(
    elasticache.CacheCluster(
        "TestCache",
        AutoMinorVersionUpgrade=True,
        CacheNodeType='cache.m3.medium',
        CacheSubnetGroupName=Ref(cache_subnet_group),
        Engine='memcached',
        NumCacheNodes=1,
        VpcSecurityGroupIds=[Ref(CacheSG)],
    )
)

###########
# Route53 #
###########

record_set_group = template.add_resource(
    route53.RecordSetGroup(
        "TestDNS",
        Condition="AllLayers",
        HostedZoneName='mnndev.com.',
        RecordSets=[
            route53.RecordSet(
                Name=Ref(varnish_subdomain),
                Type='A',
                AliasTarget=route53.AliasTarget(
                    GetAtt(varnish_load_balancer, 'CanonicalHostedZoneNameID'),
                    GetAtt(varnish_load_balancer, 'CanonicalHostedZoneName')
                ),
            ),
            route53.RecordSet(
                Name=Ref(webapp_subdomain),
                Type='A',
                AliasTarget=route53.AliasTarget(
                    GetAtt(webapp_load_balancer, 'CanonicalHostedZoneNameID'),
                    GetAtt(webapp_load_balancer, 'CanonicalHostedZoneName')
                ),
            ),
        ]
    ),
)

record_set_group2 = template.add_resource(
    route53.RecordSetGroup(
        "TestAdminDNS",
        HostedZoneName='mnndev.com.',
        RecordSets=[
            route53.RecordSet(
                Name=Ref(admin_subdomain),
                Type='A',
                AliasTarget=route53.AliasTarget(
                    GetAtt(admin_load_balancer, 'CanonicalHostedZoneNameID'),
                    GetAtt(admin_load_balancer, 'CanonicalHostedZoneName')
                )
            ),
        ]
    ),
)

###########
# Outputs #
###########

template.add_output([
    Output('DjangoDBEndpoint', Value=GetAtt(django_database, 'Endpoint.Address')),
    Output('DjangoDBInstanceID', Value=Ref(django_database)),
    Output('CacheEndpoint', Value=GetAtt(cache_cluster, 'ConfigurationEndpoint.Address')),
    Output('WebappLBEndpoint',
           Value=GetAtt(webapp_load_balancer, 'DNSName'),
           Condition="AllLayers",
       ),
    Output('AdminLBEndpoint', Value=GetAtt(admin_load_balancer,'DNSName')),
    Output('StaticBucket', Value=Ref(static_s3)),
    Output('AdminURL', Value=Ref(admin_subdomain)),
])

# This will create a new file or **overwrite an existing file**.
f = open("cloudformation.json", "w")
try:
    f.write(template.to_json()) # Write a string to a file
finally:
    f.close()
