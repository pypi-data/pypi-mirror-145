# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from tencentcloud.common.abstract_model import AbstractModel


class Account(AbstractModel):
    """TencentDB account information

    """

    def __init__(self):
        r"""
        :param User: Account name
        :type User: str
        :param Host: Host address
        :type Host: str
        """
        self.User = None
        self.Host = None


    def _deserialize(self, params):
        self.User = params.get("User")
        self.Host = params.get("Host")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ActivateHourDBInstanceRequest(AbstractModel):
    """ActivateHourDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list
        :type InstanceIds: list of str
        """
        self.InstanceIds = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ActivateHourDBInstanceResponse(AbstractModel):
    """ActivateHourDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param SuccessInstanceIds: IDs of isolated instances
        :type SuccessInstanceIds: list of str
        :param FailedInstanceIds: IDs of instances failed to be isolated
        :type FailedInstanceIds: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SuccessInstanceIds = None
        self.FailedInstanceIds = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SuccessInstanceIds = params.get("SuccessInstanceIds")
        self.FailedInstanceIds = params.get("FailedInstanceIds")
        self.RequestId = params.get("RequestId")


class AssociateSecurityGroupsRequest(AbstractModel):
    """AssociateSecurityGroups request structure.

    """

    def __init__(self):
        r"""
        :param Product: Database engine name. Valid value: `mariadb`.
        :type Product: str
        :param SecurityGroupId: ID of the security group to be associated in the format of sg-efil73jd.
        :type SecurityGroupId: str
        :param InstanceIds: ID(s) of the instance(s) to be associated in the format of tdsql-lesecurk. You can specify multiple instances.
        :type InstanceIds: list of str
        """
        self.Product = None
        self.SecurityGroupId = None
        self.InstanceIds = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssociateSecurityGroupsResponse(AbstractModel):
    """AssociateSecurityGroups response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CancelDcnJobRequest(AbstractModel):
    """CancelDcnJob request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Disaster recovery instance ID
        :type InstanceId: str
        """
        self.InstanceId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelDcnJobResponse(AbstractModel):
    """CancelDcnJob response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Task ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class CloneAccountRequest(AbstractModel):
    """CloneAccount request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param SrcUser: Source user account name
        :type SrcUser: str
        :param SrcHost: Source user host
        :type SrcHost: str
        :param DstUser: Target user account name
        :type DstUser: str
        :param DstHost: Target user host
        :type DstHost: str
        :param DstDesc: Description of target account
        :type DstDesc: str
        """
        self.InstanceId = None
        self.SrcUser = None
        self.SrcHost = None
        self.DstUser = None
        self.DstHost = None
        self.DstDesc = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SrcUser = params.get("SrcUser")
        self.SrcHost = params.get("SrcHost")
        self.DstUser = params.get("DstUser")
        self.DstHost = params.get("DstHost")
        self.DstDesc = params.get("DstDesc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CloneAccountResponse(AbstractModel):
    """CloneAccount response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task flow ID.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class CloseDBExtranetAccessRequest(AbstractModel):
    """CloseDBExtranetAccess request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: ID of instance for which to disable public network access. The ID is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param Ipv6Flag: Whether IPv6 is used. Default value: 0
        :type Ipv6Flag: int
        """
        self.InstanceId = None
        self.Ipv6Flag = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Ipv6Flag = params.get("Ipv6Flag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CloseDBExtranetAccessResponse(AbstractModel):
    """CloseDBExtranetAccess response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID. The task status can be queried through the `DescribeFlow` API.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ColumnPrivilege(AbstractModel):
    """Column permission information

    """

    def __init__(self):
        r"""
        :param Database: Database name
        :type Database: str
        :param Table: Table name
        :type Table: str
        :param Column: Column name
        :type Column: str
        :param Privileges: Permission information
        :type Privileges: list of str
        """
        self.Database = None
        self.Table = None
        self.Column = None
        self.Privileges = None


    def _deserialize(self, params):
        self.Database = params.get("Database")
        self.Table = params.get("Table")
        self.Column = params.get("Column")
        self.Privileges = params.get("Privileges")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ConstraintRange(AbstractModel):
    """Range of constraint type values

    """

    def __init__(self):
        r"""
        :param Min: Minimum value when constraint type is `section`
        :type Min: str
        :param Max: Maximum value when constraint type is `section`
        :type Max: str
        """
        self.Min = None
        self.Max = None


    def _deserialize(self, params):
        self.Min = params.get("Min")
        self.Max = params.get("Max")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CopyAccountPrivilegesRequest(AbstractModel):
    """CopyAccountPrivileges request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param SrcUserName: Source username
        :type SrcUserName: str
        :param SrcHost: Access host allowed for source user
        :type SrcHost: str
        :param DstUserName: Target username
        :type DstUserName: str
        :param DstHost: Access host allowed for target user
        :type DstHost: str
        :param SrcReadOnly: `ReadOnly` attribute of source account
        :type SrcReadOnly: str
        :param DstReadOnly: `ReadOnly` attribute of target account
        :type DstReadOnly: str
        """
        self.InstanceId = None
        self.SrcUserName = None
        self.SrcHost = None
        self.DstUserName = None
        self.DstHost = None
        self.SrcReadOnly = None
        self.DstReadOnly = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SrcUserName = params.get("SrcUserName")
        self.SrcHost = params.get("SrcHost")
        self.DstUserName = params.get("DstUserName")
        self.DstHost = params.get("DstHost")
        self.SrcReadOnly = params.get("SrcReadOnly")
        self.DstReadOnly = params.get("DstReadOnly")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CopyAccountPrivilegesResponse(AbstractModel):
    """CopyAccountPrivileges response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateAccountRequest(AbstractModel):
    """CreateAccount request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param UserName: Login username, which can contain 1-32 letters, digits, underscores, and hyphens.
        :type UserName: str
        :param Host: Host that can be logged in to, which is in the same format as the host of the MySQL account and supports wildcards, such as %, 10.%, and 10.20.%.
        :type Host: str
        :param Password: Account password. It must contain 8-32 characters in all of the following four types: lowercase letters, uppercase letters, digits, and symbols (()~!@#$%^&*-+=_|{}[]:<>,.?/), and cannot start with a slash (/).
        :type Password: str
        :param ReadOnly: Whether to create a read-only account. 0: no; 1: for the account's SQL requests, the secondary will be used first, and if it is unavailable, the primary will be used; 2: the secondary will be used first, and if it is unavailable, the operation will fail.
        :type ReadOnly: int
        :param Description: Account remarks, which can contain 0-256 letters, digits, and common symbols.
        :type Description: str
        :param DelayThresh: Determines whether the secondary is unavailable based on the passed-in time
        :type DelayThresh: int
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.Password = None
        self.ReadOnly = None
        self.Description = None
        self.DelayThresh = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.Password = params.get("Password")
        self.ReadOnly = params.get("ReadOnly")
        self.Description = params.get("Description")
        self.DelayThresh = params.get("DelayThresh")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAccountResponse(AbstractModel):
    """CreateAccount response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is passed through from the input parameters.
        :type InstanceId: str
        :param UserName: Username, which is passed through from the input parameters.
        :type UserName: str
        :param Host: Host allowed for access, which is passed through from the input parameters.
        :type Host: str
        :param ReadOnly: Passed through from the input parameters.
        :type ReadOnly: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.ReadOnly = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.ReadOnly = params.get("ReadOnly")
        self.RequestId = params.get("RequestId")


class CreateHourDBInstanceRequest(AbstractModel):
    """CreateHourDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param Zones: AZs to deploy instance nodes. You can specify up to two AZs.
        :type Zones: list of str
        :param NodeCount: Number of nodes.
        :type NodeCount: int
        :param Memory: Memory size in GB.
        :type Memory: int
        :param Storage: Storage size in GB.
        :type Storage: int
        :param Count: Number of instances to purchase.
        :type Count: int
        :param ProjectId: Project ID. If this parameter is not passed in, the default project will be used.
        :type ProjectId: int
        :param VpcId: Unique ID of the network. If this parameter is not passed in, the classic network will be used.
        :type VpcId: str
        :param SubnetId: Unique ID of the subnet. If `VpcId` is specified, this parameter is required.
        :type SubnetId: str
        :param DbVersionId: Database engine version. Valid values:
10.0.10: MariaDB 10.0.10;
10.1.9: MariaDB 10.1.9;
5.7.17: Percona 5.7.17.
If this parameter is left empty, `10.1.9` will be used.
        :type DbVersionId: str
        :param InstanceName: Custom name of the instance.
        :type InstanceName: str
        :param SecurityGroupIds: Security group ID. If this parameter is not passed in, no security groups will be associated when the instance is created.
        :type SecurityGroupIds: list of str
        :param Ipv6Flag: Whether IPv6 is supported.
        :type Ipv6Flag: int
        :param ResourceTags: Array of tag key-value pairs.
        :type ResourceTags: list of ResourceTag
        :param DcnRegion: If you create a disaster recovery instance, you need to use this parameter to specify the region of the associated primary instance so that the disaster recovery instance can sync data with the primary instance over the Data Communication Network (DCN).
        :type DcnRegion: str
        :param DcnInstanceId: If you create a disaster recovery instance, you need to use this parameter to specify the ID of the associated primary instance so that the disaster recovery instance can sync data with the primary instance over the Data Communication Network (DCN).
        :type DcnInstanceId: str
        :param InitParams: List of parameters. Valid values: `character_set_server` (character set; required); `lower_case_table_names` (table name case sensitivity; required; 0: case-sensitive; 1: case-insensitive); `innodb_page_size` (InnoDB data page size; default size: 16 KB); `sync_mode` (sync mode; 0: async; 1: strong sync; 2: downgradable strong sync; default value: 2).
        :type InitParams: list of DBParamValue
        :param RollbackInstanceId: ID of the instance whose backup data will be rolled back to the new instance you create.
        :type RollbackInstanceId: str
        :param RollbackTime: Rollback time.
        :type RollbackTime: str
        """
        self.Zones = None
        self.NodeCount = None
        self.Memory = None
        self.Storage = None
        self.Count = None
        self.ProjectId = None
        self.VpcId = None
        self.SubnetId = None
        self.DbVersionId = None
        self.InstanceName = None
        self.SecurityGroupIds = None
        self.Ipv6Flag = None
        self.ResourceTags = None
        self.DcnRegion = None
        self.DcnInstanceId = None
        self.InitParams = None
        self.RollbackInstanceId = None
        self.RollbackTime = None


    def _deserialize(self, params):
        self.Zones = params.get("Zones")
        self.NodeCount = params.get("NodeCount")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.Count = params.get("Count")
        self.ProjectId = params.get("ProjectId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.DbVersionId = params.get("DbVersionId")
        self.InstanceName = params.get("InstanceName")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        self.Ipv6Flag = params.get("Ipv6Flag")
        if params.get("ResourceTags") is not None:
            self.ResourceTags = []
            for item in params.get("ResourceTags"):
                obj = ResourceTag()
                obj._deserialize(item)
                self.ResourceTags.append(obj)
        self.DcnRegion = params.get("DcnRegion")
        self.DcnInstanceId = params.get("DcnInstanceId")
        if params.get("InitParams") is not None:
            self.InitParams = []
            for item in params.get("InitParams"):
                obj = DBParamValue()
                obj._deserialize(item)
                self.InitParams.append(obj)
        self.RollbackInstanceId = params.get("RollbackInstanceId")
        self.RollbackTime = params.get("RollbackTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateHourDBInstanceResponse(AbstractModel):
    """CreateHourDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param DealName: Order ID, which is used in the `DescribeOrders` API.
 The parameter can be used to either query order details or call the user account APIs to make another payment when this payment fails.
        :type DealName: str
        :param InstanceIds: IDs of the instances you have purchased in this order. If no instance IDs are returned, you can query them with the `DescribeOrders` API. You can also use the `DescribeDBInstances` API to check whether an instance has been created successfully.
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type InstanceIds: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DealName = None
        self.InstanceIds = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DealName = params.get("DealName")
        self.InstanceIds = params.get("InstanceIds")
        self.RequestId = params.get("RequestId")


class DBAccount(AbstractModel):
    """TencentDB account information

    """

    def __init__(self):
        r"""
        :param UserName: Username
        :type UserName: str
        :param Host: Host from which a user can log in (corresponding to the `host` field for a MySQL user; a user is uniquely identified by username and host; this parameter is in IP format and ends with % for IP range; % can be entered; if this parameter is left empty, % will be used by default)
        :type Host: str
        :param Description: User remarks
        :type Description: str
        :param CreateTime: Creation time
        :type CreateTime: str
        :param UpdateTime: Last updated time
        :type UpdateTime: str
        :param ReadOnly: Read-only flag. 0: no; 1: for the account's SQL requests, the secondary will be used first, and if it is unavailable, the primary will be used; 2: the secondary will be used first, and if it is unavailable, the operation will fail.
        :type ReadOnly: int
        :param DelayThresh: This field is meaningful for read-only accounts, indicating to select a secondary where the primary/secondary delay is below this value
Note: this field may return null, indicating that no valid values can be obtained.
        :type DelayThresh: int
        """
        self.UserName = None
        self.Host = None
        self.Description = None
        self.CreateTime = None
        self.UpdateTime = None
        self.ReadOnly = None
        self.DelayThresh = None


    def _deserialize(self, params):
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.Description = params.get("Description")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.ReadOnly = params.get("ReadOnly")
        self.DelayThresh = params.get("DelayThresh")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DBBackupTimeConfig(AbstractModel):
    """TencentDB instance backup time configuration information

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param StartBackupTime: Start time of daily backup window in the format of `mm:ss`, such as 22:00
        :type StartBackupTime: str
        :param EndBackupTime: End time of daily backup window in the format of `mm:ss`, such as 23:00
        :type EndBackupTime: str
        """
        self.InstanceId = None
        self.StartBackupTime = None
        self.EndBackupTime = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartBackupTime = params.get("StartBackupTime")
        self.EndBackupTime = params.get("EndBackupTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DBInstance(AbstractModel):
    """TencentDB instance details.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which uniquely identifies a TDSQL instance
        :type InstanceId: str
        :param InstanceName: Customizable instance name
        :type InstanceName: str
        :param AppId: Application ID of instance
        :type AppId: int
        :param ProjectId: Project ID of instance
        :type ProjectId: int
        :param Region: Instance region name, such as ap-shanghai
        :type Region: str
        :param Zone: Instance AZ name, such as ap-guangzhou-1
        :type Zone: str
        :param VpcId: VPC ID, which is 0 if the basic network is used
        :type VpcId: int
        :param SubnetId: Subnet ID, which is 0 if the basic network is used
        :type SubnetId: int
        :param Status: Instance status. Valid values: `0` (creating), `1` (running task), `2` (running), `3` (uninitialized), `-1` (isolated), `4` (initializing), `5` (eliminating), `6` (restarting), `7` (migrating data)
        :type Status: int
        :param Vip: Private IP address
        :type Vip: str
        :param Vport: Private network port
        :type Vport: int
        :param WanDomain: Domain name for public network access, which can be resolved by the public network
        :type WanDomain: str
        :param WanVip: Public IP address, which can be accessed over the public network
        :type WanVip: str
        :param WanPort: Public network port
        :type WanPort: int
        :param CreateTime: Instance creation time in the format of `2006-01-02 15:04:05`
        :type CreateTime: str
        :param UpdateTime: Last updated time of instance in the format of `2006-01-02 15:04:05`
        :type UpdateTime: str
        :param AutoRenewFlag: Auto-renewal flag. 0: no, 1: yes
        :type AutoRenewFlag: int
        :param PeriodEndTime: Instance expiration time in the format of `2006-01-02 15:04:05`
        :type PeriodEndTime: str
        :param Uin: Instance account
        :type Uin: str
        :param TdsqlVersion: TDSQL version information
        :type TdsqlVersion: str
        :param Memory: Instance memory size in GB
        :type Memory: int
        :param Storage: Instance storage capacity in GB
        :type Storage: int
        :param UniqueVpcId: VPC ID in string type
        :type UniqueVpcId: str
        :param UniqueSubnetId: VPC subnet ID in string type
        :type UniqueSubnetId: str
        :param OriginSerialId: Original ID of instance (this field is obsolete and should not be depended on)
        :type OriginSerialId: str
        :param NodeCount: Number of nodes. 2: one master and one slave, 3: one master and two slaves
        :type NodeCount: int
        :param IsTmp: Whether it is a temp instance. 0: no, non-zero value: yes
        :type IsTmp: int
        :param ExclusterId: Dedicated cluster ID. If this parameter is empty, the instance is a general instance
        :type ExclusterId: str
        :param Id: Numeric ID of instance (this field is obsolete and should not be depended on)
        :type Id: int
        :param Pid: Product type ID
        :type Pid: int
        :param Qps: Maximum QPS value
        :type Qps: int
        :param Paymode: Billing mode
Note: this field may return null, indicating that no valid values can be obtained.
        :type Paymode: str
        :param Locker: Async task flow ID when an async task is in progress on an instance
Note: this field may return null, indicating that no valid values can be obtained.
        :type Locker: int
        :param StatusDesc: Current instance running status description
Note: this field may return null, indicating that no valid values can be obtained.
        :type StatusDesc: str
        :param WanStatus: Public network access status. 0: not enabled, 1: enabled, 2: disabled, 3: enabling
        :type WanStatus: int
        :param IsAuditSupported: Whether the instance supports audit. 1: yes, 0: no
        :type IsAuditSupported: int
        :param Machine: Model
        :type Machine: str
        :param IsEncryptSupported: Whether data encryption is supported. 1: yes, 0: no
        :type IsEncryptSupported: int
        :param Cpu: Number of CPU cores of instance
        :type Cpu: int
        :param Ipv6Flag: Indicates whether the instance uses IPv6
Note: this field may return null, indicating that no valid values can be obtained.
        :type Ipv6Flag: int
        :param Vipv6: Private network IPv6 address
Note: this field may return null, indicating that no valid values can be obtained.
        :type Vipv6: str
        :param WanVipv6: Public network IPv6 address
Note: this field may return null, indicating that no valid values can be obtained.
        :type WanVipv6: str
        :param WanPortIpv6: Public network IPv6 port
Note: this field may return null, indicating that no valid values can be obtained.
        :type WanPortIpv6: int
        :param WanStatusIpv6: Public network IPv6 status
Note: this field may return null, indicating that no valid values can be obtained.
        :type WanStatusIpv6: int
        :param DbEngine: Database engine
Note: this field may return null, indicating that no valid values can be obtained.
        :type DbEngine: str
        :param DbVersion: Database version
Note: this field may return null, indicating that no valid values can be obtained.
        :type DbVersion: str
        :param DcnFlag: DCN type. Valid values: 0 (null), 1 (primary instance), 2 (disaster recovery instance)
Note: this field may return null, indicating that no valid values can be obtained.
        :type DcnFlag: int
        :param DcnStatus: DCN status. Valid values: 0 (null), 1 (creating), 2 (syncing), 3 (disconnected)
Note: this field may return null, indicating that no valid values can be obtained.
        :type DcnStatus: int
        :param DcnDstNum: The number of DCN disaster recovery instances
Note: this field may return null, indicating that no valid values can be obtained.
        :type DcnDstNum: int
        :param InstanceType: Instance type. Valid values: `1` (dedicated primary instance), `2` (primary instance), `3` (disaster recovery instance), and `4` (dedicated disaster recovery instance).
Note: this field may return null, indicating that no valid values can be obtained.
        :type InstanceType: int
        :param ResourceTags: Instance tag information
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type ResourceTags: list of ResourceTag
        """
        self.InstanceId = None
        self.InstanceName = None
        self.AppId = None
        self.ProjectId = None
        self.Region = None
        self.Zone = None
        self.VpcId = None
        self.SubnetId = None
        self.Status = None
        self.Vip = None
        self.Vport = None
        self.WanDomain = None
        self.WanVip = None
        self.WanPort = None
        self.CreateTime = None
        self.UpdateTime = None
        self.AutoRenewFlag = None
        self.PeriodEndTime = None
        self.Uin = None
        self.TdsqlVersion = None
        self.Memory = None
        self.Storage = None
        self.UniqueVpcId = None
        self.UniqueSubnetId = None
        self.OriginSerialId = None
        self.NodeCount = None
        self.IsTmp = None
        self.ExclusterId = None
        self.Id = None
        self.Pid = None
        self.Qps = None
        self.Paymode = None
        self.Locker = None
        self.StatusDesc = None
        self.WanStatus = None
        self.IsAuditSupported = None
        self.Machine = None
        self.IsEncryptSupported = None
        self.Cpu = None
        self.Ipv6Flag = None
        self.Vipv6 = None
        self.WanVipv6 = None
        self.WanPortIpv6 = None
        self.WanStatusIpv6 = None
        self.DbEngine = None
        self.DbVersion = None
        self.DcnFlag = None
        self.DcnStatus = None
        self.DcnDstNum = None
        self.InstanceType = None
        self.ResourceTags = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.AppId = params.get("AppId")
        self.ProjectId = params.get("ProjectId")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Status = params.get("Status")
        self.Vip = params.get("Vip")
        self.Vport = params.get("Vport")
        self.WanDomain = params.get("WanDomain")
        self.WanVip = params.get("WanVip")
        self.WanPort = params.get("WanPort")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.Uin = params.get("Uin")
        self.TdsqlVersion = params.get("TdsqlVersion")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.UniqueVpcId = params.get("UniqueVpcId")
        self.UniqueSubnetId = params.get("UniqueSubnetId")
        self.OriginSerialId = params.get("OriginSerialId")
        self.NodeCount = params.get("NodeCount")
        self.IsTmp = params.get("IsTmp")
        self.ExclusterId = params.get("ExclusterId")
        self.Id = params.get("Id")
        self.Pid = params.get("Pid")
        self.Qps = params.get("Qps")
        self.Paymode = params.get("Paymode")
        self.Locker = params.get("Locker")
        self.StatusDesc = params.get("StatusDesc")
        self.WanStatus = params.get("WanStatus")
        self.IsAuditSupported = params.get("IsAuditSupported")
        self.Machine = params.get("Machine")
        self.IsEncryptSupported = params.get("IsEncryptSupported")
        self.Cpu = params.get("Cpu")
        self.Ipv6Flag = params.get("Ipv6Flag")
        self.Vipv6 = params.get("Vipv6")
        self.WanVipv6 = params.get("WanVipv6")
        self.WanPortIpv6 = params.get("WanPortIpv6")
        self.WanStatusIpv6 = params.get("WanStatusIpv6")
        self.DbEngine = params.get("DbEngine")
        self.DbVersion = params.get("DbVersion")
        self.DcnFlag = params.get("DcnFlag")
        self.DcnStatus = params.get("DcnStatus")
        self.DcnDstNum = params.get("DcnDstNum")
        self.InstanceType = params.get("InstanceType")
        if params.get("ResourceTags") is not None:
            self.ResourceTags = []
            for item in params.get("ResourceTags"):
                obj = ResourceTag()
                obj._deserialize(item)
                self.ResourceTags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DBParamValue(AbstractModel):
    """TencentDB parameter information.

    """

    def __init__(self):
        r"""
        :param Param: Parameter name
        :type Param: str
        :param Value: Parameter value
        :type Value: str
        """
        self.Param = None
        self.Value = None


    def _deserialize(self, params):
        self.Param = params.get("Param")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Database(AbstractModel):
    """Database information

    """

    def __init__(self):
        r"""
        :param DbName: Database name
        :type DbName: str
        """
        self.DbName = None


    def _deserialize(self, params):
        self.DbName = params.get("DbName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatabaseFunction(AbstractModel):
    """Database function information

    """

    def __init__(self):
        r"""
        :param Func: Function name
        :type Func: str
        """
        self.Func = None


    def _deserialize(self, params):
        self.Func = params.get("Func")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatabasePrivilege(AbstractModel):
    """Database permission

    """

    def __init__(self):
        r"""
        :param Privileges: Permission information
        :type Privileges: list of str
        :param Database: Database name
        :type Database: str
        """
        self.Privileges = None
        self.Database = None


    def _deserialize(self, params):
        self.Privileges = params.get("Privileges")
        self.Database = params.get("Database")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatabaseProcedure(AbstractModel):
    """Database stored procedure information

    """

    def __init__(self):
        r"""
        :param Proc: Stored procedure name
        :type Proc: str
        """
        self.Proc = None


    def _deserialize(self, params):
        self.Proc = params.get("Proc")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatabaseTable(AbstractModel):
    """Database table information

    """

    def __init__(self):
        r"""
        :param Table: Table name
        :type Table: str
        """
        self.Table = None


    def _deserialize(self, params):
        self.Table = params.get("Table")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatabaseView(AbstractModel):
    """Database view information

    """

    def __init__(self):
        r"""
        :param View: View name
        :type View: str
        """
        self.View = None


    def _deserialize(self, params):
        self.View = params.get("View")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DcnDetailItem(AbstractModel):
    """DCN details

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param InstanceName: Instance name
        :type InstanceName: str
        :param Region: Region where the instance resides
        :type Region: str
        :param Zone: Availability zone where the instance resides
        :type Zone: str
        :param Vip: Instance IP address
        :type Vip: str
        :param Vipv6: Instance IPv6 address
        :type Vipv6: str
        :param Vport: Instance port
        :type Vport: int
        :param Status: Instance status
        :type Status: int
        :param StatusDesc: Instance status description
        :type StatusDesc: str
        :param DcnFlag: DCN flag. Valid values: `1` (primary), `2` (disaster recovery)
        :type DcnFlag: int
        :param DcnStatus: DCN status. Valid values: `0` (none), `1` (creating), `2` (syncing), `3` (disconnected)
        :type DcnStatus: int
        :param Cpu: Number of CPU cores of the instance
        :type Cpu: int
        :param Memory: Instance memory capacity in GB
        :type Memory: int
        :param Storage: Instance storage capacity in GB
        :type Storage: int
        :param PayMode: Billing mode
        :type PayMode: int
        :param CreateTime: Creation time of the instance in the format of 2006-01-02 15:04:05
        :type CreateTime: str
        :param PeriodEndTime: Expiration time of the instance in the format of 2006-01-02 15:04:05
        :type PeriodEndTime: str
        :param InstanceType: Instance type. Valid values: `1` (dedicated primary instance), `2` (non-dedicated primary instance), `3` (non-dedicated disaster recovery instance), `4` (dedicated disaster recovery instance)
        :type InstanceType: int
        """
        self.InstanceId = None
        self.InstanceName = None
        self.Region = None
        self.Zone = None
        self.Vip = None
        self.Vipv6 = None
        self.Vport = None
        self.Status = None
        self.StatusDesc = None
        self.DcnFlag = None
        self.DcnStatus = None
        self.Cpu = None
        self.Memory = None
        self.Storage = None
        self.PayMode = None
        self.CreateTime = None
        self.PeriodEndTime = None
        self.InstanceType = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.Region = params.get("Region")
        self.Zone = params.get("Zone")
        self.Vip = params.get("Vip")
        self.Vipv6 = params.get("Vipv6")
        self.Vport = params.get("Vport")
        self.Status = params.get("Status")
        self.StatusDesc = params.get("StatusDesc")
        self.DcnFlag = params.get("DcnFlag")
        self.DcnStatus = params.get("DcnStatus")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Storage = params.get("Storage")
        self.PayMode = params.get("PayMode")
        self.CreateTime = params.get("CreateTime")
        self.PeriodEndTime = params.get("PeriodEndTime")
        self.InstanceType = params.get("InstanceType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAccountRequest(AbstractModel):
    """DeleteAccount request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param UserName: Username
        :type UserName: str
        :param Host: Access host allowed for user
        :type Host: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAccountResponse(AbstractModel):
    """DeleteAccount response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAccountPrivilegesRequest(AbstractModel):
    """DescribeAccountPrivileges request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param UserName: Login username.
        :type UserName: str
        :param Host: Access host allowed for user. An account is uniquely identified by username and host.
        :type Host: str
        :param DbName: Database name. `\*` indicates that global permissions will be queried (i.e., `\*.\*`), in which case the `Type` and `Object ` parameters will be ignored
        :type DbName: str
        :param Type: Type. Valid values: table, view, proc, func, \*. If `DbName` is a specific database name and `Type` is `\*`, the permissions of the database will be queried (i.e., `db.\*`), in which case the `Object` parameter will be ignored
        :type Type: str
        :param Object: Type name. For example, if `Type` is `table`, `Object` indicates a specific table name; if both `DbName` and `Type` are specific names, it indicates a specific object name and cannot be `\*` or empty
        :type Object: str
        :param ColName: If `Type` is `table` and `ColName` is `\*`, the permissions of the table will be queried; if `ColName` is a specific field name, the permissions of the corresponding field will be queried
        :type ColName: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.DbName = None
        self.Type = None
        self.Object = None
        self.ColName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.DbName = params.get("DbName")
        self.Type = params.get("Type")
        self.Object = params.get("Object")
        self.ColName = params.get("ColName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAccountPrivilegesResponse(AbstractModel):
    """DescribeAccountPrivileges response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param Privileges: Permission list.
        :type Privileges: list of str
        :param UserName: Database account username
        :type UserName: str
        :param Host: Database account host
        :type Host: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.Privileges = None
        self.UserName = None
        self.Host = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Privileges = params.get("Privileges")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.RequestId = params.get("RequestId")


class DescribeAccountsRequest(AbstractModel):
    """DescribeAccounts request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        """
        self.InstanceId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAccountsResponse(AbstractModel):
    """DescribeAccounts response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is passed through from the input parameters.
        :type InstanceId: str
        :param Users: Instance user list.
        :type Users: list of DBAccount
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.Users = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Users") is not None:
            self.Users = []
            for item in params.get("Users"):
                obj = DBAccount()
                obj._deserialize(item)
                self.Users.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBackupTimeRequest(AbstractModel):
    """DescribeBackupTime request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceIds: list of str
        """
        self.InstanceIds = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBackupTimeResponse(AbstractModel):
    """DescribeBackupTime response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of returned configurations
        :type TotalCount: int
        :param Items: Instance backup time configuration information
Note: this field may return null, indicating that no valid values can be obtained.
        :type Items: list of DBBackupTimeConfig
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Items = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Items") is not None:
            self.Items = []
            for item in params.get("Items"):
                obj = DBBackupTimeConfig()
                obj._deserialize(item)
                self.Items.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBInstancesRequest(AbstractModel):
    """DescribeDBInstances request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Queries by instance ID or IDs. Instance ID is in the format of `tdsql-ow728lmc`. Up to 100 instances can be queried in one request.
        :type InstanceIds: list of str
        :param SearchName: Search field name. Valid values: instancename (search by instance name), vip (search by private IP), all (search by instance ID, instance name, and private IP).
        :type SearchName: str
        :param SearchKey: Search keyword. Fuzzy search is supported. Multiple keywords should be separated by line breaks (`\n`).
        :type SearchKey: str
        :param ProjectIds: Queries by project ID
        :type ProjectIds: list of int
        :param IsFilterVpc: Whether to search by VPC
        :type IsFilterVpc: bool
        :param VpcId: VPC ID, which is valid when `IsFilterVpc` is 1
        :type VpcId: str
        :param SubnetId: VPC subnet ID, which is valid when `IsFilterVpc` is 1
        :type SubnetId: str
        :param OrderBy: Sort by field. Valid values: projectId, createtime, instancename
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values: desc, asc
        :type OrderByType: str
        :param Offset: Offset. Default value: 0
        :type Offset: int
        :param Limit: Number of results to be returned. Default value: 20. Maximum value: 100.
        :type Limit: int
        :param OriginSerialIds: Queries by `OriginSerialId`
        :type OriginSerialIds: list of str
        :param IsFilterExcluster: Identifies whether to use the `ExclusterType` field. false: no, true: yes
        :type IsFilterExcluster: bool
        :param ExclusterType: Instance cluster type. 1: non-dedicated cluster, 2: dedicated cluster, 0: all
        :type ExclusterType: int
        :param ExclusterIds: Filters instances by dedicated cluster ID in the format of `dbdc-4ih6uct9`
        :type ExclusterIds: list of str
        :param TagKeys: Tag key used in queries
        :type TagKeys: list of str
        :param FilterInstanceType: Instance types used in filtering. Valid values: 1 (dedicated instance), 2 (primary instance), 3 (disaster recovery instance). Multiple values should be separated by commas.
        :type FilterInstanceType: str
        :param Status: Use this filter to include instances in specific statuses
        :type Status: list of int
        :param ExcludeStatus: Use this filter to exclude instances in specific statuses
        :type ExcludeStatus: list of int
        """
        self.InstanceIds = None
        self.SearchName = None
        self.SearchKey = None
        self.ProjectIds = None
        self.IsFilterVpc = None
        self.VpcId = None
        self.SubnetId = None
        self.OrderBy = None
        self.OrderByType = None
        self.Offset = None
        self.Limit = None
        self.OriginSerialIds = None
        self.IsFilterExcluster = None
        self.ExclusterType = None
        self.ExclusterIds = None
        self.TagKeys = None
        self.FilterInstanceType = None
        self.Status = None
        self.ExcludeStatus = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.SearchName = params.get("SearchName")
        self.SearchKey = params.get("SearchKey")
        self.ProjectIds = params.get("ProjectIds")
        self.IsFilterVpc = params.get("IsFilterVpc")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OriginSerialIds = params.get("OriginSerialIds")
        self.IsFilterExcluster = params.get("IsFilterExcluster")
        self.ExclusterType = params.get("ExclusterType")
        self.ExclusterIds = params.get("ExclusterIds")
        self.TagKeys = params.get("TagKeys")
        self.FilterInstanceType = params.get("FilterInstanceType")
        self.Status = params.get("Status")
        self.ExcludeStatus = params.get("ExcludeStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBInstancesResponse(AbstractModel):
    """DescribeDBInstances response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Number of eligible instances
        :type TotalCount: int
        :param Instances: Instance details list
        :type Instances: list of DBInstance
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.Instances = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = DBInstance()
                obj._deserialize(item)
                self.Instances.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBLogFilesRequest(AbstractModel):
    """DescribeDBLogFiles request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param Type: Requested log type. Valid values: 1 (binlog), 2 (cold backup), 3 (errlog), 4 (slowlog).
        :type Type: int
        """
        self.InstanceId = None
        self.Type = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBLogFilesResponse(AbstractModel):
    """DescribeDBLogFiles response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param Type: Requested log type. Valid values: 1 (binlog), 2 (cold backup), 3 (errlog), 4 (slowlog).
        :type Type: int
        :param Total: Total number of requested logs
        :type Total: int
        :param Files: Information such as `uri`, `length`, and `mtime` (modification time)
        :type Files: list of LogFileInfo
        :param VpcPrefix: For an instance in a VPC, this prefix plus URI can be used as the download address
        :type VpcPrefix: str
        :param NormalPrefix: For an instance in a common network, this prefix plus URI can be used as the download address
        :type NormalPrefix: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.Type = None
        self.Total = None
        self.Files = None
        self.VpcPrefix = None
        self.NormalPrefix = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Type = params.get("Type")
        self.Total = params.get("Total")
        if params.get("Files") is not None:
            self.Files = []
            for item in params.get("Files"):
                obj = LogFileInfo()
                obj._deserialize(item)
                self.Files.append(obj)
        self.VpcPrefix = params.get("VpcPrefix")
        self.NormalPrefix = params.get("NormalPrefix")
        self.RequestId = params.get("RequestId")


class DescribeDBParametersRequest(AbstractModel):
    """DescribeDBParameters request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        """
        self.InstanceId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBParametersResponse(AbstractModel):
    """DescribeDBParameters response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param Params: Requests the current parameter values of database
        :type Params: list of ParamDesc
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.Params = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = ParamDesc()
                obj._deserialize(item)
                self.Params.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDBPerformanceDetailsRequest(AbstractModel):
    """DescribeDBPerformanceDetails request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param StartTime: Start date in the format of `yyyy-mm-dd`
        :type StartTime: str
        :param EndTime: End date in the format of `yyyy-mm-dd`
        :type EndTime: str
        :param MetricName: Name of pulled metric. Valid values: long_query, select_total, update_total, insert_total, delete_total, mem_hit_rate, disk_iops, conn_active, is_master_switched, slave_delay
        :type MetricName: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBPerformanceDetailsResponse(AbstractModel):
    """DescribeDBPerformanceDetails response structure.

    """

    def __init__(self):
        r"""
        :param Master: Master node performance monitoring data
        :type Master: :class:`tencentcloud.mariadb.v20170312.models.PerformanceMonitorSet`
        :param Slave1: Slave 1 performance monitoring data
Note: this field may return null, indicating that no valid values can be obtained.
        :type Slave1: :class:`tencentcloud.mariadb.v20170312.models.PerformanceMonitorSet`
        :param Slave2: Slave 2 performance monitoring data. If the instance is one-primary-one-secondary, it does not have this field
Note: this field may return null, indicating that no valid values can be obtained.
        :type Slave2: :class:`tencentcloud.mariadb.v20170312.models.PerformanceMonitorSet`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Master = None
        self.Slave1 = None
        self.Slave2 = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Master") is not None:
            self.Master = PerformanceMonitorSet()
            self.Master._deserialize(params.get("Master"))
        if params.get("Slave1") is not None:
            self.Slave1 = PerformanceMonitorSet()
            self.Slave1._deserialize(params.get("Slave1"))
        if params.get("Slave2") is not None:
            self.Slave2 = PerformanceMonitorSet()
            self.Slave2._deserialize(params.get("Slave2"))
        self.RequestId = params.get("RequestId")


class DescribeDBPerformanceRequest(AbstractModel):
    """DescribeDBPerformance request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param StartTime: Start date in the format of `yyyy-mm-dd`
        :type StartTime: str
        :param EndTime: End date in the format of `yyyy-mm-dd`
        :type EndTime: str
        :param MetricName: Name of pulled metric. Valid values: long_query, select_total, update_total, insert_total, delete_total, mem_hit_rate, disk_iops, conn_active, is_master_switched, slave_delay
        :type MetricName: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBPerformanceResponse(AbstractModel):
    """DescribeDBPerformance response structure.

    """

    def __init__(self):
        r"""
        :param LongQuery: Number of slow queries
        :type LongQuery: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param SelectTotal: Number of SELECT operations
        :type SelectTotal: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param UpdateTotal: Number of UPDATE operations
        :type UpdateTotal: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param InsertTotal: Number of INSERT operations
        :type InsertTotal: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param DeleteTotal: Number of DELETE operations
        :type DeleteTotal: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param MemHitRate: Cache hit rate
        :type MemHitRate: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param DiskIops: Number of disk IOs per second
        :type DiskIops: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param ConnActive: Number of active connections
        :type ConnActive: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param IsMasterSwitched: Whether primary/secondary switch occurred. 1: yes, 0: no
        :type IsMasterSwitched: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param SlaveDelay: primary/secondary delay
        :type SlaveDelay: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.LongQuery = None
        self.SelectTotal = None
        self.UpdateTotal = None
        self.InsertTotal = None
        self.DeleteTotal = None
        self.MemHitRate = None
        self.DiskIops = None
        self.ConnActive = None
        self.IsMasterSwitched = None
        self.SlaveDelay = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("LongQuery") is not None:
            self.LongQuery = MonitorData()
            self.LongQuery._deserialize(params.get("LongQuery"))
        if params.get("SelectTotal") is not None:
            self.SelectTotal = MonitorData()
            self.SelectTotal._deserialize(params.get("SelectTotal"))
        if params.get("UpdateTotal") is not None:
            self.UpdateTotal = MonitorData()
            self.UpdateTotal._deserialize(params.get("UpdateTotal"))
        if params.get("InsertTotal") is not None:
            self.InsertTotal = MonitorData()
            self.InsertTotal._deserialize(params.get("InsertTotal"))
        if params.get("DeleteTotal") is not None:
            self.DeleteTotal = MonitorData()
            self.DeleteTotal._deserialize(params.get("DeleteTotal"))
        if params.get("MemHitRate") is not None:
            self.MemHitRate = MonitorData()
            self.MemHitRate._deserialize(params.get("MemHitRate"))
        if params.get("DiskIops") is not None:
            self.DiskIops = MonitorData()
            self.DiskIops._deserialize(params.get("DiskIops"))
        if params.get("ConnActive") is not None:
            self.ConnActive = MonitorData()
            self.ConnActive._deserialize(params.get("ConnActive"))
        if params.get("IsMasterSwitched") is not None:
            self.IsMasterSwitched = MonitorData()
            self.IsMasterSwitched._deserialize(params.get("IsMasterSwitched"))
        if params.get("SlaveDelay") is not None:
            self.SlaveDelay = MonitorData()
            self.SlaveDelay._deserialize(params.get("SlaveDelay"))
        self.RequestId = params.get("RequestId")


class DescribeDBResourceUsageDetailsRequest(AbstractModel):
    """DescribeDBResourceUsageDetails request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param StartTime: Start date in the format of `yyyy-mm-dd`
        :type StartTime: str
        :param EndTime: End date in the format of `yyyy-mm-dd`
        :type EndTime: str
        :param MetricName: Name of pulled metric. Valid values: data_disk_available, binlog_disk_available, mem_available, cpu_usage_rate
        :type MetricName: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBResourceUsageDetailsResponse(AbstractModel):
    """DescribeDBResourceUsageDetails response structure.

    """

    def __init__(self):
        r"""
        :param Master: Master node resource usage monitoring node
        :type Master: :class:`tencentcloud.mariadb.v20170312.models.ResourceUsageMonitorSet`
        :param Slave1: Slave 1 resource usage monitoring node
Note: this field may return null, indicating that no valid values can be obtained.
        :type Slave1: :class:`tencentcloud.mariadb.v20170312.models.ResourceUsageMonitorSet`
        :param Slave2: Slave 2 resource usage monitoring node
Note: this field may return null, indicating that no valid values can be obtained.
        :type Slave2: :class:`tencentcloud.mariadb.v20170312.models.ResourceUsageMonitorSet`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Master = None
        self.Slave1 = None
        self.Slave2 = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Master") is not None:
            self.Master = ResourceUsageMonitorSet()
            self.Master._deserialize(params.get("Master"))
        if params.get("Slave1") is not None:
            self.Slave1 = ResourceUsageMonitorSet()
            self.Slave1._deserialize(params.get("Slave1"))
        if params.get("Slave2") is not None:
            self.Slave2 = ResourceUsageMonitorSet()
            self.Slave2._deserialize(params.get("Slave2"))
        self.RequestId = params.get("RequestId")


class DescribeDBResourceUsageRequest(AbstractModel):
    """DescribeDBResourceUsage request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param StartTime: Start date in the format of `yyyy-mm-dd`
        :type StartTime: str
        :param EndTime: End date in the format of `yyyy-mm-dd`
        :type EndTime: str
        :param MetricName: Name of pulled metric. Valid values: data_disk_available, binlog_disk_available, mem_available, cpu_usage_rate
        :type MetricName: str
        """
        self.InstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.MetricName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.MetricName = params.get("MetricName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBResourceUsageResponse(AbstractModel):
    """DescribeDBResourceUsage response structure.

    """

    def __init__(self):
        r"""
        :param BinlogDiskAvailable: Available capacity of binlog disk in GB
        :type BinlogDiskAvailable: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param DataDiskAvailable: Available disk capacity in GB
        :type DataDiskAvailable: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param CpuUsageRate: CPU utilization
        :type CpuUsageRate: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param MemAvailable: Available memory size in GB
        :type MemAvailable: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.BinlogDiskAvailable = None
        self.DataDiskAvailable = None
        self.CpuUsageRate = None
        self.MemAvailable = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("BinlogDiskAvailable") is not None:
            self.BinlogDiskAvailable = MonitorData()
            self.BinlogDiskAvailable._deserialize(params.get("BinlogDiskAvailable"))
        if params.get("DataDiskAvailable") is not None:
            self.DataDiskAvailable = MonitorData()
            self.DataDiskAvailable._deserialize(params.get("DataDiskAvailable"))
        if params.get("CpuUsageRate") is not None:
            self.CpuUsageRate = MonitorData()
            self.CpuUsageRate._deserialize(params.get("CpuUsageRate"))
        if params.get("MemAvailable") is not None:
            self.MemAvailable = MonitorData()
            self.MemAvailable._deserialize(params.get("MemAvailable"))
        self.RequestId = params.get("RequestId")


class DescribeDBSecurityGroupsRequest(AbstractModel):
    """DescribeDBSecurityGroups request structure.

    """

    def __init__(self):
        r"""
        :param Product: Database engine name. Valid value: `mariadb`.
        :type Product: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        """
        self.Product = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBSecurityGroupsResponse(AbstractModel):
    """DescribeDBSecurityGroups response structure.

    """

    def __init__(self):
        r"""
        :param Groups: Security group details
        :type Groups: list of SecurityGroup
        :param VIP: Instance VIP
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type VIP: str
        :param VPort: Instance port
Note: this field may return `null`, indicating that no valid values can be obtained.
        :type VPort: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Groups = None
        self.VIP = None
        self.VPort = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Groups") is not None:
            self.Groups = []
            for item in params.get("Groups"):
                obj = SecurityGroup()
                obj._deserialize(item)
                self.Groups.append(obj)
        self.VIP = params.get("VIP")
        self.VPort = params.get("VPort")
        self.RequestId = params.get("RequestId")


class DescribeDBSlowLogsRequest(AbstractModel):
    """DescribeDBSlowLogs request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param Offset: Data entry number starting from which to return results
        :type Offset: int
        :param Limit: Number of results to be returned
        :type Limit: int
        :param StartTime: Query start time in the format of `2016-07-23 14:55:20`
        :type StartTime: str
        :param EndTime: Query end time in the format of `2016-08-22 14:55:20`
        :type EndTime: str
        :param Db: Specific name of database to be queried
        :type Db: str
        :param OrderBy: Sort by metric. Valid values: query_time_sum, query_count
        :type OrderBy: str
        :param OrderByType: Sorting order. Valid values: desc, asc
        :type OrderByType: str
        :param Slave: Whether to query slow queries of the secondary. 0: primary, 1: secondary
        :type Slave: int
        """
        self.InstanceId = None
        self.Offset = None
        self.Limit = None
        self.StartTime = None
        self.EndTime = None
        self.Db = None
        self.OrderBy = None
        self.OrderByType = None
        self.Slave = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Db = params.get("Db")
        self.OrderBy = params.get("OrderBy")
        self.OrderByType = params.get("OrderByType")
        self.Slave = params.get("Slave")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDBSlowLogsResponse(AbstractModel):
    """DescribeDBSlowLogs response structure.

    """

    def __init__(self):
        r"""
        :param Data: Slow query log data
        :type Data: list of SlowLogData
        :param LockTimeSum: Sum of all statement lock durations
        :type LockTimeSum: float
        :param QueryCount: Total number of statement queries
        :type QueryCount: int
        :param Total: Total number of results
        :type Total: int
        :param QueryTimeSum: Sum of all statement query durations
        :type QueryTimeSum: float
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Data = None
        self.LockTimeSum = None
        self.QueryCount = None
        self.Total = None
        self.QueryTimeSum = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = SlowLogData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.LockTimeSum = params.get("LockTimeSum")
        self.QueryCount = params.get("QueryCount")
        self.Total = params.get("Total")
        self.QueryTimeSum = params.get("QueryTimeSum")
        self.RequestId = params.get("RequestId")


class DescribeDatabaseObjectsRequest(AbstractModel):
    """DescribeDatabaseObjects request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of dcdbt-ow7t8lmc.
        :type InstanceId: str
        :param DbName: Database name, which can be obtained through the `DescribeDatabases` API.
        :type DbName: str
        """
        self.InstanceId = None
        self.DbName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DbName = params.get("DbName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatabaseObjectsResponse(AbstractModel):
    """DescribeDatabaseObjects response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Passed through from the input parameters.
        :type InstanceId: str
        :param DbName: Database name.
        :type DbName: str
        :param Tables: List of tables.
        :type Tables: list of DatabaseTable
        :param Views: List of views.
        :type Views: list of DatabaseView
        :param Procs: List of stored procedures.
        :type Procs: list of DatabaseProcedure
        :param Funcs: List of functions.
        :type Funcs: list of DatabaseFunction
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.DbName = None
        self.Tables = None
        self.Views = None
        self.Procs = None
        self.Funcs = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DbName = params.get("DbName")
        if params.get("Tables") is not None:
            self.Tables = []
            for item in params.get("Tables"):
                obj = DatabaseTable()
                obj._deserialize(item)
                self.Tables.append(obj)
        if params.get("Views") is not None:
            self.Views = []
            for item in params.get("Views"):
                obj = DatabaseView()
                obj._deserialize(item)
                self.Views.append(obj)
        if params.get("Procs") is not None:
            self.Procs = []
            for item in params.get("Procs"):
                obj = DatabaseProcedure()
                obj._deserialize(item)
                self.Procs.append(obj)
        if params.get("Funcs") is not None:
            self.Funcs = []
            for item in params.get("Funcs"):
                obj = DatabaseFunction()
                obj._deserialize(item)
                self.Funcs.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDatabaseTableRequest(AbstractModel):
    """DescribeDatabaseTable request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of dcdbt-ow7t8lmc.
        :type InstanceId: str
        :param DbName: Database name, which can be obtained through the `DescribeDatabases` API.
        :type DbName: str
        :param Table: Table name, which can be obtained through the `DescribeDatabaseObjects` API.
        :type Table: str
        """
        self.InstanceId = None
        self.DbName = None
        self.Table = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DbName = params.get("DbName")
        self.Table = params.get("Table")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatabaseTableResponse(AbstractModel):
    """DescribeDatabaseTable response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance name.
        :type InstanceId: str
        :param DbName: Database name.
        :type DbName: str
        :param Table: Table name.
        :type Table: str
        :param Cols: Column information.
        :type Cols: list of TableColumn
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.DbName = None
        self.Table = None
        self.Cols = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DbName = params.get("DbName")
        self.Table = params.get("Table")
        if params.get("Cols") is not None:
            self.Cols = []
            for item in params.get("Cols"):
                obj = TableColumn()
                obj._deserialize(item)
                self.Cols.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDatabasesRequest(AbstractModel):
    """DescribeDatabases request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `dcdbt-ow7t8lmc`.
        :type InstanceId: str
        """
        self.InstanceId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatabasesResponse(AbstractModel):
    """DescribeDatabases response structure.

    """

    def __init__(self):
        r"""
        :param Databases: List of databases on instance.
        :type Databases: list of Database
        :param InstanceId: Passed through from the input parameters.
        :type InstanceId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Databases = None
        self.InstanceId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Databases") is not None:
            self.Databases = []
            for item in params.get("Databases"):
                obj = Database()
                obj._deserialize(item)
                self.Databases.append(obj)
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class DescribeDcnDetailRequest(AbstractModel):
    """DescribeDcnDetail request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        """
        self.InstanceId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDcnDetailResponse(AbstractModel):
    """DescribeDcnDetail response structure.

    """

    def __init__(self):
        r"""
        :param DcnDetails: DCN synchronization details
        :type DcnDetails: list of DcnDetailItem
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.DcnDetails = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DcnDetails") is not None:
            self.DcnDetails = []
            for item in params.get("DcnDetails"):
                obj = DcnDetailItem()
                obj._deserialize(item)
                self.DcnDetails.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeFileDownloadUrlRequest(AbstractModel):
    """DescribeFileDownloadUrl request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param FilePath: Unsigned file path
        :type FilePath: str
        """
        self.InstanceId = None
        self.FilePath = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.FilePath = params.get("FilePath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeFileDownloadUrlResponse(AbstractModel):
    """DescribeFileDownloadUrl response structure.

    """

    def __init__(self):
        r"""
        :param PreSignedUrl: Signed download URL
        :type PreSignedUrl: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.PreSignedUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        self.PreSignedUrl = params.get("PreSignedUrl")
        self.RequestId = params.get("RequestId")


class DescribeFlowRequest(AbstractModel):
    """DescribeFlow request structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Flow ID returned by async request API.
        :type FlowId: int
        """
        self.FlowId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeFlowResponse(AbstractModel):
    """DescribeFlow response structure.

    """

    def __init__(self):
        r"""
        :param Status: Flow status. 0: succeeded, 1: failed, 2: running
        :type Status: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DescribeInstanceNodeInfoRequest(AbstractModel):
    """DescribeInstanceNodeInfo request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, such as tdsql-6ltok4u9
        :type InstanceId: str
        :param Limit: The maximum number of results returned at a time. By default, there is no upper limit to this value, that is, all results can be returned.
        :type Limit: int
        :param Offset: Offset of the returned results. Default value: `0`.
        :type Offset: int
        """
        self.InstanceId = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstanceNodeInfoResponse(AbstractModel):
    """DescribeInstanceNodeInfo response structure.

    """

    def __init__(self):
        r"""
        :param TotalCount: Total number of nodes
        :type TotalCount: int
        :param NodesInfo: Node information
        :type NodesInfo: list of NodeInfo
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.TotalCount = None
        self.NodesInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("NodesInfo") is not None:
            self.NodesInfo = []
            for item in params.get("NodesInfo"):
                obj = NodeInfo()
                obj._deserialize(item)
                self.NodesInfo.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeLogFileRetentionPeriodRequest(AbstractModel):
    """DescribeLogFileRetentionPeriod request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        """
        self.InstanceId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLogFileRetentionPeriodResponse(AbstractModel):
    """DescribeLogFileRetentionPeriod response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param Days: Backup log retention days
        :type Days: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.Days = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Days = params.get("Days")
        self.RequestId = params.get("RequestId")


class DescribeProjectSecurityGroupsRequest(AbstractModel):
    """DescribeProjectSecurityGroups request structure.

    """

    def __init__(self):
        r"""
        :param Product: Database engine name. Valid value: `mariadb`.
        :type Product: str
        :param ProjectId: Project ID
        :type ProjectId: int
        """
        self.Product = None
        self.ProjectId = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.ProjectId = params.get("ProjectId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeProjectSecurityGroupsResponse(AbstractModel):
    """DescribeProjectSecurityGroups response structure.

    """

    def __init__(self):
        r"""
        :param Groups: Security group details
        :type Groups: list of SecurityGroup
        :param Total: Total number of security groups.
        :type Total: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Groups = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Groups") is not None:
            self.Groups = []
            for item in params.get("Groups"):
                obj = SecurityGroup()
                obj._deserialize(item)
                self.Groups.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DestroyHourDBInstanceRequest(AbstractModel):
    """DestroyHourDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of tdsql-avw0207d. It is the same as the instance ID displayed in the TencentDB console.
        :type InstanceId: str
        """
        self.InstanceId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DestroyHourDBInstanceResponse(AbstractModel):
    """DestroyHourDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID, which can be used in the [DescribeFlow](https://intl.cloud.tencent.com/document/product/237/16177?from_cn_redirect=1) API to query the async task result.
        :type FlowId: int
        :param InstanceId: Instance ID, which is the same as the request parameter `InstanceId`.
        :type InstanceId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.InstanceId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class DisassociateSecurityGroupsRequest(AbstractModel):
    """DisassociateSecurityGroups request structure.

    """

    def __init__(self):
        r"""
        :param Product: Database engine name. Valid value: `mariadb`.
        :type Product: str
        :param SecurityGroupId: Security group ID
        :type SecurityGroupId: str
        :param InstanceIds: Instance ID list, which is an array of one or more instance IDs.
        :type InstanceIds: list of str
        """
        self.Product = None
        self.SecurityGroupId = None
        self.InstanceIds = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisassociateSecurityGroupsResponse(AbstractModel):
    """DisassociateSecurityGroups response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class FunctionPrivilege(AbstractModel):
    """Function permission information

    """

    def __init__(self):
        r"""
        :param Database: Database name
        :type Database: str
        :param FunctionName: Function name
        :type FunctionName: str
        :param Privileges: Permission information
        :type Privileges: list of str
        """
        self.Database = None
        self.FunctionName = None
        self.Privileges = None


    def _deserialize(self, params):
        self.Database = params.get("Database")
        self.FunctionName = params.get("FunctionName")
        self.Privileges = params.get("Privileges")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GrantAccountPrivilegesRequest(AbstractModel):
    """GrantAccountPrivileges request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param UserName: Login username.
        :type UserName: str
        :param Host: Access host allowed for user. An account is uniquely identified by username and host.
        :type Host: str
        :param DbName: Database name. `\*` indicates that global permissions will be set (i.e., `\*.\*`), in which case the `Type` and `Object ` parameters will be ignored. If `DbName` is not `\*`, the input parameter `Type` is required.
        :type DbName: str
        :param Privileges: Global permission. Valid values: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`, `REFERENCES`, `INDEX`, `ALTER`, `CREATE TEMPORARY TABLES`, `LOCK TABLES`, `EXECUTE`, `CREATE VIEW`, `SHOW VIEW`, `CREATE ROUTINE`, `ALTER ROUTINE`, `EVENT`, `TRIGGER`, `SHOW DATABASES`, `REPLICATION CLIENT`, `REPLICATION SLAVE`. 
Database permission. Valid values: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`, `REFERENCES`, `INDEX`, `ALTER`, `CREATE TEMPORARY TABLES`, `LOCK TABLES`, `EXECUTE`, `CREATE VIEW`, `SHOW VIEW`, `CREATE ROUTINE`, `ALTER ROUTINE`, `EVENT`, `TRIGGER`. 
Table/View permission. Valid values: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`, `REFERENCES`, `INDEX`, `ALTER`, `CREATE VIEW`, `SHOW VIEW`, `TRIGGER`. 
Stored procedure/function permission. Valid values: `ALTER ROUTINE`, `EXECUTE`. 
Field permission. Valid values: `INSERT`, `REFERENCES`, `SELECT`, `UPDATE`.
        :type Privileges: list of str
        :param Type: Type. Valid values: table, view, proc, func, \*. If `DbName` is a specific database name and `Type` is `\*`, the permissions of the database will be set (i.e., `db.\*`), in which case the `Object` parameter will be ignored
        :type Type: str
        :param Object: Type name. For example, if `Type` is `table`, `Object` indicates a specific table name; if both `DbName` and `Type` are specific names, it indicates a specific object name and cannot be `\*` or empty
        :type Object: str
        :param ColName: If `Type` is `table` and `ColName` is `\*`, the permissions will be granted to the table; if `ColName` is a specific field name, the permissions will be granted to the field
        :type ColName: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.DbName = None
        self.Privileges = None
        self.Type = None
        self.Object = None
        self.ColName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.DbName = params.get("DbName")
        self.Privileges = params.get("Privileges")
        self.Type = params.get("Type")
        self.Object = params.get("Object")
        self.ColName = params.get("ColName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GrantAccountPrivilegesResponse(AbstractModel):
    """GrantAccountPrivileges response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InitDBInstancesRequest(AbstractModel):
    """InitDBInstances request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: List of IDs of instances to be initialized. The ID is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceIds: list of str
        :param Params: Parameter list. Valid values: character_set_server (character set; required); lower_case_table_names (table name case sensitivity; required; 0: case-sensitive, 1: case-insensitive); innodb_page_size (InnoDB data page; default size: 16 KB); sync_mode (sync mode; 0: async; 1: strong sync; 2: downgradable strong sync; default value: strong sync).
        :type Params: list of DBParamValue
        """
        self.InstanceIds = None
        self.Params = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = DBParamValue()
                obj._deserialize(item)
                self.Params.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InitDBInstancesResponse(AbstractModel):
    """InitDBInstances response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID. The task status can be queried through the `DescribeFlow` API.
        :type FlowId: int
        :param InstanceIds: Passed through from the input parameters.
        :type InstanceIds: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.InstanceIds = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.InstanceIds = params.get("InstanceIds")
        self.RequestId = params.get("RequestId")


class IsolateHourDBInstanceRequest(AbstractModel):
    """IsolateHourDBInstance request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: Instance ID list
        :type InstanceIds: list of str
        """
        self.InstanceIds = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IsolateHourDBInstanceResponse(AbstractModel):
    """IsolateHourDBInstance response structure.

    """

    def __init__(self):
        r"""
        :param SuccessInstanceIds: IDs of instances removed from isolation
        :type SuccessInstanceIds: list of str
        :param FailedInstanceIds: IDs of instances failed to be removed from isolation
        :type FailedInstanceIds: list of str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.SuccessInstanceIds = None
        self.FailedInstanceIds = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SuccessInstanceIds = params.get("SuccessInstanceIds")
        self.FailedInstanceIds = params.get("FailedInstanceIds")
        self.RequestId = params.get("RequestId")


class LogFileInfo(AbstractModel):
    """Pulled log information

    """

    def __init__(self):
        r"""
        :param Mtime: Last modified time of log
        :type Mtime: int
        :param Length: File length
        :type Length: int
        :param Uri: Uniform resource identifier (URI) used during log download
        :type Uri: str
        :param FileName: Filename
        :type FileName: str
        """
        self.Mtime = None
        self.Length = None
        self.Uri = None
        self.FileName = None


    def _deserialize(self, params):
        self.Mtime = params.get("Mtime")
        self.Length = params.get("Length")
        self.Uri = params.get("Uri")
        self.FileName = params.get("FileName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAccountDescriptionRequest(AbstractModel):
    """ModifyAccountDescription request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param UserName: Login username.
        :type UserName: str
        :param Host: Access host allowed for user. An account is uniquely identified by username and host.
        :type Host: str
        :param Description: New account remarks, which can contain 0-256 characters.
        :type Description: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.Description = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAccountDescriptionResponse(AbstractModel):
    """ModifyAccountDescription response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAccountPrivilegesRequest(AbstractModel):
    """ModifyAccountPrivileges request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of tdsql-c1nl9rpv. It is the same as the instance ID displayed in the TencentDB console.
        :type InstanceId: str
        :param Accounts: Database account, including username and host address.
        :type Accounts: list of Account
        :param GlobalPrivileges: Global permission. Valid values of `GlobalPrivileges`: `"SELECT"`, `"INSERT"`, `"UPDATE"`, `"DELETE"`, `"CREATE"`, `"PROCESS"`, `"DROP"`, `"REFERENCES"`, `"INDEX"`, `"ALTER"`, `"SHOW DATABASES"`, `"CREATE TEMPORARY TABLES"`, `"LOCK TABLES"`, `"EXECUTE"`, `"CREATE VIEW"`, `"SHOW VIEW"`, `"CREATE ROUTINE"`, `"ALTER ROUTINE"`, `"EVENT"`, `"TRIGGER"`.
Note: if the parameter is left empty, no change will be made to the granted global permissions. To clear the granted global permissions, set the parameter to an empty array.
        :type GlobalPrivileges: list of str
        :param DatabasePrivileges: Database permission. Valid values of `Privileges`: `"SELECT"`, `"INSERT"`, `"UPDATE"`, `"DELETE"`, `"CREATE"`, `"DROP"`, `"REFERENCES"`, `"INDEX"`, `"ALTER"`, `"CREATE TEMPORARY TABLES"`, `"LOCK TABLES"`, `"EXECUTE"`, `"CREATE VIEW"`, `"SHOW VIEW"`, `"CREATE ROUTINE"`, `"ALTER ROUTINE"`, `"EVENT"`, `"TRIGGER"`.
Note: if the parameter is left empty, no change will be made to the granted database permissions. To clear the granted database permissions, set `Privileges` to an empty array.
        :type DatabasePrivileges: list of DatabasePrivilege
        :param TablePrivileges: Database table permission. Valid values of `Privileges`: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`, `REFERENCES`, `INDEX`, `ALTER`, `CREATE VIEW`, `SHOW VIEW`, `TRIGGER`.
Note: if the parameter is not passed in, no change will be made to the granted table permissions. To clear the granted table permissions, set `Privileges` to an empty array.
        :type TablePrivileges: list of TablePrivilege
        :param ColumnPrivileges: Column permission. Valid values of `Privileges`: `"SELECT"`, `"INSERT"`, `"UPDATE"`, `"REFERENCES"`.
Note: if the parameter is left empty, no change will be made to the granted column permissions. To clear the granted column permissions, set `Privileges` to an empty array.
        :type ColumnPrivileges: list of ColumnPrivilege
        :param ViewPrivileges: Database view permission. Valid values of `Privileges`: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`, `REFERENCES`, `INDEX`, `ALTER`, `CREATE VIEW`, `SHOW VIEW`, `TRIGGER`.
Note: if the parameter is not passed in, no change will be made to the granted view permissions. To clear the granted view permissions, set `Privileges` to an empty array.
        :type ViewPrivileges: list of ViewPrivileges
        :param FunctionPrivileges: Database function permissions. Valid values of `Privileges`: `ALTER ROUTINE`, `EXECUTE`.
Note: if the parameter is not passed in, no change will be made to the granted function permissions. To clear the granted function permissions, set `Privileges` to an empty array.
        :type FunctionPrivileges: list of FunctionPrivilege
        :param ProcedurePrivileges: Database stored procedure permission. Valid values of `Privileges`: `ALTER ROUTINE`, `EXECUTE`.
Note: if the parameter is not passed in, no change will be made to the granted stored procedure permissions. To clear the granted stored procedure permissions, set `Privileges` to an empty array.
        :type ProcedurePrivileges: list of ProcedurePrivilege
        """
        self.InstanceId = None
        self.Accounts = None
        self.GlobalPrivileges = None
        self.DatabasePrivileges = None
        self.TablePrivileges = None
        self.ColumnPrivileges = None
        self.ViewPrivileges = None
        self.FunctionPrivileges = None
        self.ProcedurePrivileges = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Accounts") is not None:
            self.Accounts = []
            for item in params.get("Accounts"):
                obj = Account()
                obj._deserialize(item)
                self.Accounts.append(obj)
        self.GlobalPrivileges = params.get("GlobalPrivileges")
        if params.get("DatabasePrivileges") is not None:
            self.DatabasePrivileges = []
            for item in params.get("DatabasePrivileges"):
                obj = DatabasePrivilege()
                obj._deserialize(item)
                self.DatabasePrivileges.append(obj)
        if params.get("TablePrivileges") is not None:
            self.TablePrivileges = []
            for item in params.get("TablePrivileges"):
                obj = TablePrivilege()
                obj._deserialize(item)
                self.TablePrivileges.append(obj)
        if params.get("ColumnPrivileges") is not None:
            self.ColumnPrivileges = []
            for item in params.get("ColumnPrivileges"):
                obj = ColumnPrivilege()
                obj._deserialize(item)
                self.ColumnPrivileges.append(obj)
        if params.get("ViewPrivileges") is not None:
            self.ViewPrivileges = []
            for item in params.get("ViewPrivileges"):
                obj = ViewPrivileges()
                obj._deserialize(item)
                self.ViewPrivileges.append(obj)
        if params.get("FunctionPrivileges") is not None:
            self.FunctionPrivileges = []
            for item in params.get("FunctionPrivileges"):
                obj = FunctionPrivilege()
                obj._deserialize(item)
                self.FunctionPrivileges.append(obj)
        if params.get("ProcedurePrivileges") is not None:
            self.ProcedurePrivileges = []
            for item in params.get("ProcedurePrivileges"):
                obj = ProcedurePrivilege()
                obj._deserialize(item)
                self.ProcedurePrivileges.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAccountPrivilegesResponse(AbstractModel):
    """ModifyAccountPrivileges response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID, which can be used in the [DescribeFlow](https://intl.cloud.tencent.com/document/product/237/16177?from_cn_redirect=1) API to query the async task result.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ModifyBackupTimeRequest(AbstractModel):
    """ModifyBackupTime request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param StartBackupTime: Start time of daily backup window in the format of `mm:ss`, such as 22:00
        :type StartBackupTime: str
        :param EndBackupTime: End time of daily backup window in the format of `mm:ss`, such as 23:59
        :type EndBackupTime: str
        """
        self.InstanceId = None
        self.StartBackupTime = None
        self.EndBackupTime = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.StartBackupTime = params.get("StartBackupTime")
        self.EndBackupTime = params.get("EndBackupTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBackupTimeResponse(AbstractModel):
    """ModifyBackupTime response structure.

    """

    def __init__(self):
        r"""
        :param Status: Setting status. 0: success
        :type Status: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifyDBInstanceNameRequest(AbstractModel):
    """ModifyDBInstanceName request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: ID of instance to be modified, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param InstanceName: New name of instance, which can contain letters, digits, underscores, and hyphens.
        :type InstanceName: str
        """
        self.InstanceId = None
        self.InstanceName = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceNameResponse(AbstractModel):
    """ModifyDBInstanceName response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class ModifyDBInstanceSecurityGroupsRequest(AbstractModel):
    """ModifyDBInstanceSecurityGroups request structure.

    """

    def __init__(self):
        r"""
        :param Product: Database engine name. Valid value: `mariadb`.
        :type Product: str
        :param InstanceId: Instance ID
        :type InstanceId: str
        :param SecurityGroupIds: List of IDs of security groups to be modified, which is an array of one or more security group IDs.
        :type SecurityGroupIds: list of str
        """
        self.Product = None
        self.InstanceId = None
        self.SecurityGroupIds = None


    def _deserialize(self, params):
        self.Product = params.get("Product")
        self.InstanceId = params.get("InstanceId")
        self.SecurityGroupIds = params.get("SecurityGroupIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstanceSecurityGroupsResponse(AbstractModel):
    """ModifyDBInstanceSecurityGroups response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDBInstancesProjectRequest(AbstractModel):
    """ModifyDBInstancesProject request structure.

    """

    def __init__(self):
        r"""
        :param InstanceIds: List of IDs of instances to be modified. The ID is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceIds: list of str
        :param ProjectId: ID of the project to be assigned, which can be obtained through the `DescribeProjects` API.
        :type ProjectId: int
        """
        self.InstanceIds = None
        self.ProjectId = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        self.ProjectId = params.get("ProjectId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBInstancesProjectResponse(AbstractModel):
    """ModifyDBInstancesProject response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDBParametersRequest(AbstractModel):
    """ModifyDBParameters request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param Params: Parameter list. Each element is a combination of `Param` and `Value`.
        :type Params: list of DBParamValue
        """
        self.InstanceId = None
        self.Params = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Params") is not None:
            self.Params = []
            for item in params.get("Params"):
                obj = DBParamValue()
                obj._deserialize(item)
                self.Params.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBParametersResponse(AbstractModel):
    """ModifyDBParameters response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param Result: Parameter modification result
        :type Result: list of ParamModifyResult
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.Result = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("Result") is not None:
            self.Result = []
            for item in params.get("Result"):
                obj = ParamModifyResult()
                obj._deserialize(item)
                self.Result.append(obj)
        self.RequestId = params.get("RequestId")


class ModifyDBSyncModeRequest(AbstractModel):
    """ModifyDBSyncMode request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: ID of an instance for which to modify the sync mode. The ID is in the format of tdsql-ow728lmc.
        :type InstanceId: str
        :param SyncMode: Sync mode. Valid values: `0` (async), `1` (strong sync), `2` (downgradable strong sync).
        :type SyncMode: int
        """
        self.InstanceId = None
        self.SyncMode = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.SyncMode = params.get("SyncMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDBSyncModeResponse(AbstractModel):
    """ModifyDBSyncMode response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID. The task status can be queried through the `DescribeFlow` API.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ModifyLogFileRetentionPeriodRequest(AbstractModel):
    """ModifyLogFileRetentionPeriod request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param Days: Retention days up to 30
        :type Days: int
        """
        self.InstanceId = None
        self.Days = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Days = params.get("Days")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyLogFileRetentionPeriodResponse(AbstractModel):
    """ModifyLogFileRetentionPeriod response structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of `tdsql-ow728lmc`.
        :type InstanceId: str
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.InstanceId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.RequestId = params.get("RequestId")


class ModifySyncTaskAttributeRequest(AbstractModel):
    """ModifySyncTaskAttribute request structure.

    """

    def __init__(self):
        r"""
        :param TaskIds: IDs of tasks for which to modify the attributes. The IDs can be obtained by the return value of the `DescribeSyncTasks` API. Up to 100 tasks can be operated at a time.
        :type TaskIds: list of str
        :param TaskName: Task name. You can specify any name you like, but its length cannot exceed 100 characters.
        :type TaskName: str
        """
        self.TaskIds = None
        self.TaskName = None


    def _deserialize(self, params):
        self.TaskIds = params.get("TaskIds")
        self.TaskName = params.get("TaskName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySyncTaskAttributeResponse(AbstractModel):
    """ModifySyncTaskAttribute response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class MonitorData(AbstractModel):
    """Monitoring data

    """

    def __init__(self):
        r"""
        :param StartTime: Start time in the format of `2018-03-24 23:59:59`
        :type StartTime: str
        :param EndTime: End time in the format of `2018-03-24 23:59:59`
        :type EndTime: str
        :param Data: Monitoring data
        :type Data: list of float
        """
        self.StartTime = None
        self.EndTime = None
        self.Data = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Data = params.get("Data")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NodeInfo(AbstractModel):
    """Instance node information

    """

    def __init__(self):
        r"""
        :param NodeId: Node ID
        :type NodeId: str
        :param Role: Node role. Valid values: `master`, `slave`
        :type Role: str
        """
        self.NodeId = None
        self.Role = None


    def _deserialize(self, params):
        self.NodeId = params.get("NodeId")
        self.Role = params.get("Role")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OpenDBExtranetAccessRequest(AbstractModel):
    """OpenDBExtranetAccess request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: ID of instance for which to enable public network access. The ID is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param Ipv6Flag: Whether IPv6 is used. Default value: 0
        :type Ipv6Flag: int
        """
        self.InstanceId = None
        self.Ipv6Flag = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Ipv6Flag = params.get("Ipv6Flag")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OpenDBExtranetAccessResponse(AbstractModel):
    """OpenDBExtranetAccess response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID. The task status can be queried through the `DescribeFlow` API.
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class ParamConstraint(AbstractModel):
    """Parameter constraint

    """

    def __init__(self):
        r"""
        :param Type: Constraint type, such as `enum` and `section`
        :type Type: str
        :param Enum: List of valid values when constraint type is `enum`
        :type Enum: str
        :param Range: Range when constraint type is `section`
Note: this field may return null, indicating that no valid values can be obtained.
        :type Range: :class:`tencentcloud.mariadb.v20170312.models.ConstraintRange`
        :param String: List of valid values when constraint type is `string`
        :type String: str
        """
        self.Type = None
        self.Enum = None
        self.Range = None
        self.String = None


    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.Enum = params.get("Enum")
        if params.get("Range") is not None:
            self.Range = ConstraintRange()
            self.Range._deserialize(params.get("Range"))
        self.String = params.get("String")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ParamDesc(AbstractModel):
    """Database parameter description

    """

    def __init__(self):
        r"""
        :param Param: Parameter name
        :type Param: str
        :param Value: Current parameter value
        :type Value: str
        :param SetValue: Previously set value, which is the same as `value` after the parameter takes effect.
Note: this field may return null, indicating that no valid values can be obtained.
        :type SetValue: str
        :param Default: Default value
        :type Default: str
        :param Constraint: Parameter constraint
        :type Constraint: :class:`tencentcloud.mariadb.v20170312.models.ParamConstraint`
        :param HaveSetValue: Whether a value has been set. false: no, true: yes
        :type HaveSetValue: bool
        """
        self.Param = None
        self.Value = None
        self.SetValue = None
        self.Default = None
        self.Constraint = None
        self.HaveSetValue = None


    def _deserialize(self, params):
        self.Param = params.get("Param")
        self.Value = params.get("Value")
        self.SetValue = params.get("SetValue")
        self.Default = params.get("Default")
        if params.get("Constraint") is not None:
            self.Constraint = ParamConstraint()
            self.Constraint._deserialize(params.get("Constraint"))
        self.HaveSetValue = params.get("HaveSetValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ParamModifyResult(AbstractModel):
    """Parameter modification result

    """

    def __init__(self):
        r"""
        :param Param: Renames a parameter
        :type Param: str
        :param Code: Result of parameter modification. 0: success, -1: failure, -2: invalid parameter value
        :type Code: int
        """
        self.Param = None
        self.Code = None


    def _deserialize(self, params):
        self.Param = params.get("Param")
        self.Code = params.get("Code")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PerformanceMonitorSet(AbstractModel):
    """Set of database performance monitoring metrics

    """

    def __init__(self):
        r"""
        :param UpdateTotal: Number of UPDATE operations
        :type UpdateTotal: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param DiskIops: Number of disk IOs per second
        :type DiskIops: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param ConnActive: Number of active connections
        :type ConnActive: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param MemHitRate: Cache hit rate
        :type MemHitRate: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param SlaveDelay: Primary/Secondary delay
        :type SlaveDelay: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param SelectTotal: Number of SELECT operations
        :type SelectTotal: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param LongQuery: Number of slow queries
        :type LongQuery: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param DeleteTotal: Number of DELETE operations
        :type DeleteTotal: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param InsertTotal: Number of INSERT operations
        :type InsertTotal: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param IsMasterSwitched: Whether primary/Secondary switch occurred. 1: yes, 0: no
        :type IsMasterSwitched: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        """
        self.UpdateTotal = None
        self.DiskIops = None
        self.ConnActive = None
        self.MemHitRate = None
        self.SlaveDelay = None
        self.SelectTotal = None
        self.LongQuery = None
        self.DeleteTotal = None
        self.InsertTotal = None
        self.IsMasterSwitched = None


    def _deserialize(self, params):
        if params.get("UpdateTotal") is not None:
            self.UpdateTotal = MonitorData()
            self.UpdateTotal._deserialize(params.get("UpdateTotal"))
        if params.get("DiskIops") is not None:
            self.DiskIops = MonitorData()
            self.DiskIops._deserialize(params.get("DiskIops"))
        if params.get("ConnActive") is not None:
            self.ConnActive = MonitorData()
            self.ConnActive._deserialize(params.get("ConnActive"))
        if params.get("MemHitRate") is not None:
            self.MemHitRate = MonitorData()
            self.MemHitRate._deserialize(params.get("MemHitRate"))
        if params.get("SlaveDelay") is not None:
            self.SlaveDelay = MonitorData()
            self.SlaveDelay._deserialize(params.get("SlaveDelay"))
        if params.get("SelectTotal") is not None:
            self.SelectTotal = MonitorData()
            self.SelectTotal._deserialize(params.get("SelectTotal"))
        if params.get("LongQuery") is not None:
            self.LongQuery = MonitorData()
            self.LongQuery._deserialize(params.get("LongQuery"))
        if params.get("DeleteTotal") is not None:
            self.DeleteTotal = MonitorData()
            self.DeleteTotal._deserialize(params.get("DeleteTotal"))
        if params.get("InsertTotal") is not None:
            self.InsertTotal = MonitorData()
            self.InsertTotal._deserialize(params.get("InsertTotal"))
        if params.get("IsMasterSwitched") is not None:
            self.IsMasterSwitched = MonitorData()
            self.IsMasterSwitched._deserialize(params.get("IsMasterSwitched"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ProcedurePrivilege(AbstractModel):
    """Stored procedure permission information

    """

    def __init__(self):
        r"""
        :param Database: Database name
        :type Database: str
        :param Procedure: Stored procedure name
        :type Procedure: str
        :param Privileges: Permission information
        :type Privileges: list of str
        """
        self.Database = None
        self.Procedure = None
        self.Privileges = None


    def _deserialize(self, params):
        self.Database = params.get("Database")
        self.Procedure = params.get("Procedure")
        self.Privileges = params.get("Privileges")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResetAccountPasswordRequest(AbstractModel):
    """ResetAccountPassword request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID, which is in the format of `tdsql-ow728lmc` and can be obtained through the `DescribeDBInstances` API.
        :type InstanceId: str
        :param UserName: Login username.
        :type UserName: str
        :param Host: Access host allowed for user. An account is uniquely identified by username and host.
        :type Host: str
        :param Password: New password, which can contain 6-32 letters, digits, and common symbols but not semicolons, single quotation marks, and double quotation marks.
        :type Password: str
        """
        self.InstanceId = None
        self.UserName = None
        self.Host = None
        self.Password = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.UserName = params.get("UserName")
        self.Host = params.get("Host")
        self.Password = params.get("Password")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResetAccountPasswordResponse(AbstractModel):
    """ResetAccountPassword response structure.

    """

    def __init__(self):
        r"""
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResourceTag(AbstractModel):
    """Tag object, including tag key and tag value

    """

    def __init__(self):
        r"""
        :param TagKey: Tag key
        :type TagKey: str
        :param TagValue: Tag value
        :type TagValue: str
        """
        self.TagKey = None
        self.TagValue = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValue = params.get("TagValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResourceUsageMonitorSet(AbstractModel):
    """Set of database resource usage monitoring metrics

    """

    def __init__(self):
        r"""
        :param BinlogDiskAvailable: Available capacity of binlog disk in GB
        :type BinlogDiskAvailable: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param CpuUsageRate: CPU utilization
        :type CpuUsageRate: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param MemAvailable: Available memory size in GB
        :type MemAvailable: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        :param DataDiskAvailable: Available disk capacity in GB
        :type DataDiskAvailable: :class:`tencentcloud.mariadb.v20170312.models.MonitorData`
        """
        self.BinlogDiskAvailable = None
        self.CpuUsageRate = None
        self.MemAvailable = None
        self.DataDiskAvailable = None


    def _deserialize(self, params):
        if params.get("BinlogDiskAvailable") is not None:
            self.BinlogDiskAvailable = MonitorData()
            self.BinlogDiskAvailable._deserialize(params.get("BinlogDiskAvailable"))
        if params.get("CpuUsageRate") is not None:
            self.CpuUsageRate = MonitorData()
            self.CpuUsageRate._deserialize(params.get("CpuUsageRate"))
        if params.get("MemAvailable") is not None:
            self.MemAvailable = MonitorData()
            self.MemAvailable._deserialize(params.get("MemAvailable"))
        if params.get("DataDiskAvailable") is not None:
            self.DataDiskAvailable = MonitorData()
            self.DataDiskAvailable._deserialize(params.get("DataDiskAvailable"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SecurityGroup(AbstractModel):
    """Security group details

    """

    def __init__(self):
        r"""
        :param ProjectId: Project ID
        :type ProjectId: int
        :param CreateTime: Creation time in the format of yyyy-mm-dd hh:mm:ss
        :type CreateTime: str
        :param SecurityGroupId: Security group ID
        :type SecurityGroupId: str
        :param SecurityGroupName: Security group name
        :type SecurityGroupName: str
        :param SecurityGroupRemark: Security group remarks
        :type SecurityGroupRemark: str
        :param Inbound: Inbound rule
        :type Inbound: list of SecurityGroupBound
        :param Outbound: Outbound rule
        :type Outbound: list of SecurityGroupBound
        """
        self.ProjectId = None
        self.CreateTime = None
        self.SecurityGroupId = None
        self.SecurityGroupName = None
        self.SecurityGroupRemark = None
        self.Inbound = None
        self.Outbound = None


    def _deserialize(self, params):
        self.ProjectId = params.get("ProjectId")
        self.CreateTime = params.get("CreateTime")
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.SecurityGroupName = params.get("SecurityGroupName")
        self.SecurityGroupRemark = params.get("SecurityGroupRemark")
        if params.get("Inbound") is not None:
            self.Inbound = []
            for item in params.get("Inbound"):
                obj = SecurityGroupBound()
                obj._deserialize(item)
                self.Inbound.append(obj)
        if params.get("Outbound") is not None:
            self.Outbound = []
            for item in params.get("Outbound"):
                obj = SecurityGroupBound()
                obj._deserialize(item)
                self.Outbound.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SecurityGroupBound(AbstractModel):
    """Security group inbound/outbound rule

    """

    def __init__(self):
        r"""
        :param Action: Policy, which can be `ACCEPT` or `DROP`
        :type Action: str
        :param CidrIp: Source IP or source IP range, such as 192.168.0.0/16
        :type CidrIp: str
        :param PortRange: Port
        :type PortRange: str
        :param IpProtocol: Network protocol. UDP and TCP are supported.
        :type IpProtocol: str
        """
        self.Action = None
        self.CidrIp = None
        self.PortRange = None
        self.IpProtocol = None


    def _deserialize(self, params):
        self.Action = params.get("Action")
        self.CidrIp = params.get("CidrIp")
        self.PortRange = params.get("PortRange")
        self.IpProtocol = params.get("IpProtocol")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SlowLogData(AbstractModel):
    """Slow query entry information

    """

    def __init__(self):
        r"""
        :param CheckSum: Statement checksum for querying details
        :type CheckSum: str
        :param Db: Database name
        :type Db: str
        :param FingerPrint: Abstracted SQL statement
        :type FingerPrint: str
        :param LockTimeAvg: Average lock duration
        :type LockTimeAvg: str
        :param LockTimeMax: Maximum lock duration
        :type LockTimeMax: str
        :param LockTimeMin: Minimum lock duration
        :type LockTimeMin: str
        :param LockTimeSum: Sum of lock durations
        :type LockTimeSum: str
        :param QueryCount: Number of queries
        :type QueryCount: str
        :param QueryTimeAvg: Average query duration
        :type QueryTimeAvg: str
        :param QueryTimeMax: Maximum query duration
        :type QueryTimeMax: str
        :param QueryTimeMin: Minimum query duration
        :type QueryTimeMin: str
        :param QueryTimeSum: Sum of query durations
        :type QueryTimeSum: str
        :param RowsExaminedSum: Number of scanned rows
        :type RowsExaminedSum: str
        :param RowsSentSum: Number of sent rows
        :type RowsSentSum: str
        :param TsMax: Last execution time
        :type TsMax: str
        :param TsMin: First execution time
        :type TsMin: str
        :param User: Account
        :type User: str
        :param ExampleSql: Sample SQL
Note: this field may return null, indicating that no valid values can be obtained.
        :type ExampleSql: str
        :param Host: Host address of the account
        :type Host: str
        """
        self.CheckSum = None
        self.Db = None
        self.FingerPrint = None
        self.LockTimeAvg = None
        self.LockTimeMax = None
        self.LockTimeMin = None
        self.LockTimeSum = None
        self.QueryCount = None
        self.QueryTimeAvg = None
        self.QueryTimeMax = None
        self.QueryTimeMin = None
        self.QueryTimeSum = None
        self.RowsExaminedSum = None
        self.RowsSentSum = None
        self.TsMax = None
        self.TsMin = None
        self.User = None
        self.ExampleSql = None
        self.Host = None


    def _deserialize(self, params):
        self.CheckSum = params.get("CheckSum")
        self.Db = params.get("Db")
        self.FingerPrint = params.get("FingerPrint")
        self.LockTimeAvg = params.get("LockTimeAvg")
        self.LockTimeMax = params.get("LockTimeMax")
        self.LockTimeMin = params.get("LockTimeMin")
        self.LockTimeSum = params.get("LockTimeSum")
        self.QueryCount = params.get("QueryCount")
        self.QueryTimeAvg = params.get("QueryTimeAvg")
        self.QueryTimeMax = params.get("QueryTimeMax")
        self.QueryTimeMin = params.get("QueryTimeMin")
        self.QueryTimeSum = params.get("QueryTimeSum")
        self.RowsExaminedSum = params.get("RowsExaminedSum")
        self.RowsSentSum = params.get("RowsSentSum")
        self.TsMax = params.get("TsMax")
        self.TsMin = params.get("TsMin")
        self.User = params.get("User")
        self.ExampleSql = params.get("ExampleSql")
        self.Host = params.get("Host")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SwitchDBInstanceHARequest(AbstractModel):
    """SwitchDBInstanceHA request structure.

    """

    def __init__(self):
        r"""
        :param InstanceId: Instance ID in the format of tdsql-ow728lmc
        :type InstanceId: str
        :param Zone: Target AZ. The node with the lowest delay in the target AZ will be automatically promoted to primary node.
        :type Zone: str
        """
        self.InstanceId = None
        self.Zone = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.Zone = params.get("Zone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SwitchDBInstanceHAResponse(AbstractModel):
    """SwitchDBInstanceHA response structure.

    """

    def __init__(self):
        r"""
        :param FlowId: Async task ID
        :type FlowId: int
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self.FlowId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowId = params.get("FlowId")
        self.RequestId = params.get("RequestId")


class TableColumn(AbstractModel):
    """Database column information

    """

    def __init__(self):
        r"""
        :param Col: Column name
        :type Col: str
        :param Type: Column type
        :type Type: str
        """
        self.Col = None
        self.Type = None


    def _deserialize(self, params):
        self.Col = params.get("Col")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TablePrivilege(AbstractModel):
    """Table permission

    """

    def __init__(self):
        r"""
        :param Database: Database name
        :type Database: str
        :param Table: Table name
        :type Table: str
        :param Privileges: Permission information
        :type Privileges: list of str
        """
        self.Database = None
        self.Table = None
        self.Privileges = None


    def _deserialize(self, params):
        self.Database = params.get("Database")
        self.Table = params.get("Table")
        self.Privileges = params.get("Privileges")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ViewPrivileges(AbstractModel):
    """View permission information

    """

    def __init__(self):
        r"""
        :param Database: Database name
        :type Database: str
        :param View: View name
        :type View: str
        :param Privileges: Permission information
        :type Privileges: list of str
        """
        self.Database = None
        self.View = None
        self.Privileges = None


    def _deserialize(self, params):
        self.Database = params.get("Database")
        self.View = params.get("View")
        self.Privileges = params.get("Privileges")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        