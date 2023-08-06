from sqlalchemy import BigInteger, Boolean, Column, DECIMAL, DateTime, Float, ForeignKey, ForeignKeyConstraint, \
    Identity, Index, Integer, PrimaryKeyConstraint, String, TEXT, Table, Unicode, text
from sqlalchemy.dialects.mssql import DATETIME2, NTEXT, TINYINT, UNIQUEIDENTIFIER
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import NullType

Base = declarative_base()
metadata = Base.metadata


class AssetComponentType(Base):
    __tablename__ = 'AssetComponentType'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_AssetComponentType'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Name = Column(Unicode, nullable=False)
    Description = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)


class AssetGroup(Base):
    __tablename__ = 'AssetGroup'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_AssetGroup'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    OrganisationId = Column(Unicode, nullable=False)
    Name = Column(Unicode, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    Description = Column(Unicode)

    AssetGroupType = relationship('AssetGroupType', back_populates='AssetGroup')


class AssetType(Base):
    __tablename__ = 'AssetType'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_AssetType'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Name = Column(Unicode, nullable=False)
    OrganisationId = Column(Unicode, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    BuildingComponent = Column(Integer, nullable=False, server_default=text('((0))'))
    Description = Column(Unicode)

    Asset = relationship('Asset', back_populates='AssetType')
    AssetComponent = relationship('AssetComponent', back_populates='AssetType')
    AssetGroupType = relationship('AssetGroupType', back_populates='AssetType')
    AssetTypeClassification = relationship('AssetTypeClassification', back_populates='AssetType')


class AuditMethod(Base):
    __tablename__ = 'AuditMethod'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_AuditMethod'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Name = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    Description = Column(Unicode)

    AssetAudit = relationship('AssetAudit', back_populates='AuditMethod')


class AuditWeighting(Base):
    __tablename__ = 'AuditWeighting'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_AuditWeighting'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    WeightingGroup = Column(Integer, nullable=False)
    WeightingKey = Column(Integer, nullable=False)
    WeightingValue = Column(Float(53), nullable=False)
    OrganisationId = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    UpdatedBy = Column(Unicode, nullable=False)
    UpdatedDate = Column(DATETIME2, nullable=False)


class BuildingElementFunction(Base):
    __tablename__ = 'BuildingElementFunction'
    __table_args__ = (
        PrimaryKeyConstraint('Guid', name='PK_BuildingElementFunction'),
    )

    Guid = Column(UNIQUEIDENTIFIER)
    BuildingElementType = Column(Unicode, nullable=False, server_default=text("(N'UNKNOWN')"))
    BuildingElementGuid = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Unicode, nullable=False)
    PredefinedName = Column(Unicode, nullable=False, server_default=text("(N'USERDEFINED')"))
    Status = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(1)))'))
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    OrganisationId = Column(Unicode(50), nullable=False)
    UserDefinedName = Column(Unicode)
    Value = Column(Unicode)
    Remarks = Column(Unicode)


class Comment(Base):
    __tablename__ = 'Comment'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_Comment'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    UserGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    ParentType = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    ParentReference = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    ContentType = Column(String(20, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    Content = Column(String(collation='SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    StatusId = Column(Integer, nullable=False, server_default=text('((1))'))
    UpdatedDate = Column(DATETIME2, nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    SubReference = Column(Unicode)
    SubType = Column(Unicode)
    ProjectGuid = Column(Unicode)


class CommonDataEnvironmentRecord(Base):
    __tablename__ = 'CommonDataEnvironmentRecord'
    __table_args__ = (
        PrimaryKeyConstraint('AttachedComponent', 'ComponentId', 'Variable', 'Value', name='PK_CommonDataEnvironmentRecord'),
    )

    Variable = Column(Unicode(450), nullable=False)
    AttachedComponent = Column(Unicode(25), nullable=False, server_default=text("(N'Phase')"))
    Value = Column(Unicode(100), nullable=False)
    LastUpdated = Column(DateTime, nullable=False, server_default=text('(getdate())'))
    ComponentId = Column(Unicode(100), nullable=False, server_default=text("(N'')"))


class ContactType(Base):
    __tablename__ = 'ContactType'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_ContactType'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    OrganisationId = Column(Unicode, nullable=False)
    Name = Column(Unicode, nullable=False)
    Definition = Column(NTEXT(1073741823))

    Contact = relationship('Contact', back_populates='ContactType')
    ContactTypeProperty = relationship('ContactTypeProperty', back_populates='ContactType')


class Email(Base):
    __tablename__ = 'Email'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_Email'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ContactId = Column(UNIQUEIDENTIFIER, nullable=False, index=True)
    EmailType = Column(Integer, nullable=False)
    EmailAddress = Column(Unicode, nullable=False)
    Primary = Column(Integer, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    UpdatedBy = Column(Unicode)


class File(Base):
    __tablename__ = 'File'
    __table_args__ = (
        PrimaryKeyConstraint('Guid', name='PK_File'),
    )

    Guid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    UserGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    FileName = Column(String(120, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    FileType = Column(String(20, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    Location = Column(String(collation='SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    FileSize = Column(Integer, nullable=False)
    Status = Column(Integer, nullable=False)
    UpdatedDate = Column(DATETIME2, nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    MimeType = Column(String(20, 'SQL_Latin1_General_CP1_CS_AS'))
    Description = Column(String(collation='SQL_Latin1_General_CP1_CS_AS'))

    FileUsage = relationship('FileUsage', back_populates='File')


class FileCapRecord(Base):
    __tablename__ = 'FileCapRecord'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_FileCapRecord'),
    )

    Id = Column(Unicode(450))
    FileName = Column(Unicode(450), nullable=False)
    CreatedDate = Column(DateTime, nullable=False, server_default=text('(getdate())'))
    CreatedUserId = Column(Unicode(450), nullable=False)
    CurrentVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    LastUpdatedDate = Column(DateTime, server_default=text('(getdate())'))
    LastUpdatedByUserId = Column(Unicode(450))
    Remarks = Column(Unicode)

    Project = relationship('Project', secondary='ProjectCap', back_populates='FileCapRecord')
    FileCapRecordLibraryItem = relationship('FileCapRecordLibraryItem', back_populates='FileCapRecord')
    CapExecutionHistory = relationship('CapExecutionHistory', back_populates='FileCapRecord')
    CapExecutionHistoryDependency = relationship('CapExecutionHistoryDependency', back_populates='FileCapRecord')


class FileLrmlRecord(Base):
    __tablename__ = 'FileLrmlRecord'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_FileLrmlRecord'),
    )

    Id = Column(Unicode(450))
    FileName = Column(Unicode(450), nullable=False)
    CreatedDate = Column(DateTime, nullable=False, server_default=text('(getdate())'))
    CreatedUserId = Column(Unicode(450), nullable=False)
    LastUpdatedDate = Column(DateTime, server_default=text('(getdate())'))
    LastUpdatedByUserId = Column(Unicode(450))
    Remarks = Column(Unicode)


class FileUsageDocumentType(Base):
    __tablename__ = 'FileUsageDocumentType'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_FileUsageDocumentType'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Status = Column(Integer, nullable=False, server_default=text('((1))'))
    OrganisationId = Column(Unicode)
    Name = Column(Unicode)

    FileUsageDocumentTypeFile = relationship('FileUsageDocumentTypeFile', back_populates='FileUsageDocumentType')


class FinOrganisation(Base):
    __tablename__ = 'FinOrganisation'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_FinOrganisation'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    OrganisationId = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    Enable = Column(Integer, nullable=False, server_default=text('((0))'))
    CreatedDate = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    UpdatedDate = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    BillStartNumber = Column(Integer, nullable=False, server_default=text('((0))'))
    InvoiceStartNumber = Column(Integer, nullable=False, server_default=text('((0))'))
    JournalStartNumber = Column(Integer, nullable=False, server_default=text('((0))'))
    PurchaseOrderStartNumber = Column(Integer, nullable=False, server_default=text('((0))'))
    QuoteStartNumber = Column(Integer, nullable=False, server_default=text('((0))'))
    ReportingPeriod = Column(Integer)
    DefaultPaymentPeriodValue = Column(Integer)
    DefaultCurrency = Column(Integer)
    ReportingPeriodStartDate = Column(DATETIME2)
    CreatedBy = Column(Unicode)
    UpdatedBy = Column(Unicode)
    DefaultTax = Column(Integer)
    DefaultPaymentPeriodInterval = Column(Unicode)
    ContingencyFundAccountId = Column(Integer)
    RentPaymentAccountId = Column(Integer)
    RentIncomeAccountId = Column(Integer)
    MaintenanceItems = Column(Integer)

    FinAccountClass = relationship('FinAccountClass', back_populates='FinOrganisation')
    FinAccount = relationship('FinAccount', back_populates='FinOrganisation')
    FinTransactionGroup = relationship('FinTransactionGroup', back_populates='FinOrganisation')
    FinAccountAnnualRecord = relationship('FinAccountAnnualRecord', back_populates='FinOrganisation')
    FinAdditionalProperties = relationship('FinAdditionalProperties', back_populates='FinOrganisation')
    FinBudget = relationship('FinBudget', back_populates='FinOrganisation')
    LineItem = relationship('LineItem', back_populates='FinOrganisation')
    FinTransaction = relationship('FinTransaction', back_populates='FinOrganisation')


class HealthAndSafetyPermit(Base):
    __tablename__ = 'HealthAndSafetyPermit'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_HealthAndSafetyPermit'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    PermitNumber = Column(Unicode, nullable=False)
    WorkOrderGuid = Column(Unicode(80), nullable=False, index=True)
    Status = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    ContactId = Column(Integer, index=True)
    IssuerId = Column(Unicode)
    PreparerId = Column(Unicode)

    HealthAndSafetyPermitTypePermit = relationship('HealthAndSafetyPermitTypePermit', back_populates='HealthAndSafetyPermit')


class HealthAndSafetyPermitType(Base):
    __tablename__ = 'HealthAndSafetyPermitType'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_HealthAndSafetyPermitType'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Description = Column(Unicode, nullable=False)
    Category = Column(Integer, nullable=False)
    Type = Column(Integer, nullable=False)
    Weight = Column(Integer, nullable=False)
    Status = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    ShortDescription = Column(Unicode)

    HealthAndSafetyPermitTypePermit = relationship('HealthAndSafetyPermitTypePermit', back_populates='HealthAndSafetyPermitType')


class History(Base):
    __tablename__ = 'History'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_History'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    UserGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    ParentType = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    ParentReference = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    Content = Column(String(collation='SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    SubType = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    ForeignReference = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    ForeignType = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'))
    OrganisationId = Column(Unicode)
    SubReference = Column(Unicode)
    ProjectGuid = Column(Unicode)


class Manager(Base):
    __tablename__ = 'Manager'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_Manager'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ManagerType = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    ManagerReference = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    OrganisationGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    Status = Column(Integer, nullable=False)
    IsUser = Column(Integer, nullable=False, server_default=text('((0))'))


class Organisation(Base):
    __tablename__ = 'Organisation'
    __table_args__ = (
        PrimaryKeyConstraint('OrganisationId', name='PK_Organisation'),
    )

    OrganisationId = Column(Unicode(50))
    Name = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    UpdatedBy = Column(Unicode)


class OrganisationEntity(Base):
    __tablename__ = 'OrganisationEntity'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_OrganisationEntity'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    OrganisationId = Column(Unicode, nullable=False)
    Title = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    CreatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    LastUpdatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    ParentId = Column(Unicode)
    ExternalReference = Column(Unicode)
    ExternalReferenceType = Column(Unicode)


class Permission(Base):
    __tablename__ = 'Permission'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_Permission'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Name = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    Description = Column(Unicode)
    Group = Column(Unicode)
    SubGroup = Column(Unicode)

    RolePermissions = relationship('RolePermissions', back_populates='Permission')


class Phone(Base):
    __tablename__ = 'Phone'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_Phone'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ContactId = Column(UNIQUEIDENTIFIER, nullable=False, index=True)
    PhoneType = Column(Integer, nullable=False)
    PhoneNumber = Column(Unicode, nullable=False)
    Primary = Column(Integer, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    UpdatedBy = Column(Unicode)


class Postcode(Base):
    __tablename__ = 'Postcode'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_Postcode'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Code = Column(Unicode)
    RegionName = Column(Unicode)
    RegionKey = Column(Unicode)
    CountryCode = Column(Unicode)


class ProjectGroup(Base):
    __tablename__ = 'ProjectGroup'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_ProjectGroup'),
    )

    Id = Column(UNIQUEIDENTIFIER)
    Name = Column(Unicode(50), nullable=False)
    OrganizationId = Column(Unicode(50), nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastModifiedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))

    Project = relationship('Project', secondary='ProjectGroupProject', back_populates='ProjectGroup')


class Property(Base):
    __tablename__ = 'Property'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_Property'),
        Index('IDX_PropertyKeyOrgParentModuleRef', 'Key', 'OrganisationId', 'ParentType', 'ParentReference', 'Module'),
        Index('IDX_PropertyKeyOrgParentRef', 'Key', 'OrganisationId', 'ParentType', 'ParentReference'),
        Index('IDX_PropertyOrgParentRef', 'OrganisationId', 'ParentType', 'ParentReference'),
        Index('IDX_PropertyParentRef', 'ParentType', 'ParentReference')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Key = Column(Unicode(20), nullable=False)
    Value = Column(Unicode, nullable=False)
    ParentType = Column(Unicode(20), nullable=False)
    ParentReference = Column(Unicode(50), nullable=False)
    Format = Column(Integer, nullable=False)
    StatusId = Column(Integer, nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    UpdatedDate = Column(DATETIME2, nullable=False)
    UpdatedBy = Column(Unicode, nullable=False)
    OrganisationId = Column(Unicode(20), nullable=False, server_default=text("(N'')"))
    Type = Column(Unicode(20))
    SubType = Column(Unicode(20))
    Module = Column(Unicode(20))


class PropertyDefinition(Base):
    __tablename__ = 'PropertyDefinition'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_AssetPropertyType'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Created = Column(DATETIME2, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    Format = Column(Integer, nullable=False, server_default=text('((0))'))
    Key = Column(Unicode)
    Label = Column(Unicode)
    ParentType = Column(Unicode)


class PropertyInsurance(Base):
    __tablename__ = 'PropertyInsurance'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_PropertyInsurance'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    PolicyNumber = Column(Integer, nullable=False)
    InsurerName = Column(Integer, nullable=False)
    InsuranceType = Column(Integer, nullable=False)
    PolicyType = Column(Integer, nullable=False)
    InsuredAmount = Column(Integer, nullable=False)
    PremiumAmount = Column(Integer, nullable=False)
    ExcessAmount = Column(Integer, nullable=False)
    PaymentMethod = Column(Integer, nullable=False)
    PaymentFrequency = Column(Integer, nullable=False)
    RenewalDate = Column(Integer, nullable=False)
    Status = Column(Integer, nullable=False)
    ProjectId = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)


class ResourceSubscription(Base):
    __tablename__ = 'ResourceSubscription'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_ResourceSubscription'),
    )

    Id = Column(BigInteger, Identity(start=1, increment=1))
    MaxAllowedResources = Column(Integer, nullable=False, server_default=text('((1))'))
    Type = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(0)))'))
    InitialisedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    OrganisationId = Column(Unicode(50), nullable=False, index=True)
    InitialisedUserId = Column(Unicode(50), nullable=False)

    ResourceSubscriptionUsage = relationship('ResourceSubscriptionUsage', back_populates='ResourceSubscription')


class Role(Base):
    __tablename__ = 'Role'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_Role'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Name = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    IsUser = Column(Integer, nullable=False)
    Description = Column(Unicode)
    Group = Column(Unicode)
    LongDescription = Column(Unicode)

    ContactTypeRole = relationship('ContactTypeRole', back_populates='Role')
    RolePermissions = relationship('RolePermissions', back_populates='Role')


class Shared(Base):
    __tablename__ = 'Shared'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_Shared'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    OrganisationGuid = Column(Unicode, nullable=False)
    TargetEmail = Column(Unicode, nullable=False)
    Token = Column(Unicode, nullable=False)
    ParentType = Column(Unicode, nullable=False)
    ParentReference = Column(Unicode, nullable=False)
    InvitationSentDate = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    UpdatedDate = Column(DATETIME2, nullable=False)
    UpdatedBy = Column(Unicode, nullable=False)
    TargetUserGuid = Column(Unicode)
    CorcId = Column(Unicode)
    InvitationAcceptedDate = Column(DATETIME2)
    InvitationCompletedDate = Column(DATETIME2)
    InvitationPeriod = Column(Integer)
    Permissions = Column(Unicode)


class Site(Base):
    __tablename__ = 'Site'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_Site'),
    )

    Id = Column(UNIQUEIDENTIFIER)
    Name = Column(Unicode(50), nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    Latitude = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    Longitude = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    LastModifiedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    Address = Column(Unicode)
    Boundary = Column(NullType)

    Project = relationship('Project', back_populates='Site')
    SiteGroupSite = relationship('SiteGroupSite', foreign_keys='[SiteGroupSite.AcabimSiteId]', back_populates='Site')
    SiteGroupSite_ = relationship('SiteGroupSite', foreign_keys='[SiteGroupSite.SiteId]', back_populates='Site_')
    SiteUser = relationship('SiteUser', back_populates='Site')
    LandDevelopmentCalculation = relationship('LandDevelopmentCalculation', back_populates='Site')
    FinAccountAnnualRecord = relationship('FinAccountAnnualRecord', back_populates='Site')
    LongTermMaintenanceItem = relationship('LongTermMaintenanceItem', back_populates='Site')


class SiteGroup(Base):
    __tablename__ = 'SiteGroup'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_SiteGroup'),
    )

    Id = Column(UNIQUEIDENTIFIER)
    Name = Column(Unicode(50), nullable=False)
    OrganizationId = Column(Unicode(450), nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastModifiedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))

    SiteGroupSite = relationship('SiteGroupSite', foreign_keys='[SiteGroupSite.AcabimSiteGroupId]', back_populates='SiteGroup')
    SiteGroupSite_ = relationship('SiteGroupSite', foreign_keys='[SiteGroupSite.GroupId]', back_populates='SiteGroup_')


class SpaceContact(Base):
    __tablename__ = 'SpaceContact'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_SpaceContact'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ContactId = Column(Integer, nullable=False)
    Role = Column(Integer, nullable=False)
    UpdatedBy = Column(Unicode, nullable=False)
    UpdatedDate = Column(DATETIME2, nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    SpaceGuid = Column(Unicode)


class VehicleMake(Base):
    __tablename__ = 'VehicleMake'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_VehicleMake'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Name = Column(Unicode, nullable=False)
    OrganisationId = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Description = Column(Unicode)

    VehicleActivity = relationship('VehicleActivity', back_populates='VehicleMake')
    VehicleModel = relationship('VehicleModel', back_populates='VehicleMake')
    Vehicle = relationship('Vehicle', back_populates='VehicleMake')


class WorkOrderAction(Base):
    __tablename__ = 'WorkOrderAction'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_WorkOrderAction'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Status = Column(Integer, nullable=False)
    Role = Column(Unicode, nullable=False)
    Action = Column(Unicode, nullable=False)
    ActionType = Column(Unicode, nullable=False)
    HasDate = Column(Integer, nullable=False, server_default=text('((0))'))
    RequireComment = Column(Integer, nullable=False, server_default=text('((0))'))
    RequireUser = Column(Integer, nullable=False, server_default=text('((0))'))
    RequireAlertFlag = Column(Integer, nullable=False, server_default=text('((0))'))
    HasDueDate = Column(Integer, nullable=False, server_default=text('((0))'))
    Active = Column(Integer, nullable=False, server_default=text('((1))'))
    RemoveContact = Column(Integer, nullable=False, server_default=text('((0))'))
    RemoveManager = Column(Integer, nullable=False, server_default=text('((0))'))
    RemoveModerator = Column(Integer, nullable=False, server_default=text('((0))'))
    NextStatus = Column(Integer)
    RoleTo = Column(Unicode)
    Description = Column(Unicode)


class WorkOrderAssignmentType(Base):
    __tablename__ = 'WorkOrderAssignmentType'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_WorkOrderAssignmentType'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    AssignmentType = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)

    WorkOrderLifecycle = relationship('WorkOrderLifecycle', back_populates='WorkOrderAssignmentType')


class WorkOrderStatus(Base):
    __tablename__ = 'WorkOrderStatus'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_WorkOrderStatus'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Status = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)

    WorkOrder = relationship('WorkOrder', back_populates='WorkOrderStatus')
    WorkOrderLifecycle = relationship('WorkOrderLifecycle', back_populates='WorkOrderStatus')


class WorkOrderType(Base):
    __tablename__ = 'WorkOrderType'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK_WorkOrderType'),
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Name = Column(String(150, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((1))'))
    CibGroup = Column(String(255, 'SQL_Latin1_General_CP1_CS_AS'))
    OmniClass = Column(String(255, 'SQL_Latin1_General_CP1_CS_AS'))

    WorkOrder = relationship('WorkOrder', back_populates='WorkOrderType')
    WorkOrderCategory = relationship('WorkOrderCategory', back_populates='WorkOrderType')
    Action = relationship('Action', back_populates='WorkOrderType')
    WorkOrderVersion = relationship('WorkOrderVersion', back_populates='WorkOrderType')


class EFMigrationsHistory(Base):
    __tablename__ = '__EFMigrationsHistory'
    __table_args__ = (
        PrimaryKeyConstraint('MigrationId', name='PK___EFMigrationsHistory'),
    )

    MigrationId = Column(Unicode(150))
    ProductVersion = Column(Unicode(32), nullable=False)


class Asset(Base):
    __tablename__ = 'Asset'
    __table_args__ = (
        ForeignKeyConstraint(['AssetTypeId'], ['AssetType.Id'], ondelete='CASCADE', name='FK_Asset_AssetType_AssetTypeId'),
        PrimaryKeyConstraint('Guid', name='PK_Asset')
    )

    Guid = Column(Unicode(60))
    Name = Column(Unicode, nullable=False)
    ServiceLife = Column(Integer, nullable=False)
    StartAge = Column(Integer, nullable=False)
    StartValue = Column(DECIMAL(18, 2), nullable=False)
    CurrentValue = Column(DECIMAL(18, 2), nullable=False)
    Created = Column(DateTime, nullable=False, server_default=text('(getdate())'))
    LastUpdated = Column(DateTime, nullable=False, server_default=text('(getdate())'))
    LastUpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    OrganisationId = Column(Unicode, nullable=False, server_default=text("(N'')"))
    AssetGroupId = Column(Integer, nullable=False, index=True, server_default=text('((0))'))
    Quantity = Column(Integer, nullable=False, server_default=text("(N'1')"))
    AssetTypeId = Column(ForeignKey('AssetType.Id', ondelete='CASCADE'), nullable=False, index=True, server_default=text('((0))'))
    CreatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    StartDate = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    MaintenanceRepeat = Column(Integer, nullable=False, server_default=text('((0))'))
    MaintenanceRepeatPeriodType = Column(Integer, nullable=False, server_default=text('((0))'))
    Description = Column(Unicode)
    SpaceGuid = Column(Unicode)
    BuildingStoreyGuid = Column(Unicode)
    BuildingGuid = Column(Unicode)
    SiteGuid = Column(Unicode)
    ProjectGuid = Column(Unicode)
    FinishParentType = Column(Unicode)
    MigrationId = Column(Unicode)
    FinishParentGuid = Column(Unicode)
    FinishType = Column(Unicode)
    MaintenanceRepeatBudget = Column(DECIMAL(18, 2))
    MaintenanceRepeatPeriod = Column(Integer)

    AssetType = relationship('AssetType', back_populates='Asset')


class AssetAudit(Base):
    __tablename__ = 'AssetAudit'
    __table_args__ = (
        ForeignKeyConstraint(['AuditMethodId'], ['AuditMethod.Id'], ondelete='CASCADE', name='FK_AssetAudit_AuditMethod_AuditMethodId'),
        PrimaryKeyConstraint('Id', name='PK_AssetAudit')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ParentReference = Column(Unicode(60), nullable=False)
    AuditMethodId = Column(ForeignKey('AuditMethod.Id', ondelete='CASCADE'), nullable=False, index=True)
    Rating = Column(Integer, nullable=False)
    Status = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    AuditType = Column(Integer, nullable=False, server_default=text('((0))'))
    RatingCeiling = Column(Integer, nullable=False, server_default=text('((0))'))
    ParentType = Column(Unicode, nullable=False, server_default=text("(N'asset')"))
    AuditUserGuid = Column(Unicode)
    AuditStartDate = Column(DATETIME2)
    AuditEndDate = Column(DATETIME2)

    AuditMethod = relationship('AuditMethod', back_populates='AssetAudit')


class AssetComponent(Base):
    __tablename__ = 'AssetComponent'
    __table_args__ = (
        ForeignKeyConstraint(['AssetComponentTypeId'], ['AssetType.Id'], ondelete='CASCADE', name='FK_AssetComponent_AssetType_AssetComponentTypeId'),
        PrimaryKeyConstraint('Guid', name='PK_AssetComponent')
    )

    Guid = Column(Unicode(450))
    ParentType = Column(Unicode, nullable=False)
    ParentReference = Column(Unicode, nullable=False)
    AssetComponentTypeId = Column(ForeignKey('AssetType.Id', ondelete='CASCADE'), nullable=False, index=True)

    AssetType = relationship('AssetType', back_populates='AssetComponent')


class AssetGroupType(Base):
    __tablename__ = 'AssetGroupType'
    __table_args__ = (
        ForeignKeyConstraint(['AssetGroupId'], ['AssetGroup.Id'], ondelete='CASCADE', name='FK_AssetGroupType_AssetGroup_AssetGroupId'),
        ForeignKeyConstraint(['AssetTypeId'], ['AssetType.Id'], ondelete='CASCADE', name='FK_AssetGroupType_AssetType_AssetTypeId'),
        PrimaryKeyConstraint('Id', name='PK_AssetGroupType')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    OrganisationId = Column(Unicode, nullable=False)
    AssetGroupId = Column(ForeignKey('AssetGroup.Id', ondelete='CASCADE'), nullable=False, index=True)
    AssetTypeId = Column(ForeignKey('AssetType.Id', ondelete='CASCADE'), nullable=False, index=True)
    Created = Column(DATETIME2, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))

    AssetGroup = relationship('AssetGroup', back_populates='AssetGroupType')
    AssetType = relationship('AssetType', back_populates='AssetGroupType')


class AssetTypeClassification(Base):
    __tablename__ = 'AssetTypeClassification'
    __table_args__ = (
        ForeignKeyConstraint(['AssetTypeId'], ['AssetType.Id'], ondelete='CASCADE', name='FK_AssetTypeClassification_AssetType_AssetTypeId'),
        PrimaryKeyConstraint('Id', name='PK_AssetTypeClassification')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    AssetTypeId = Column(ForeignKey('AssetType.Id', ondelete='CASCADE'), nullable=False, index=True)
    ClassificationType = Column(Integer, nullable=False)
    Name = Column(Unicode, nullable=False)
    OrganisationId = Column(Unicode, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))

    AssetType = relationship('AssetType', back_populates='AssetTypeClassification')


class Contact(Base):
    __tablename__ = 'Contact'
    __table_args__ = (
        ForeignKeyConstraint(['ContactTypeId'], ['ContactType.Id'], ondelete='CASCADE', name='FK_ContactType_Contact'),
        PrimaryKeyConstraint('Id', name='PK_Contact')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    LastUpdated = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((1))'))
    OrganisationId = Column(Unicode, nullable=False)
    Registered = Column(Integer, nullable=False, server_default=text('((0))'))
    LegalRepresentative = Column(Integer, nullable=False, server_default=text('((0))'))
    IsOrganisation = Column(Integer, nullable=False, server_default=text('((0))'))
    memberOf = Column(Integer, nullable=False, server_default=text('((0))'))
    IsPreferredContact = Column(Integer, nullable=False, server_default=text('((0))'))
    PrimaryContact = Column(Integer, nullable=False, server_default=text('((0))'))
    IsAdministrator = Column(Integer, nullable=False, server_default=text('((0))'))
    UserGuid = Column(Unicode)
    UpdatedBy = Column(Unicode)
    ContactTypeId = Column(ForeignKey('ContactType.Id', ondelete='CASCADE'), index=True, server_default=text('((0))'))
    PreferredContactProperty = Column(Integer)
    LegalName = Column(Unicode)

    ContactType = relationship('ContactType', back_populates='Contact')
    ContactEntity = relationship('ContactEntity', back_populates='Contact')
    ContactOrganisation = relationship('ContactOrganisation', back_populates='Contact')
    ContactOrganisationProperty = relationship('ContactOrganisationProperty', back_populates='Contact')
    ContactProfileProperty = relationship('ContactProfileProperty', back_populates='Contact')
    FinTransactionGroup = relationship('FinTransactionGroup', back_populates='Contact')


class ContactTypeProperty(Base):
    __tablename__ = 'ContactTypeProperty'
    __table_args__ = (
        ForeignKeyConstraint(['ContactTypeId'], ['ContactType.Id'], ondelete='CASCADE', name='FK_ContactTypeProperty_ContactType_ContactTypeId'),
        PrimaryKeyConstraint('Id', name='PK_ContactTypeProperty')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ContactTypeId = Column(ForeignKey('ContactType.Id', ondelete='CASCADE'), nullable=False, index=True)
    PropertyType = Column(Unicode, nullable=False)
    Value = Column(Unicode)

    ContactType = relationship('ContactType', back_populates='ContactTypeProperty')


class ContactTypeRole(Base):
    __tablename__ = 'ContactTypeRole'
    __table_args__ = (
        ForeignKeyConstraint(['RoleId'], ['Role.Id'], ondelete='CASCADE', name='FK_ContactTypeRole_Role_RoleId'),
        PrimaryKeyConstraint('Id', name='PK_ContactTypeRole')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    RoleId = Column(ForeignKey('Role.Id', ondelete='CASCADE'), nullable=False, index=True)
    ContactTypeId = Column(Integer, nullable=False)

    Role = relationship('Role', back_populates='ContactTypeRole')


class FileCapRecordLibraryItem(Base):
    __tablename__ = 'FileCapRecordLibraryItem'
    __table_args__ = (
        ForeignKeyConstraint(['CapId'], ['FileCapRecord.Id'], ondelete='CASCADE', name='FK_FileCapRecordLibraryItem_FileCapRecord_CapId'),
        PrimaryKeyConstraint('CapId', 'OmniClassNumber', name='PK_FileCapRecordLibraryItem')
    )

    CapId = Column(ForeignKey('FileCapRecord.Id', ondelete='CASCADE'), nullable=False)
    OmniClassNumber = Column(Unicode(450), nullable=False)
    AddedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))

    FileCapRecord = relationship('FileCapRecord', back_populates='FileCapRecordLibraryItem')


class FileUsage(Base):
    __tablename__ = 'FileUsage'
    __table_args__ = (
        ForeignKeyConstraint(['FileGuid'], ['File.Guid'], ondelete='CASCADE', name='FK_FileUsage_File_FileGuid'),
        PrimaryKeyConstraint('Id', name='PK_FileUsage')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    UserGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    FileGuid = Column(ForeignKey('File.Guid', ondelete='CASCADE'), nullable=False, index=True)
    ParentType = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    ParentReference = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    Status = Column(Integer, nullable=False)
    UpdatedDate = Column(DATETIME2, nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    SubReference = Column(Unicode)
    SubType = Column(Unicode)
    ProjectGuid = Column(Unicode)

    File = relationship('File', back_populates='FileUsage')
    FileUsageDocumentTypeFile = relationship('FileUsageDocumentTypeFile', back_populates='FileUsage')


class FinAccountClass(Base):
    __tablename__ = 'FinAccountClass'
    __table_args__ = (
        ForeignKeyConstraint(['FinOrganisationId'], ['FinOrganisation.Id'], ondelete='CASCADE', name='FK_FinAccountClass_FinOrganisation_FinOrganisationId'),
        PrimaryKeyConstraint('Id', name='PK_FinAccountClass')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Identifier = Column(Integer, nullable=False)
    Name = Column(Unicode, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    UpdatedBy = Column(Unicode, nullable=False)
    Updated = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    FinOrganisationId = Column(ForeignKey('FinOrganisation.Id', ondelete='CASCADE'), nullable=False, index=True, server_default=text('((0))'))
    Description = Column(Unicode)
    DisabledBy = Column(Unicode)
    Disabled = Column(DATETIME2)

    FinOrganisation = relationship('FinOrganisation', back_populates='FinAccountClass')
    FinAccount = relationship('FinAccount', back_populates='FinAccountClass')


class HealthAndSafetyPermitTypePermit(Base):
    __tablename__ = 'HealthAndSafetyPermitTypePermit'
    __table_args__ = (
        ForeignKeyConstraint(['HealthAndSafetyPermitId'], ['HealthAndSafetyPermit.Id'], ondelete='CASCADE', name='FK_HealthAndSafetyPermitTypePermit_HealthAndSafetyPermit_HealthAndSafetyPermitId'),
        ForeignKeyConstraint(['HealthAndSafetyPermitTypeId'], ['HealthAndSafetyPermitType.Id'], ondelete='CASCADE', name='FK_HealthAndSafetyPermitTypePermit_HealthAndSafetyPermitType_HealthAndSafetyPermitTypeId'),
        PrimaryKeyConstraint('Id', name='PK_HealthAndSafetyPermitTypePermit')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    HealthAndSafetyPermitId = Column(ForeignKey('HealthAndSafetyPermit.Id', ondelete='CASCADE'), nullable=False, index=True)
    HealthAndSafetyPermitTypeId = Column(ForeignKey('HealthAndSafetyPermitType.Id', ondelete='CASCADE'), nullable=False, index=True)
    Status = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)

    HealthAndSafetyPermit = relationship('HealthAndSafetyPermit', back_populates='HealthAndSafetyPermitTypePermit')
    HealthAndSafetyPermitType = relationship('HealthAndSafetyPermitType', back_populates='HealthAndSafetyPermitTypePermit')


class Project(Base):
    __tablename__ = 'Project'
    __table_args__ = (
        ForeignKeyConstraint(['ParentId'], ['Project.Id'], name='FK_Project_Project_ParentId'),
        ForeignKeyConstraint(['SiteId'], ['Site.Id'], name='FK_Project_Site_SiteId'),
        PrimaryKeyConstraint('Id', name='PK_Project')
    )

    Id = Column(Unicode(50))
    Name = Column(Unicode(450), nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    SiteId = Column(ForeignKey('Site.Id'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastModifiedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    TenancyStatus = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(0)))'))
    ParentId = Column(ForeignKey('Project.Id'), index=True)
    Description = Column(Unicode(1000))
    BuildingGuid = Column(Unicode)

    FileCapRecord = relationship('FileCapRecord', secondary='ProjectCap', back_populates='Project')
    ProjectGroup = relationship('ProjectGroup', secondary='ProjectGroupProject', back_populates='Project')
    Project = relationship('Project', remote_side=[Id], back_populates='Project_reverse')
    Project_reverse = relationship('Project', remote_side=[ParentId], back_populates='Project')
    Site = relationship('Site', back_populates='Project')
    BimDataModel = relationship('BimDataModel', back_populates='Project')
    CapExecutionHistory = relationship('CapExecutionHistory', back_populates='Project')
    LandDevelopmentCalculation = relationship('LandDevelopmentCalculation', back_populates='Project')
    ProjectCapLibrary = relationship('ProjectCapLibrary', back_populates='Project')
    ProjectTask = relationship('ProjectTask', back_populates='Project')
    ProjectUser = relationship('ProjectUser', back_populates='Project')
    SpaceGroup = relationship('SpaceGroup', back_populates='Project')
    FinAccountAnnualRecord = relationship('FinAccountAnnualRecord', back_populates='Project')
    LongTermMaintenanceItem = relationship('LongTermMaintenanceItem', back_populates='Project')
    PropertyLease = relationship('PropertyLease', back_populates='Project')


class ResourceSubscriptionUsage(Base):
    __tablename__ = 'ResourceSubscriptionUsage'
    __table_args__ = (
        ForeignKeyConstraint(['SubscriptionId'], ['ResourceSubscription.Id'], ondelete='CASCADE', name='FK_ResourceSubscriptionUsage_ResourceSubscription_SubscriptionId'),
        PrimaryKeyConstraint('SubscriptionId', 'ResourceId', name='PK_ResourceSubscriptionUsage')
    )

    SubscriptionId = Column(ForeignKey('ResourceSubscription.Id', ondelete='CASCADE'), nullable=False)
    ResourceId = Column(Unicode(450), nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    StartedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))

    ResourceSubscription = relationship('ResourceSubscription', back_populates='ResourceSubscriptionUsage')


class RolePermissions(Base):
    __tablename__ = 'RolePermissions'
    __table_args__ = (
        ForeignKeyConstraint(['PermissionId'], ['Permission.Id'], ondelete='CASCADE', name='FK_RolePermissions_Permission_PermissionId'),
        ForeignKeyConstraint(['RoleId'], ['Role.Id'], ondelete='CASCADE', name='FK_RolePermissions_Role_RoleId'),
        PrimaryKeyConstraint('Id', name='PK_RolePermissions')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    RoleId = Column(ForeignKey('Role.Id', ondelete='CASCADE'), nullable=False, index=True)
    PermissionId = Column(ForeignKey('Permission.Id', ondelete='CASCADE'), nullable=False, index=True)

    Permission = relationship('Permission', back_populates='RolePermissions')
    Role = relationship('Role', back_populates='RolePermissions')


class SiteGroupSite(Base):
    __tablename__ = 'SiteGroupSite'
    __table_args__ = (
        ForeignKeyConstraint(['AcabimSiteGroupId'], ['SiteGroup.Id'], name='FK_SiteGroupSite_SiteGroup_AcabimSiteGroupId'),
        ForeignKeyConstraint(['AcabimSiteId'], ['Site.Id'], name='FK_SiteGroupSite_Site_AcabimSiteId'),
        ForeignKeyConstraint(['GroupId'], ['SiteGroup.Id'], name='FK_SiteGroupSite_SiteGroup_GroupId'),
        ForeignKeyConstraint(['SiteId'], ['Site.Id'], ondelete='CASCADE', name='FK_SiteGroupSite_Site_SiteId'),
        PrimaryKeyConstraint('GroupId', 'SiteId', name='PK_SiteGroupSite')
    )

    GroupId = Column(ForeignKey('SiteGroup.Id'), nullable=False)
    SiteId = Column(ForeignKey('Site.Id', ondelete='CASCADE'), nullable=False, index=True)
    AcabimSiteGroupId = Column(ForeignKey('SiteGroup.Id'), index=True)
    AcabimSiteId = Column(ForeignKey('Site.Id'), index=True)

    SiteGroup = relationship('SiteGroup', foreign_keys=[AcabimSiteGroupId], back_populates='SiteGroupSite')
    Site = relationship('Site', foreign_keys=[AcabimSiteId], back_populates='SiteGroupSite')
    SiteGroup_ = relationship('SiteGroup', foreign_keys=[GroupId], back_populates='SiteGroupSite_')
    Site_ = relationship('Site', foreign_keys=[SiteId], back_populates='SiteGroupSite_')


class SiteUser(Base):
    __tablename__ = 'SiteUser'
    __table_args__ = (
        ForeignKeyConstraint(['SiteId'], ['Site.Id'], ondelete='CASCADE', name='FK_SiteUser_Site_SiteId'),
        PrimaryKeyConstraint('SiteId', 'UserId', 'Role', name='PK_SiteUser')
    )

    SiteId = Column(ForeignKey('Site.Id', ondelete='CASCADE'), nullable=False)
    UserId = Column(Unicode(450), nullable=False)
    Role = Column(Integer, nullable=False, server_default=text('((2))'))
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    CreatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    OrganizationId = Column(Unicode, nullable=False, server_default=text("(N'')"))

    Site = relationship('Site', back_populates='SiteUser')


class VehicleActivity(Base):
    __tablename__ = 'VehicleActivity'
    __table_args__ = (
        ForeignKeyConstraint(['VehicleId'], ['VehicleMake.Id'], ondelete='CASCADE', name='FK_VehicleActivity_VehicleMake_VehicleId'),
        PrimaryKeyConstraint('Id', name='PK_VehicleActivity')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    VehicleId = Column(ForeignKey('VehicleMake.Id', ondelete='CASCADE'), nullable=False, index=True)
    ActivityType = Column(Integer, nullable=False)
    ActivityDate = Column(DATETIME2, nullable=False)
    OrganisationId = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Description = Column(Unicode)

    VehicleMake = relationship('VehicleMake', back_populates='VehicleActivity')


class VehicleModel(Base):
    __tablename__ = 'VehicleModel'
    __table_args__ = (
        ForeignKeyConstraint(['VehicleMakeId'], ['VehicleMake.Id'], ondelete='CASCADE', name='FK_VehicleModel_VehicleMake_VehicleMakeId'),
        PrimaryKeyConstraint('Id', name='PK_VehicleModel')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Name = Column(Unicode, nullable=False)
    VehicleMakeId = Column(ForeignKey('VehicleMake.Id', ondelete='CASCADE'), nullable=False, index=True)
    OrganisationId = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Description = Column(Unicode)

    VehicleMake = relationship('VehicleMake', back_populates='VehicleModel')
    Vehicle = relationship('Vehicle', back_populates='VehicleModel')


class WorkOrder(Base):
    __tablename__ = 'WorkOrder'
    __table_args__ = (
        ForeignKeyConstraint(['Status'], ['WorkOrderStatus.Id'], name='FK_WorkOrder_WorkOrderStatus_Status'),
        ForeignKeyConstraint(['WorkTypeId'], ['WorkOrderType.Id'], name='FK_WorkOrder_WorkOrderType_WorkTypeId'),
        PrimaryKeyConstraint('Guid', name='PK_WorkOrder')
    )

    Guid = Column(Unicode(80))
    Version = Column(Integer, nullable=False)
    DateReceived = Column(DateTime, nullable=False, server_default=text('(getdate())'))
    DateRequired = Column(DateTime, nullable=False)
    RequestedBy = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    WorkOrderDescription = Column(String(collation='SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    WorkTypeId = Column(ForeignKey('WorkOrderType.Id'), nullable=False, index=True)
    CategoryId = Column(Integer, nullable=False)
    Priority = Column(Integer, nullable=False)
    SiteGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    OrderNumber = Column(Integer, nullable=False)
    LastUpdatedDate = Column(DateTime, nullable=False)
    UpdatedBy = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    Status = Column(ForeignKey('WorkOrderStatus.Id'), nullable=False, index=True, server_default=text('((0))'))
    SecondaryOrderNumber = Column(Integer, nullable=False, server_default=text('((0))'))
    OnHoldToDate = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    Flag = Column(Integer, nullable=False, server_default=text('((0))'))
    DueDate = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    HeathAndSafetyPermitStatus = Column(Integer, nullable=False, server_default=text('((0))'))
    OrganisationGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    TaskId = Column(Integer)
    ProjectGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    StoreyGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    SpaceGuids = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CS_AS'))
    AssetGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    LocationDescription = Column(String(collation='SQL_Latin1_General_CP1_CS_AS'))
    ParentGuid = Column(Unicode(80))
    CurrentContact = Column(Integer, server_default=text('((0))'))
    ParentType = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'))
    ExternalOrderNumber = Column(Unicode)
    ModeratorGuid = Column(Unicode)
    CostActual = Column(DECIMAL(18, 2))
    CostBudget = Column(DECIMAL(18, 2))
    CostCommitted = Column(DECIMAL(18, 2))
    ExpenseType = Column(Integer)
    ManagerGuid = Column(Unicode)
    WorkOrderCategoryId = Column(Integer, index=True)
    WorkOrderTaskId = Column(Integer, index=True)

    WorkOrderStatus = relationship('WorkOrderStatus', back_populates='WorkOrder')
    WorkOrderType = relationship('WorkOrderType', back_populates='WorkOrder')
    WorkOrderLifecycle = relationship('WorkOrderLifecycle', back_populates='WorkOrder')


class WorkOrderCategory(Base):
    __tablename__ = 'WorkOrderCategory'
    __table_args__ = (
        ForeignKeyConstraint(['WorkTypeId'], ['WorkOrderType.Id'], ondelete='CASCADE', name='FK_WorkOrderCategory_WorkOrderType_WorkTypeId'),
        PrimaryKeyConstraint('Id', name='PK_WorkOrderCategory')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    OrganisationGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    WorkTypeId = Column(ForeignKey('WorkOrderType.Id', ondelete='CASCADE'), nullable=False, index=True)
    Name = Column(String(150, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    DefaultPriority = Column(Integer, nullable=False, server_default=text('((0))'))
    Status = Column(Integer, nullable=False, server_default=text('((1))'))
    ManagerType = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'))
    ManagerReference = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    DefaultAssigneeType = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'))
    DefaultAssigneeReference = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))

    WorkOrderType = relationship('WorkOrderType', back_populates='WorkOrderCategory')
    WorkOrderTask = relationship('WorkOrderTask', foreign_keys='[WorkOrderTask.CategoryId]', back_populates='WorkOrderCategory')
    WorkOrderTask_ = relationship('WorkOrderTask', foreign_keys='[WorkOrderTask.WorkOrderCategoryId1]', back_populates='WorkOrderCategory_')
    WorkOrderVersion = relationship('WorkOrderVersion', back_populates='WorkOrderCategory')


class BimDataModel(Base):
    __tablename__ = 'BimDataModel'
    __table_args__ = (
        ForeignKeyConstraint(['ProjectId'], ['Project.Id'], name='FK_BimDataModel_Project_ProjectId'),
        PrimaryKeyConstraint('ModelId', name='PK_BimDataModel')
    )

    ModelId = Column(UNIQUEIDENTIFIER)
    ModelType = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(1)))'))
    ModelPhase = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(0)))'))
    ModelState = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(0)))'))
    OrganisationId = Column(Unicode(50), nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    CreatedUserId = Column(Unicode(50), nullable=False)
    IsDefault = Column(Boolean, nullable=False, server_default=text('(CONVERT([bit],(0)))'))
    ModelName = Column(Unicode)
    ProjectId = Column(ForeignKey('Project.Id'), index=True)
    PracticalCompletionDate = Column(DATETIME2)
    ConstructionStartDate = Column(DATETIME2)
    Data = Column(Unicode)

    Project = relationship('Project', back_populates='BimDataModel')
    BimDataModelVersion = relationship('BimDataModelVersion', back_populates='BimDataModel')
    Building = relationship('Building', back_populates='BimDataModel')
    BuildingElement3DSpatialData = relationship('BuildingElement3DSpatialData', back_populates='BimDataModel')
    BuildingElementPropertySet = relationship('BuildingElementPropertySet', back_populates='BimDataModel')
    MiscellaneousBuildingElement = relationship('MiscellaneousBuildingElement', back_populates='BimDataModel')
    SpaceEnclosureChild = relationship('SpaceEnclosureChild', back_populates='BimDataModel')
    UsageClassification = relationship('UsageClassification', back_populates='BimDataModel')
    BuildingStorey = relationship('BuildingStorey', back_populates='BimDataModel')
    Beam = relationship('Beam', back_populates='BimDataModel')
    Column_ = relationship('Column_', back_populates='BimDataModel')
    OpeningContainer = relationship('OpeningContainer', back_populates='BimDataModel')
    Ramp = relationship('Ramp', back_populates='BimDataModel')
    Roof = relationship('Roof', back_populates='BimDataModel')
    Slab = relationship('Slab', back_populates='BimDataModel')
    SpatialZone = relationship('SpatialZone', back_populates='BimDataModel')
    Stair = relationship('Stair', back_populates='BimDataModel')
    Wall = relationship('Wall', back_populates='BimDataModel')
    OpeningElement = relationship('OpeningElement', back_populates='BimDataModel')
    RampFlight = relationship('RampFlight', back_populates='BimDataModel')
    Space = relationship('Space', back_populates='BimDataModel')
    StairFlight = relationship('StairFlight', back_populates='BimDataModel')
    Window = relationship('Window', back_populates='BimDataModel')
    Door = relationship('Door', back_populates='BimDataModel')
    LightFixture = relationship('LightFixture', back_populates='BimDataModel')
    SanitaryTerminal = relationship('SanitaryTerminal', back_populates='BimDataModel')
    SpaceEnclosure = relationship('SpaceEnclosure', back_populates='BimDataModel')
    WindowPanel = relationship('WindowPanel', back_populates='BimDataModel')
    DoorPanel = relationship('DoorPanel', back_populates='BimDataModel')
    Lamp = relationship('Lamp', back_populates='BimDataModel')


class CapExecutionHistory(Base):
    __tablename__ = 'CapExecutionHistory'
    __table_args__ = (
        ForeignKeyConstraint(['ProjectId'], ['Project.Id'], ondelete='CASCADE', name='FK_CapExecutionHistory_Project_ProjectId'),
        ForeignKeyConstraint(['RootCapId'], ['FileCapRecord.Id'], ondelete='CASCADE', name='FK_CapExecutionHistory_FileCapRecord_RootCapId'),
        PrimaryKeyConstraint('ExecutionId', name='PK_CapExecutionHistory')
    )

    ExecutionId = Column(Unicode(50))
    UserId = Column(Unicode(50), nullable=False)
    OrganisationId = Column(Unicode(50), nullable=False)
    ExecutionDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    RootCapId = Column(ForeignKey('FileCapRecord.Id', ondelete='CASCADE'), nullable=False, index=True)
    RootCapVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    ExecutionState = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(0)))'))
    ProjectId = Column(ForeignKey('Project.Id', ondelete='CASCADE'), index=True)
    BatchId = Column(Unicode(50))
    Metadata = Column(Unicode)

    Project = relationship('Project', back_populates='CapExecutionHistory')
    FileCapRecord = relationship('FileCapRecord', back_populates='CapExecutionHistory')
    CapExecutionHistoryDependency = relationship('CapExecutionHistoryDependency', back_populates='CapExecutionHistory')


class ContactEntity(Base):
    __tablename__ = 'ContactEntity'
    __table_args__ = (
        ForeignKeyConstraint(['ContactId'], ['Contact.Id'], ondelete='CASCADE', name='FK_ContactEntity_Contact_ContactId'),
        PrimaryKeyConstraint('Id', name='PK_ContactEntity')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ContactId = Column(ForeignKey('Contact.Id', ondelete='CASCADE'), nullable=False, index=True)
    LastUpdated = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    OrganisationEntityId = Column(Integer, nullable=False, server_default=text('((0))'))
    UpdatedBy = Column(Unicode)

    Contact = relationship('Contact', back_populates='ContactEntity')


class ContactOrganisation(Base):
    __tablename__ = 'ContactOrganisation'
    __table_args__ = (
        ForeignKeyConstraint(['ContactId'], ['Contact.Id'], ondelete='CASCADE', name='FK_ContactOrganisation_Contact_ContactId'),
        PrimaryKeyConstraint('Id', name='PK_ContactOrganisation')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ContactId = Column(ForeignKey('Contact.Id', ondelete='CASCADE'), nullable=False, index=True)
    OrganisationId = Column(Unicode, nullable=False)
    ContactType = Column(Integer, nullable=False, server_default=text('((0))'))
    LastUpdated = Column(DateTime, nullable=False, server_default=text('(getdate())'))
    UpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    ContactRole = Column(Unicode)
    Department = Column(Unicode)
    AccountCode = Column(Unicode(150))

    Contact = relationship('Contact', back_populates='ContactOrganisation')


class ContactOrganisationProperty(Base):
    __tablename__ = 'ContactOrganisationProperty'
    __table_args__ = (
        ForeignKeyConstraint(['ContactId'], ['Contact.Id'], ondelete='CASCADE', name='FK_ContactOrganisationProperty_Contact_ContactId'),
        PrimaryKeyConstraint('Id', name='PK_ContactOrganisationProperty')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ContactId = Column(ForeignKey('Contact.Id', ondelete='CASCADE'), nullable=False, index=True)
    OrganisationId = Column(Unicode, nullable=False)
    PropertyType = Column(Unicode, nullable=False)
    PropertyLabel = Column(Unicode, nullable=False)
    DefaultForType = Column(Integer, nullable=False)
    PropertyValue = Column(Unicode)

    Contact = relationship('Contact', back_populates='ContactOrganisationProperty')


class ContactProfileProperty(Base):
    __tablename__ = 'ContactProfileProperty'
    __table_args__ = (
        ForeignKeyConstraint(['ContactId'], ['Contact.Id'], ondelete='CASCADE', name='FK_ContactProfileProperty_Contact_ContactId'),
        PrimaryKeyConstraint('Id', name='PK_ContactProfileProperty')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ContactId = Column(ForeignKey('Contact.Id', ondelete='CASCADE'), nullable=False, index=True)
    PropertyType = Column(Unicode, nullable=False)
    PropertyLabel = Column(Unicode, nullable=False)
    PropertyValue = Column(Unicode)
    DefaultForType = Column(Integer)
    PropertySubType = Column(Unicode)

    Contact = relationship('Contact', back_populates='ContactProfileProperty')


class FileUsageDocumentTypeFile(Base):
    __tablename__ = 'FileUsageDocumentTypeFile'
    __table_args__ = (
        ForeignKeyConstraint(['FileUsageDocumentTypeId'], ['FileUsageDocumentType.Id'], ondelete='CASCADE', name='FK_FileUsageDocumentTypeFile_FileUsageDocumentType_FileUsageDocumentTypeId'),
        ForeignKeyConstraint(['FileUsageId'], ['FileUsage.Id'], ondelete='CASCADE', name='FK_FileUsageDocumentTypeFile_FileUsage_FileUsageId'),
        PrimaryKeyConstraint('Id', name='PK_FileUsageDocumentTypeFile')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    FileUsageDocumentTypeId = Column(ForeignKey('FileUsageDocumentType.Id', ondelete='CASCADE'), nullable=False, index=True)
    FileUsageId = Column(ForeignKey('FileUsage.Id', ondelete='CASCADE'), nullable=False, index=True)

    FileUsageDocumentType = relationship('FileUsageDocumentType', back_populates='FileUsageDocumentTypeFile')
    FileUsage = relationship('FileUsage', back_populates='FileUsageDocumentTypeFile')


class FinAccount(Base):
    __tablename__ = 'FinAccount'
    __table_args__ = (
        ForeignKeyConstraint(['FinAccountClassId'], ['FinAccountClass.Id'], name='FK_FinAccount_FinAccountClass_FinAccountClassId'),
        ForeignKeyConstraint(['FinOrganisationId'], ['FinOrganisation.Id'], name='FK_FinAccount_FinOrganisation_FinOrganisationId'),
        PrimaryKeyConstraint('Id', name='PK_FinAccount')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    FinOrganisationId = Column(ForeignKey('FinOrganisation.Id'), nullable=False)
    FinAccountClassId = Column(ForeignKey('FinAccountClass.Id'), nullable=False)
    Identifier = Column(Integer, nullable=False)
    Name = Column(Unicode, nullable=False)
    ValueType = Column(Integer, nullable=False)
    Budget = Column(DECIMAL(18, 2), nullable=False)
    AccountType = Column(Integer, nullable=False, server_default=text('((0))'))
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    Updated = Column(DATETIME2, nullable=False)
    UpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    Description = Column(Unicode)
    ExternalReference = Column(Unicode)
    ExternalReferenceType = Column(Unicode)
    Disabled = Column(DATETIME2)
    DisabledBy = Column(Unicode)

    FinAccountClass = relationship('FinAccountClass', back_populates='FinAccount')
    FinOrganisation = relationship('FinOrganisation', back_populates='FinAccount')
    FinAccountAnnualRecord = relationship('FinAccountAnnualRecord', back_populates='FinAccount')
    FinBudget = relationship('FinBudget', back_populates='FinAccount')
    LineItem = relationship('LineItem', back_populates='FinAccount')
    MaintenanceType = relationship('MaintenanceType', back_populates='FinAccount')
    FinTransaction = relationship('FinTransaction', back_populates='FinAccount')


class FinTransactionGroup(Base):
    __tablename__ = 'FinTransactionGroup'
    __table_args__ = (
        ForeignKeyConstraint(['ContactId'], ['Contact.Id'], name='FK_FinTransactionGroup_Contact_ContactId'),
        ForeignKeyConstraint(['FinOrganisationId'], ['FinOrganisation.Id'], name='FK_FinTransactionGroup_FinOrganisation_FinOrganisationId'),
        PrimaryKeyConstraint('Id', name='PK_FinTransactionGroup')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    FinOrganisationId = Column(ForeignKey('FinOrganisation.Id'), nullable=False, index=True)
    GroupType = Column(Integer, nullable=False)
    Identifier = Column(Unicode, nullable=False)
    OrderNumber = Column(Integer, nullable=False)
    ContactId = Column(ForeignKey('Contact.Id'), nullable=False, index=True)
    Tax = Column(Integer, nullable=False)
    GroupDiscount = Column(DECIMAL(18, 2), nullable=False)
    PaymentStatus = Column(Integer, nullable=False)
    GeneralStatus = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    RepeatFlag = Column(Boolean, nullable=False, server_default=text('(CONVERT([bit],(0)))'))
    RepeatFrequency = Column(Integer, nullable=False, server_default=text('((0))'))
    RepeatPeriod = Column(Integer, nullable=False, server_default=text('((0))'))
    PredecessorId = Column(Integer, nullable=False, server_default=text('((0))'))
    DefaultPaymentPeriod = Column(Integer, nullable=False, server_default=text('((0))'))
    DefaultPaymentPeriodType = Column(Integer, nullable=False, server_default=text('((0))'))
    DefaultPaymentPeriodValue = Column(Integer, nullable=False, server_default=text('((0))'))
    Currency = Column(Integer, nullable=False, server_default=text('((0))'))
    Description = Column(Unicode)
    IssuedDate = Column(DATETIME2)
    PaymentDueDate = Column(DATETIME2)
    FullyPaidDate = Column(DATETIME2)
    Closed = Column(DATETIME2)
    ClosedBy = Column(Unicode)
    ParentReference = Column(Unicode)
    ParentType = Column(Unicode)
    TemplateType = Column(Integer)

    Contact = relationship('Contact', back_populates='FinTransactionGroup')
    FinOrganisation = relationship('FinOrganisation', back_populates='FinTransactionGroup')
    FinAdditionalProperties = relationship('FinAdditionalProperties', back_populates='FinTransactionGroup')
    FinPayment = relationship('FinPayment', back_populates='FinTransactionGroup')
    FinTransaction = relationship('FinTransaction', back_populates='FinTransactionGroup')


class LandDevelopmentCalculation(Base):
    __tablename__ = 'LandDevelopmentCalculation'
    __table_args__ = (
        ForeignKeyConstraint(['ProjectId'], ['Project.Id'], ondelete='CASCADE', name='FK_LandDevelopmentCalculation_Project_ProjectId'),
        ForeignKeyConstraint(['SiteGuid'], ['Site.Id'], ondelete='CASCADE', name='FK_LandDevelopmentCalculation_Site_SiteGuid'),
        PrimaryKeyConstraint('Id', name='PK_LandDevelopmentCalculation')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    SiteGuid = Column(ForeignKey('Site.Id', ondelete='CASCADE'), nullable=False, index=True)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    ProjectId = Column(ForeignKey('Project.Id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("(N'')"))
    Content = Column(Unicode)

    Project = relationship('Project', back_populates='LandDevelopmentCalculation')
    Site = relationship('Site', back_populates='LandDevelopmentCalculation')


t_ProjectCap = Table(
    'ProjectCap', metadata,
    Column('ProjectId', ForeignKey('Project.Id', ondelete='CASCADE'), nullable=False),
    Column('CapId', ForeignKey('FileCapRecord.Id'), nullable=False, index=True),
    ForeignKeyConstraint(['CapId'], ['FileCapRecord.Id'], name='FK_ProjectCap_FileCapRecord_CapId'),
    ForeignKeyConstraint(['ProjectId'], ['Project.Id'], ondelete='CASCADE', name='FK_ProjectCap_Project_ProjectId'),
    PrimaryKeyConstraint('ProjectId', 'CapId', name='PK_ProjectCap'),
    Index('IX_ProjectCap_CapId', 'CapId')
)


class ProjectCapLibrary(Base):
    __tablename__ = 'ProjectCapLibrary'
    __table_args__ = (
        ForeignKeyConstraint(['ProjectId'], ['Project.Id'], ondelete='CASCADE', name='FK_ProjectCapLibrary_Project_ProjectId'),
        PrimaryKeyConstraint('ProjectId', 'OmniClassNumber', name='PK_ProjectCapLibrary')
    )

    ProjectId = Column(ForeignKey('Project.Id', ondelete='CASCADE'), nullable=False)
    OmniClassNumber = Column(Unicode(450), nullable=False)

    Project = relationship('Project', back_populates='ProjectCapLibrary')


t_ProjectGroupProject = Table(
    'ProjectGroupProject', metadata,
    Column('GroupId', ForeignKey('ProjectGroup.Id'), nullable=False),
    Column('ProjectId', ForeignKey('Project.Id', ondelete='CASCADE'), nullable=False, index=True),
    ForeignKeyConstraint(['GroupId'], ['ProjectGroup.Id'], name='FK_ProjectGroupProject_ProjectGroup_GroupId'),
    ForeignKeyConstraint(['ProjectId'], ['Project.Id'], ondelete='CASCADE', name='FK_ProjectGroupProject_Project_ProjectId'),
    PrimaryKeyConstraint('GroupId', 'ProjectId', name='PK_ProjectGroupProject'),
    Index('IX_ProjectGroupProject_ProjectId', 'ProjectId')
)


class ProjectTask(Base):
    __tablename__ = 'ProjectTask'
    __table_args__ = (
        ForeignKeyConstraint(['ProjectId'], ['Project.Id'], ondelete='CASCADE', name='FK_ProjectTask_Project_ProjectId'),
        PrimaryKeyConstraint('Id', name='PK_ProjectTask')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ProjectId = Column(ForeignKey('Project.Id', ondelete='CASCADE'), nullable=False, index=True)
    Name = Column(Unicode, nullable=False)
    Priority = Column(Integer, nullable=False)
    PlannedStartDate = Column(DATETIME2, nullable=False)
    PlannedEndDate = Column(DATETIME2, nullable=False)
    ActualStartTime = Column(DATETIME2, nullable=False)
    ActualEndTime = Column(DATETIME2, nullable=False)
    PlannedBudget = Column(DECIMAL(18, 2), nullable=False)
    ActualBudget = Column(DECIMAL(18, 2), nullable=False)
    Description = Column(Unicode)

    Project = relationship('Project', back_populates='ProjectTask')
    ProjectActivity = relationship('ProjectActivity', back_populates='ProjectTask')


class ProjectUser(Base):
    __tablename__ = 'ProjectUser'
    __table_args__ = (
        ForeignKeyConstraint(['ProjectId'], ['Project.Id'], ondelete='CASCADE', name='FK_ProjectUser_Project_ProjectId'),
        PrimaryKeyConstraint('ProjectId', 'UserId', 'Role', name='PK_ProjectUser')
    )

    ProjectId = Column(ForeignKey('Project.Id', ondelete='CASCADE'), nullable=False)
    UserId = Column(Unicode(450), nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    Role = Column(Integer, nullable=False, server_default=text('((2))'))
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    OrganizationId = Column(Unicode, nullable=False, server_default=text("(N'')"))

    Project = relationship('Project', back_populates='ProjectUser')


class SpaceGroup(Base):
    __tablename__ = 'SpaceGroup'
    __table_args__ = (
        ForeignKeyConstraint(['ProjectId'], ['Project.Id'], ondelete='CASCADE', name='FK_SpaceGroup_Project_ProjectId'),
        PrimaryKeyConstraint('Id', name='PK_SpaceGroup')
    )

    Id = Column(Unicode(450))
    AreaPerOccupant = Column(Float(53), nullable=False)
    LastModifiedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    CreatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    OrganisationId = Column(Unicode(50), nullable=False)
    ProjectId = Column(ForeignKey('Project.Id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("(N'')"))
    Category = Column(Unicode)
    Name = Column(Unicode)
    Description = Column(Unicode)
    LastUpdatedUserId = Column(Unicode)

    Project = relationship('Project', back_populates='SpaceGroup')
    SpaceGroupSpace = relationship('SpaceGroupSpace', back_populates='SpaceGroup')


class Vehicle(Base):
    __tablename__ = 'Vehicle'
    __table_args__ = (
        ForeignKeyConstraint(['VehicleMakeId'], ['VehicleMake.Id'], ondelete='CASCADE', name='FK_Vehicle_VehicleMake_VehicleMakeId'),
        ForeignKeyConstraint(['VehicleModelId'], ['VehicleModel.Id'], name='FK_Vehicle_VehicleModel_VehicleModelId'),
        PrimaryKeyConstraint('Guid', name='PK_Vehicle')
    )

    Guid = Column(Unicode(450))
    VehicleStyle = Column(Integer, nullable=False)
    VehicleMakeId = Column(ForeignKey('VehicleMake.Id', ondelete='CASCADE'), nullable=False, index=True)
    CanBeHired = Column(Boolean, nullable=False)
    OrganisationId = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    VehicleTrim = Column(Unicode)
    VehicleModelId = Column(ForeignKey('VehicleModel.Id'), index=True)
    Description = Column(Unicode)
    ManufacturedYear = Column(Integer)
    VehicleIdentificationNumber = Column(Unicode)
    EngineNumber = Column(Unicode)
    FuelType = Column(Integer)
    EngineSize = Column(DECIMAL(18, 2))
    TransmissionType = Column(Integer)
    OdometerUnit = Column(Integer)
    Odometer = Column(DECIMAL(18, 2))
    PurchasePrice = Column(DECIMAL(18, 2))
    MarketValue = Column(DECIMAL(18, 2))
    FuelCardNumber = Column(Unicode)
    NextRegistrationDate = Column(DATETIME2)
    NextWoFDate = Column(DATETIME2)
    HireFlatCharge = Column(DECIMAL(18, 2))
    HireDistanceCharge = Column(DECIMAL(18, 2))
    ImageFileGuid = Column(Unicode)

    VehicleMake = relationship('VehicleMake', back_populates='Vehicle')
    VehicleModel = relationship('VehicleModel', back_populates='Vehicle')


class WorkOrderLifecycle(Base):
    __tablename__ = 'WorkOrderLifecycle'
    __table_args__ = (
        ForeignKeyConstraint(['AssignmentTypeId'], ['WorkOrderAssignmentType.Id'], ondelete='CASCADE', name='FK_WorkOrderLifecycle_WorkOrderAssignmentType_AssignmentTypeId'),
        ForeignKeyConstraint(['StatusId'], ['WorkOrderStatus.Id'], ondelete='CASCADE', name='FK_WorkOrderLifecycle_WorkOrderStatus_StatusId'),
        ForeignKeyConstraint(['WorkOrderGuid'], ['WorkOrder.Guid'], ondelete='CASCADE', name='FK_WorkOrderLifecycle_WorkOrder_WorkOrderGuid'),
        PrimaryKeyConstraint('Id', name='PK_WorkOrderLifecycle')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    WorkOrderGuid = Column(ForeignKey('WorkOrder.Guid', ondelete='CASCADE'), nullable=False, index=True)
    TimeStamp = Column(DateTime, nullable=False)
    StatusId = Column(ForeignKey('WorkOrderStatus.Id', ondelete='CASCADE'), nullable=False, index=True)
    AssignmentTypeId = Column(ForeignKey('WorkOrderAssignmentType.Id', ondelete='CASCADE'), nullable=False, index=True)
    AssignedBy = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    AssignedTo = Column(Integer, nullable=False)
    StatusChangedBy = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    UpdatedBy = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    UpdatedDate = Column(DateTime, nullable=False)
    Name = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False, server_default=text("('')"))
    NextLifecycle = Column(Integer)
    PreviousLifecycle = Column(Integer)

    WorkOrderAssignmentType = relationship('WorkOrderAssignmentType', back_populates='WorkOrderLifecycle')
    WorkOrderStatus = relationship('WorkOrderStatus', back_populates='WorkOrderLifecycle')
    WorkOrder = relationship('WorkOrder', back_populates='WorkOrderLifecycle')


class WorkOrderTask(Base):
    __tablename__ = 'WorkOrderTask'
    __table_args__ = (
        ForeignKeyConstraint(['CategoryId'], ['WorkOrderCategory.Id'], ondelete='CASCADE', name='FK_WorkOrderSubCategory_WorkOrderCategory_CategoryId'),
        ForeignKeyConstraint(['WorkOrderCategoryId1'], ['WorkOrderCategory.Id'], name='FK_WorkOrderSubCategory_WorkOrderCategory_WorkOrderCategoryId1'),
        PrimaryKeyConstraint('Id', name='PK_WorkOrderSubCategory')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    OrganisationGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    Name = Column(String(255, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    CategoryId = Column(ForeignKey('WorkOrderCategory.Id', ondelete='CASCADE'), nullable=False, index=True)
    Status = Column(Integer, nullable=False)
    WorkOrderCategoryId1 = Column(ForeignKey('WorkOrderCategory.Id'), index=True)

    WorkOrderCategory = relationship('WorkOrderCategory', foreign_keys=[CategoryId], back_populates='WorkOrderTask')
    WorkOrderCategory_ = relationship('WorkOrderCategory', foreign_keys=[WorkOrderCategoryId1], back_populates='WorkOrderTask_')
    Action = relationship('Action', back_populates='WorkOrderTask')
    WorkOrderVersion = relationship('WorkOrderVersion', back_populates='WorkOrderTask')


class Action(Base):
    __tablename__ = 'Action'
    __table_args__ = (
        ForeignKeyConstraint(['WorkOrderTaskId'], ['WorkOrderTask.Id'], ondelete='CASCADE', name='FK_Action_WorkOrderTask_WorkOrderTaskId'),
        ForeignKeyConstraint(['WorkOrderTypeId'], ['WorkOrderType.Id'], name='FK_Action_WorkOrderType_WorkOrderTypeId'),
        PrimaryKeyConstraint('Id', name='PK_Action')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Name = Column(Unicode, nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    UpdatedDate = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    WorkOrderTaskId = Column(ForeignKey('WorkOrderTask.Id', ondelete='CASCADE'), nullable=False, index=True, server_default=text('((0))'))
    Repeatable = Column(Integer, nullable=False, server_default=text('((0))'))
    Description = Column(Unicode)
    ParentType = Column(Unicode)
    ChildType = Column(Unicode)
    ActionCategory = Column(Unicode)
    CreatedBy = Column(Unicode)
    UpdatedBy = Column(Unicode)
    WorkOrderCategoryId = Column(Integer, index=True)
    WorkOrderTypeId = Column(ForeignKey('WorkOrderType.Id'), index=True)
    ActionSubCategory = Column(Unicode)
    ParentTypeSubset = Column(Unicode)
    ExpenseType = Column(Integer)
    Priority = Column(Integer)

    WorkOrderTask = relationship('WorkOrderTask', back_populates='Action')
    WorkOrderType = relationship('WorkOrderType', back_populates='Action')
    ActionSchedule = relationship('ActionSchedule', back_populates='Action')


class BimDataModelVersion(Base):
    __tablename__ = 'BimDataModelVersion'
    __table_args__ = (
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_BimDataModelVersion_BimDataModel_ModelId'),
        PrimaryKeyConstraint('VersionNumber', 'ModelId', name='PK_BimDataModelVersion')
    )

    VersionNumber = Column(Integer, nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True)
    CreatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    CreatedUserId = Column(Unicode(50), nullable=False)
    DataSource = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(0)))'))
    VersionCommittedTime = Column(DATETIME2)
    Remarks = Column(Unicode)

    BimDataModel = relationship('BimDataModel', back_populates='BimDataModelVersion')
    BimDataModelVersionChange = relationship('BimDataModelVersionChange', back_populates='BimDataModelVersion')
    BimDataModelVersionFile = relationship('BimDataModelVersionFile', back_populates='BimDataModelVersion')
    IfcMetaData = relationship('IfcMetaData', back_populates='BimDataModelVersion')


class CapExecutionHistoryDependency(Base):
    __tablename__ = 'CapExecutionHistoryDependency'
    __table_args__ = (
        ForeignKeyConstraint(['DependentCapId'], ['FileCapRecord.Id'], name='FK_CapExecutionHistoryDependency_FileCapRecord_DependentCapId'),
        ForeignKeyConstraint(['ExecutionId'], ['CapExecutionHistory.ExecutionId'], ondelete='CASCADE', name='FK_CapExecutionHistoryDependency_CapExecutionHistory_ExecutionId'),
        PrimaryKeyConstraint('ExecutionId', 'DependentCapId', name='PK_CapExecutionHistoryDependency')
    )

    ExecutionId = Column(ForeignKey('CapExecutionHistory.ExecutionId', ondelete='CASCADE'), nullable=False)
    DependentCapId = Column(ForeignKey('FileCapRecord.Id'), nullable=False, index=True)
    DependentCapVersion = Column(Integer, nullable=False, server_default=text('((1))'))

    FileCapRecord = relationship('FileCapRecord', back_populates='CapExecutionHistoryDependency')
    CapExecutionHistory = relationship('CapExecutionHistory', back_populates='CapExecutionHistoryDependency')


class FinAccountAnnualRecord(Base):
    __tablename__ = 'FinAccountAnnualRecord'
    __table_args__ = (
        ForeignKeyConstraint(['FinAccountId'], ['FinAccount.Id'], ondelete='CASCADE', name='FK_FinAccountAnnualRecord_FinAccount_FinAccountId'),
        ForeignKeyConstraint(['FinOrganisationId'], ['FinOrganisation.Id'], ondelete='CASCADE', name='FK_FinAccountAnnualRecord_FinOrganisation_FinOrganisationId'),
        ForeignKeyConstraint(['ProjectGuid'], ['Project.Id'], name='FK_FinAccountAnnualRecord_Project_ProjectGuid'),
        ForeignKeyConstraint(['SiteGuid'], ['Site.Id'], ondelete='CASCADE', name='FK_FinAccountAnnualRecord_Site_SiteGuid'),
        PrimaryKeyConstraint('Id', name='PK_FinAccountAnnualRecord')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    FinOrganisationId = Column(ForeignKey('FinOrganisation.Id', ondelete='CASCADE'), nullable=False, index=True)
    FinAccountId = Column(ForeignKey('FinAccount.Id', ondelete='CASCADE'), nullable=False, index=True)
    Year = Column(Integer, nullable=False)
    Balance = Column(DECIMAL(18, 2), nullable=False)
    ExpenseBudget = Column(DECIMAL(18, 2), nullable=False)
    ExpenseActual = Column(DECIMAL(18, 2), nullable=False)
    IncomeBudget = Column(DECIMAL(18, 2), nullable=False)
    IncomeActual = Column(DECIMAL(18, 2), nullable=False)
    SiteGuid = Column(ForeignKey('Site.Id', ondelete='CASCADE'), nullable=False, index=True)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    Updated = Column(DATETIME2, nullable=False)
    UpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    ProjectGuid = Column(ForeignKey('Project.Id'), index=True)

    FinAccount = relationship('FinAccount', back_populates='FinAccountAnnualRecord')
    FinOrganisation = relationship('FinOrganisation', back_populates='FinAccountAnnualRecord')
    Project = relationship('Project', back_populates='FinAccountAnnualRecord')
    Site = relationship('Site', back_populates='FinAccountAnnualRecord')


class FinAdditionalProperties(Base):
    __tablename__ = 'FinAdditionalProperties'
    __table_args__ = (
        ForeignKeyConstraint(['FinOrganisationId'], ['FinOrganisation.Id'], ondelete='CASCADE', name='FK_FinAdditionalProperties_FinOrganisation_FinOrganisationId'),
        ForeignKeyConstraint(['FinTransactionGroupId'], ['FinTransactionGroup.Id'], ondelete='CASCADE', name='FK_FinAdditionalProperties_FinTransactionGroup_FinTransactionGroupId'),
        PrimaryKeyConstraint('Id', name='PK_FinAdditionalProperties')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    FinOrganisationId = Column(ForeignKey('FinOrganisation.Id', ondelete='CASCADE'), nullable=False, index=True)
    Opex = Column(DECIMAL(18, 2), nullable=False)
    Capex = Column(DECIMAL(18, 2), nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    FinTransactionGroupId = Column(ForeignKey('FinTransactionGroup.Id', ondelete='CASCADE'), nullable=False, index=True, server_default=text('((0))'))
    ParentType = Column(Unicode)
    ParentReference = Column(Unicode)
    Closed = Column(DATETIME2)
    ClosedBy = Column(Unicode)

    FinOrganisation = relationship('FinOrganisation', back_populates='FinAdditionalProperties')
    FinTransactionGroup = relationship('FinTransactionGroup', back_populates='FinAdditionalProperties')


class FinBudget(Base):
    __tablename__ = 'FinBudget'
    __table_args__ = (
        ForeignKeyConstraint(['FinAccountId'], ['FinAccount.Id'], ondelete='CASCADE', name='FK_FinBudget_FinAccount_FinAccountId'),
        ForeignKeyConstraint(['FinOrganisationId'], ['FinOrganisation.Id'], ondelete='CASCADE', name='FK_FinBudget_FinOrganisation_FinOrganisationId'),
        PrimaryKeyConstraint('Id', name='PK_FinBudget')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    FinOrganisationId = Column(ForeignKey('FinOrganisation.Id', ondelete='CASCADE'), nullable=False, index=True)
    FinAccountId = Column(ForeignKey('FinAccount.Id', ondelete='CASCADE'), nullable=False, index=True)
    Name = Column(Unicode, nullable=False)
    Amount = Column(DECIMAL(18, 2), nullable=False)
    StartDate = Column(DATETIME2, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Disabled = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    ExpenseType = Column(Integer, nullable=False, server_default=text('((0))'))
    Description = Column(Unicode)
    ParentType = Column(Unicode)
    ParentReference = Column(Unicode)
    Discount = Column(DECIMAL(18, 2))
    TaxComponentMethod = Column(Integer)
    TaxComponentValue = Column(DECIMAL(18, 2))
    IntervalType = Column(Integer)
    Intervals = Column(Integer)
    EndDate = Column(DATETIME2)
    DisabledBy = Column(Unicode)
    GeneratorReference = Column(Unicode)
    GeneratorType = Column(Unicode)

    FinAccount = relationship('FinAccount', back_populates='FinBudget')
    FinOrganisation = relationship('FinOrganisation', back_populates='FinBudget')


class FinPayment(Base):
    __tablename__ = 'FinPayment'
    __table_args__ = (
        ForeignKeyConstraint(['FinTransactionGroupId'], ['FinTransactionGroup.Id'], ondelete='CASCADE', name='FK_FinPayment_FinTransactionGroup_FinTransactionGroupId'),
        PrimaryKeyConstraint('Id', name='PK_FinPayment')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    FinTransactionGroupId = Column(ForeignKey('FinTransactionGroup.Id', ondelete='CASCADE'), nullable=False, index=True)
    PaymentDate = Column(DATETIME2, nullable=False)
    PaymentAmount = Column(DECIMAL(18, 2), nullable=False)
    Created = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    CreatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    LastUpdated = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    LastUpdatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    Status = Column(Integer, nullable=False, server_default=text('((0))'))

    FinTransactionGroup = relationship('FinTransactionGroup', back_populates='FinPayment')


class LineItem(Base):
    __tablename__ = 'LineItem'
    __table_args__ = (
        ForeignKeyConstraint(['DefaultFinAccountId'], ['FinAccount.Id'], name='FK_LineItem_FinAccount_DefaultFinAccountId'),
        ForeignKeyConstraint(['FinOrganisationId'], ['FinOrganisation.Id'], ondelete='CASCADE', name='FK_LineItem_FinOrganisation_FinOrganisationId'),
        PrimaryKeyConstraint('Id', name='PK_LineItem')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    FinOrganisationId = Column(ForeignKey('FinOrganisation.Id', ondelete='CASCADE'), nullable=False, index=True)
    DefaultCost = Column(DECIMAL(18, 2), nullable=False)
    DefaultPrice = Column(DECIMAL(18, 2), nullable=False)
    DefaultTaxComponentMethod = Column(Integer, nullable=False)
    DefaultTaxComponentValue = Column(DECIMAL(18, 2), nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Disabled = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    Code = Column(Unicode)
    Name = Column(Unicode)
    DefaultFinAccountId = Column(ForeignKey('FinAccount.Id'), index=True)
    DisabledBy = Column(Unicode)

    FinAccount = relationship('FinAccount', back_populates='LineItem')
    FinOrganisation = relationship('FinOrganisation', back_populates='LineItem')
    FinTransaction = relationship('FinTransaction', back_populates='LineItem')
    PropertyLease = relationship('PropertyLease', back_populates='LineItem')


class MaintenanceType(Base):
    __tablename__ = 'MaintenanceType'
    __table_args__ = (
        ForeignKeyConstraint(['FinAccountId'], ['FinAccount.Id'], name='FK_MaintenanceType_FinAccount_FinAccountId'),
        PrimaryKeyConstraint('Id', name='PK_MaintenanceType')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    OrganisationId = Column(Unicode, nullable=False)
    Name = Column(Unicode, nullable=False)
    Category = Column(Integer, nullable=False)
    Term = Column(Integer, nullable=False)
    ExpenseType = Column(Integer, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)
    Description = Column(Unicode)
    FinAccountId = Column(ForeignKey('FinAccount.Id'), index=True)

    FinAccount = relationship('FinAccount', back_populates='MaintenanceType')
    LongTermMaintenanceItem = relationship('LongTermMaintenanceItem', back_populates='MaintenanceType')


class ProjectActivity(Base):
    __tablename__ = 'ProjectActivity'
    __table_args__ = (
        ForeignKeyConstraint(['TaskId'], ['ProjectTask.Id'], ondelete='CASCADE', name='FK_ProjectActivity_ProjectTask_TaskId'),
        PrimaryKeyConstraint('Id', name='PK_ProjectActivity')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    TaskId = Column(ForeignKey('ProjectTask.Id', ondelete='CASCADE'), nullable=False, index=True)
    Name = Column(Unicode, nullable=False)
    Priority = Column(Integer, nullable=False)
    PlannedStartDate = Column(DATETIME2, nullable=False)
    PlannedEndDate = Column(DATETIME2, nullable=False)
    ActualStartTime = Column(DATETIME2, nullable=False)
    ActualEndTime = Column(DATETIME2, nullable=False)
    PlannedBudget = Column(DECIMAL(18, 2), nullable=False)
    ActualBudget = Column(DECIMAL(18, 2), nullable=False)
    Description = Column(Unicode)

    ProjectTask = relationship('ProjectTask', back_populates='ProjectActivity')


class SpaceGroupSpace(Base):
    __tablename__ = 'SpaceGroupSpace'
    __table_args__ = (
        ForeignKeyConstraint(['GroupId'], ['SpaceGroup.Id'], ondelete='CASCADE', name='FK_SpaceGroupSpace_SpaceGroup_GroupId'),
        PrimaryKeyConstraint('GroupId', 'SpaceGuid', name='PK_SpaceGroupSpace')
    )

    GroupId = Column(ForeignKey('SpaceGroup.Id', ondelete='CASCADE'), nullable=False)
    SpaceGuid = Column(Unicode(450), nullable=False)

    SpaceGroup = relationship('SpaceGroup', back_populates='SpaceGroupSpace')


class WorkOrderVersion(Base):
    __tablename__ = 'WorkOrderVersion'
    __table_args__ = (
        ForeignKeyConstraint(['WorkOrderCategoryId'], ['WorkOrderCategory.Id'], name='FK_WorkOrderVersion_WorkOrderCategory_WorkOrderCategoryId'),
        ForeignKeyConstraint(['WorkOrderTaskId'], ['WorkOrderTask.Id'], name='FK_WorkOrderVersion_WorkOrderTask_WorkOrderTaskId'),
        ForeignKeyConstraint(['WorkTypeId'], ['WorkOrderType.Id'], name='FK_WorkOrderVersion_WorkOrderType_WorkTypeId'),
        PrimaryKeyConstraint('Id', name='PK_WorkOrderVersion')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    Guid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    Version = Column(Integer, nullable=False)
    DateReceived = Column(DATETIME2, nullable=False)
    DateRequired = Column(DATETIME2, nullable=False)
    RequestedBy = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    WorkOrderDescription = Column(String(collation='SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    WorkTypeId = Column(ForeignKey('WorkOrderType.Id'), nullable=False, index=True)
    CategoryId = Column(Integer, nullable=False)
    Priority = Column(Integer, nullable=False)
    SiteGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    OrderNumber = Column(Integer, nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False)
    UpdatedBy = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'), nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    SecondaryOrderNumber = Column(Integer, nullable=False, server_default=text('((0))'))
    OnHoldToDate = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    Flag = Column(Integer, nullable=False, server_default=text('((0))'))
    DueDate = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    HeathAndSafetyPermitStatus = Column(Integer, nullable=False, server_default=text('((0))'))
    OrganisationGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    TaskId = Column(Integer)
    ProjectGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    StoreyGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    SpaceGuids = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CS_AS'))
    AssetGuid = Column(String(80, 'SQL_Latin1_General_CP1_CS_AS'))
    LocationDescription = Column(String(collation='SQL_Latin1_General_CP1_CS_AS'))
    ParentGuid = Column(Unicode)
    CurrentContact = Column(Integer, server_default=text('((0))'))
    ParentType = Column(String(50, 'SQL_Latin1_General_CP1_CS_AS'))
    ExternalOrderNumber = Column(Unicode)
    ModeratorGuid = Column(Unicode)
    CostActual = Column(DECIMAL(18, 2))
    CostBudget = Column(DECIMAL(18, 2))
    CostCommitted = Column(DECIMAL(18, 2))
    ExpenseType = Column(Integer)
    ManagerGuid = Column(Unicode)
    WorkOrderCategoryId = Column(ForeignKey('WorkOrderCategory.Id'), index=True)
    WorkOrderTaskId = Column(ForeignKey('WorkOrderTask.Id'), index=True)

    WorkOrderCategory = relationship('WorkOrderCategory', back_populates='WorkOrderVersion')
    WorkOrderTask = relationship('WorkOrderTask', back_populates='WorkOrderVersion')
    WorkOrderType = relationship('WorkOrderType', back_populates='WorkOrderVersion')


class ActionSchedule(Base):
    __tablename__ = 'ActionSchedule'
    __table_args__ = (
        ForeignKeyConstraint(['ActionId'], ['Action.Id'], ondelete='CASCADE', name='FK_ActionSchedule_Action_ActionId'),
        PrimaryKeyConstraint('Id', name='PK_ActionSchedule')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    OrganisationId = Column(Unicode, nullable=False)
    ParentType = Column(Unicode, nullable=False)
    ParentReference = Column(Unicode, nullable=False)
    ActionId = Column(ForeignKey('Action.Id', ondelete='CASCADE'), nullable=False, index=True)
    StartDate = Column(DATETIME2, nullable=False)
    Repeat = Column(Integer, nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    UpdatedDate = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    ManagerGuid = Column(Unicode)
    ActorId = Column(Integer)
    Instructions = Column(Unicode)
    EndDate = Column(DATETIME2)
    LastRunDate = Column(DATETIME2)
    RepeatPeriodType = Column(Integer)
    RepeatPeriod = Column(Integer)
    CreatedBy = Column(Unicode)
    UpdatedBy = Column(Unicode)
    Data = Column(Unicode)

    Action = relationship('Action', back_populates='ActionSchedule')
    ActionScheduleEvent = relationship('ActionScheduleEvent', back_populates='ActionSchedule')


class BimDataMigration(BimDataModelVersion):
    __tablename__ = 'BimDataMigration'
    __table_args__ = (
        ForeignKeyConstraint(['VersionNumber', 'ModelId'], ['BimDataModelVersion.VersionNumber', 'BimDataModelVersion.ModelId'], name='FK_BimDataMigration_BimDataModelVersion_VersionNumber_ModelId'),
        PrimaryKeyConstraint('VersionNumber', 'ModelId', name='PK_BimDataMigration')
    )

    StartTime = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    MigrationId = Column(UNIQUEIDENTIFIER, nullable=False, unique=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    VersionNumber = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(UNIQUEIDENTIFIER, nullable=False, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    ProcessDuration = Column(BigInteger, nullable=False, server_default=text('(CONVERT([bigint],(0)))'))
    EndTime = Column(DATETIME2)
    ExecutedProcessName = Column(Unicode(50))
    ExecutedProcessOwner = Column(Unicode(100))
    ExecutedProcessVersion = Column(Unicode(15))

    Building = relationship('Building', back_populates='BimDataMigration')
    BuildingElement3DSpatialData = relationship('BuildingElement3DSpatialData', back_populates='BimDataMigration')
    BuildingElementPropertySet = relationship('BuildingElementPropertySet', back_populates='BimDataMigration')
    MiscellaneousBuildingElement = relationship('MiscellaneousBuildingElement', back_populates='BimDataMigration')
    SpaceEnclosureChild = relationship('SpaceEnclosureChild', back_populates='BimDataMigration')
    UsageClassification = relationship('UsageClassification', back_populates='BimDataMigration')
    BuildingStorey = relationship('BuildingStorey', back_populates='BimDataMigration')
    Beam = relationship('Beam', back_populates='BimDataMigration')
    Column_ = relationship('Column_', back_populates='BimDataMigration')
    OpeningContainer = relationship('OpeningContainer', back_populates='BimDataMigration')
    Ramp = relationship('Ramp', back_populates='BimDataMigration')
    Roof = relationship('Roof', back_populates='BimDataMigration')
    Slab = relationship('Slab', back_populates='BimDataMigration')
    SpatialZone = relationship('SpatialZone', back_populates='BimDataMigration')
    Stair = relationship('Stair', back_populates='BimDataMigration')
    Wall = relationship('Wall', back_populates='BimDataMigration')
    OpeningElement = relationship('OpeningElement', back_populates='BimDataMigration')
    RampFlight = relationship('RampFlight', back_populates='BimDataMigration')
    Space = relationship('Space', back_populates='BimDataMigration')
    StairFlight = relationship('StairFlight', back_populates='BimDataMigration')
    Window = relationship('Window', back_populates='BimDataMigration')
    Door = relationship('Door', back_populates='BimDataMigration')
    LightFixture = relationship('LightFixture', back_populates='BimDataMigration')
    SanitaryTerminal = relationship('SanitaryTerminal', back_populates='BimDataMigration')
    SpaceEnclosure = relationship('SpaceEnclosure', back_populates='BimDataMigration')
    WindowPanel = relationship('WindowPanel', back_populates='BimDataMigration')
    DoorPanel = relationship('DoorPanel', back_populates='BimDataMigration')
    Lamp = relationship('Lamp', back_populates='BimDataMigration')


class BimDataModelVersionChange(Base):
    __tablename__ = 'BimDataModelVersionChange'
    __table_args__ = (
        ForeignKeyConstraint(['VersionNumber', 'ModelId'], ['BimDataModelVersion.VersionNumber', 'BimDataModelVersion.ModelId'], ondelete='CASCADE', name='FK_BimDataModelVersionChange_BimDataModelVersion_VersionNumber_ModelId'),
        PrimaryKeyConstraint('VersionChangeId', name='PK_BimDataModelVersionChange'),
        Index('IX_BimDataModelVersionChange_VersionNumber_ModelId', 'VersionNumber', 'ModelId')
    )

    VersionChangeId = Column(BigInteger, Identity(start=1, increment=1))
    ModelId = Column(UNIQUEIDENTIFIER, nullable=False)
    VersionNumber = Column(Integer, nullable=False)
    ChangedElementGuid = Column(Unicode(50), nullable=False)
    ChangedElementType = Column(Integer, nullable=False)
    ChangeType = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(0)))'))
    ChangedElementAttribute = Column(Unicode)
    OldValue = Column(Unicode)

    BimDataModelVersion = relationship('BimDataModelVersion', back_populates='BimDataModelVersionChange')


class BimDataModelVersionFile(Base):
    __tablename__ = 'BimDataModelVersionFile'
    __table_args__ = (
        ForeignKeyConstraint(['VersionNumber', 'ModelId'], ['BimDataModelVersion.VersionNumber', 'BimDataModelVersion.ModelId'], ondelete='CASCADE', name='FK_BimDataModelVersionFile_BimDataModelVersion_VersionNumber_ModelId'),
        PrimaryKeyConstraint('FileId', name='PK_BimDataModelVersionFile'),
        Index('IX_BimDataModelVersionFile_VersionNumber_ModelId', 'VersionNumber', 'ModelId')
    )

    ModelId = Column(UNIQUEIDENTIFIER, nullable=False)
    VersionNumber = Column(Integer, nullable=False)
    BimModelFileType = Column(TINYINT, nullable=False)
    FileId = Column(Integer, Identity(start=1, increment=1))
    OriginalFileName = Column(Unicode)
    FileNameSuffix = Column(Unicode)

    BimDataModelVersion = relationship('BimDataModelVersion', back_populates='BimDataModelVersionFile')


class FinTransaction(Base):
    __tablename__ = 'FinTransaction'
    __table_args__ = (
        ForeignKeyConstraint(['FinAccountId'], ['FinAccount.Id'], ondelete='CASCADE', name='FK_FinTransaction_FinAccount_FinAccountId'),
        ForeignKeyConstraint(['FinOrganisationId'], ['FinOrganisation.Id'], name='FK_FinTransaction_FinOrganisation_FinOrganisationId'),
        ForeignKeyConstraint(['FinTransactionGroupId'], ['FinTransactionGroup.Id'], name='FK_FinTransaction_FinTransactionGroup_FinTransactionGroupId'),
        ForeignKeyConstraint(['LineItemId'], ['LineItem.Id'], ondelete='CASCADE', name='FK_FinTransaction_LineItem_LineItemId'),
        PrimaryKeyConstraint('Id', name='PK_FinTransaction')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    FinOrganisationId = Column(ForeignKey('FinOrganisation.Id'), nullable=False, index=True)
    FinAccountId = Column(ForeignKey('FinAccount.Id', ondelete='CASCADE'), nullable=False, index=True)
    FinTransactionGroupId = Column(ForeignKey('FinTransactionGroup.Id'), nullable=False, index=True)
    Debit = Column(DECIMAL(18, 2), nullable=False)
    Credit = Column(DECIMAL(18, 2), nullable=False)
    Name = Column(Unicode, nullable=False)
    ItemQuantity = Column(DECIMAL(18, 2), nullable=False)
    LineDiscount = Column(DECIMAL(18, 2), nullable=False)
    TaxComponentMethod = Column(Integer, nullable=False)
    TaxComponentValue = Column(DECIMAL(18, 2), nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    Disabled = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    GeneralStatus = Column(Integer, nullable=False, server_default=text('((0))'))
    LineItemId = Column(ForeignKey('LineItem.Id', ondelete='CASCADE'), nullable=False, index=True, server_default=text('((0))'))
    Description = Column(Unicode)
    ParentType = Column(Unicode)
    ParentReference = Column(Unicode)
    DisabledBy = Column(Unicode)

    FinAccount = relationship('FinAccount', back_populates='FinTransaction')
    FinOrganisation = relationship('FinOrganisation', back_populates='FinTransaction')
    FinTransactionGroup = relationship('FinTransactionGroup', back_populates='FinTransaction')
    LineItem = relationship('LineItem', back_populates='FinTransaction')


class IfcMetaData(Base):
    __tablename__ = 'IfcMetaData'
    __table_args__ = (
        ForeignKeyConstraint(['VersionNumber', 'ModelId'], ['BimDataModelVersion.VersionNumber', 'BimDataModelVersion.ModelId'], ondelete='CASCADE', name='FK_IfcMetaData_BimDataModelVersion_VersionNumber_ModelId'),
        PrimaryKeyConstraint('ModelId', 'VersionNumber', 'PropertyName', name='PK_IfcMetaData'),
        Index('IX_IfcMetaData_VersionNumber_ModelId', 'VersionNumber', 'ModelId')
    )

    ModelId = Column(UNIQUEIDENTIFIER, nullable=False)
    PropertyName = Column(Unicode(450), nullable=False)
    VersionNumber = Column(Integer, nullable=False, server_default=text('((0))'))
    PropertyValue = Column(Unicode)

    BimDataModelVersion = relationship('BimDataModelVersion', back_populates='IfcMetaData')


class LongTermMaintenanceItem(Base):
    __tablename__ = 'LongTermMaintenanceItem'
    __table_args__ = (
        ForeignKeyConstraint(['MaintenanceTypeId'], ['MaintenanceType.Id'], ondelete='CASCADE', name='FK_LongTermMaintenanceItem_MaintenanceType_MaintenanceTypeId'),
        ForeignKeyConstraint(['ProjectGuid'], ['Project.Id'], ondelete='CASCADE', name='FK_LongTermMaintenanceItem_Project_ProjectGuid'),
        ForeignKeyConstraint(['SiteGuid'], ['Site.Id'], ondelete='CASCADE', name='FK_LongTermMaintenanceItem_Site_SiteGuid'),
        PrimaryKeyConstraint('Guid', name='PK_LongTermMaintenanceItem')
    )

    Guid = Column(Unicode(450))
    OrganisationId = Column(Unicode, nullable=False)
    ProjectGuid = Column(ForeignKey('Project.Id', ondelete='CASCADE'), nullable=False, index=True)
    BuildingGuid = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    Created = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    CreatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    LastUpdated = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    LastUpdatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    MaintenanceTypeId = Column(ForeignKey('MaintenanceType.Id', ondelete='CASCADE'), nullable=False, index=True, server_default=text('((0))'))
    SiteGuid = Column(ForeignKey('Site.Id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    OpeningBalance = Column(DECIMAL(18, 2), nullable=False, server_default=text('((0.0))'))
    OpeningYear = Column(Integer, nullable=False, server_default=text('((0))'))

    MaintenanceType = relationship('MaintenanceType', back_populates='LongTermMaintenanceItem')
    Project = relationship('Project', back_populates='LongTermMaintenanceItem')
    Site = relationship('Site', back_populates='LongTermMaintenanceItem')
    LongTermMaintenanceItemAnnualBudget = relationship('LongTermMaintenanceItemAnnualBudget', back_populates='LongTermMaintenanceItem')


class PropertyLease(Base):
    __tablename__ = 'PropertyLease'
    __table_args__ = (
        ForeignKeyConstraint(['LineItemId'], ['LineItem.Id'], name='FK_PropertyLease_LineItem_LineItemId'),
        ForeignKeyConstraint(['ProjectId'], ['Project.Id'], ondelete='CASCADE', name='FK_PropertyLease_Project_ProjectId'),
        PrimaryKeyConstraint('Id', name='PK_PropertyLease')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ProjectId = Column(ForeignKey('Project.Id', ondelete='CASCADE'), nullable=False, index=True)
    Name = Column(Unicode, nullable=False)
    Description = Column(Unicode, nullable=False)
    StartDate = Column(DATETIME2, nullable=False)
    EndDate = Column(DATETIME2, nullable=False)
    RentPaymentFrequency = Column(Integer, nullable=False)
    OpexPercentage = Column(DECIMAL(18, 2), nullable=False)
    LeaseType = Column(Integer, nullable=False, server_default=text('((0))'))
    OrganisationContactId = Column(Integer, nullable=False, server_default=text('((0))'))
    PrimaryContactId = Column(Integer, nullable=False, server_default=text('((0))'))
    Created = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    CreatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    Updated = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    UpdatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    LeasePayment = Column(DECIMAL(18, 2), nullable=False, server_default=text('((0.0))'))
    LeasePaymentFrequency = Column(Integer, nullable=False, server_default=text('((0))'))
    RentPayment = Column(DECIMAL(18, 2), nullable=False, server_default=text('((0.0))'))
    RentPaymentDateFrequency = Column(Integer, nullable=False, server_default=text('((0))'))
    RentPaymentDateType = Column(Integer, nullable=False, server_default=text('((0))'))
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    LeaseExecuted = Column(Integer, nullable=False, server_default=text('((0))'))
    SiteId = Column(UNIQUEIDENTIFIER, nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    OrganisationId = Column(Unicode)
    LineItemId = Column(ForeignKey('LineItem.Id'), index=True)

    LineItem = relationship('LineItem', back_populates='PropertyLease')
    Project = relationship('Project', back_populates='PropertyLease')
    PropertyLeaseAgreement = relationship('PropertyLeaseAgreement', back_populates='PropertyLease')
    PropertyLeaseInspection = relationship('PropertyLeaseInspection', back_populates='PropertyLease')
    RentReviewDates = relationship('RentReviewDates', back_populates='PropertyLease')
    RightOfRenewalDates = relationship('RightOfRenewalDates', back_populates='PropertyLease')


class ActionScheduleEvent(Base):
    __tablename__ = 'ActionScheduleEvent'
    __table_args__ = (
        ForeignKeyConstraint(['ActionScheduleId'], ['ActionSchedule.Id'], ondelete='CASCADE', name='FK_ActionScheduleEvent_ActionSchedule_ActionScheduleId'),
        PrimaryKeyConstraint('Id', name='PK_ActionScheduleEvent')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    ActionScheduleId = Column(ForeignKey('ActionSchedule.Id', ondelete='CASCADE'), nullable=False, index=True)
    ChildType = Column(Unicode, nullable=False)
    ChildReference = Column(Unicode, nullable=False)
    StartDate = Column(DATETIME2, nullable=False)
    CreatedDate = Column(DATETIME2, nullable=False)
    UpdatedDate = Column(DATETIME2, nullable=False)
    Status = Column(Integer, nullable=False)
    EndDate = Column(DATETIME2)
    CreatedBy = Column(Unicode)
    UpdatedBy = Column(Unicode)

    ActionSchedule = relationship('ActionSchedule', back_populates='ActionScheduleEvent')


class Building(Base):
    __tablename__ = 'Building'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Building_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Building_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Building')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    ElevationOfTerrain = Column(Float(53), nullable=False)
    ElevationOfRefHeight = Column(Float(53), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    Gfa = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    Ufa = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    BuildingAddress = Column(Unicode)
    Longitude = Column(Float(53))
    Latitude = Column(Float(53))
    GeographicalLocation = Column(NullType)
    Remarks = Column(Unicode)
    BuildingNumber = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='Building')
    BimDataModel = relationship('BimDataModel', back_populates='Building')
    BuildingStorey = relationship('BuildingStorey', back_populates='Building')


class BuildingElement3DSpatialData(Base):
    __tablename__ = 'BuildingElement3DSpatialData'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_BuildingElement3DSpatialData_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_BuildingElement3DSpatialData_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_BuildingElement3DSpatialData')
    )

    BuildingElementType = Column(Integer, nullable=False, server_default=text('((0))'))
    BuildingElementGuid = Column(Unicode(450), nullable=False, index=True)
    PropertyName = Column(Unicode, nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    Guid = Column(Unicode(50), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    RawGeometryData = Column(Unicode)
    Geometry = Column(NullType)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='BuildingElement3DSpatialData')
    BimDataModel = relationship('BimDataModel', back_populates='BuildingElement3DSpatialData')


class BuildingElementPropertySet(Base):
    __tablename__ = 'BuildingElementPropertySet'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_BuildingElementPropertySet_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_BuildingElementPropertySet_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_BuildingElementPropertySet')
    )

    BuildingElementType = Column(Integer, nullable=False, server_default=text('((0))'))
    BuildingElementGuid = Column(Unicode(450), nullable=False, index=True)
    PropertyType = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(0)))'))
    PropertyName = Column(Unicode, nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    Guid = Column(Unicode(50), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    PropertyValue = Column(Unicode)
    Remarks = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='BuildingElementPropertySet')
    BimDataModel = relationship('BimDataModel', back_populates='BuildingElementPropertySet')


class LongTermMaintenanceItemAnnualBudget(Base):
    __tablename__ = 'LongTermMaintenanceItemAnnualBudget'
    __table_args__ = (
        ForeignKeyConstraint(['LongTermMaintenanceItemGuid'], ['LongTermMaintenanceItem.Guid'], ondelete='CASCADE', name='FK_LongTermMaintenanceItemAnnualBudget_LongTermMaintenanceItem_LongTermMaintenanceItemGuid'),
        PrimaryKeyConstraint('Id', name='PK_LongTermMaintenanceItemAnnualBudget')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    LongTermMaintenanceItemGuid = Column(ForeignKey('LongTermMaintenanceItem.Guid', ondelete='CASCADE'), nullable=False, index=True)
    Year = Column(Integer, nullable=False)
    ProposedAmount = Column(DECIMAL(18, 2), nullable=False)
    ActualAmount = Column(DECIMAL(18, 2), nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    LastUpdated = Column(DATETIME2, nullable=False)
    LastUpdatedBy = Column(Unicode, nullable=False)
    OrganisationId = Column(Unicode, nullable=False, server_default=text("(N'')"))

    LongTermMaintenanceItem = relationship('LongTermMaintenanceItem', back_populates='LongTermMaintenanceItemAnnualBudget')


class MiscellaneousBuildingElement(Base):
    __tablename__ = 'MiscellaneousBuildingElement'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_MiscellaneousBuildingElement_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_MiscellaneousBuildingElement_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_MiscellaneousBuildingElement')
    )

    Guid = Column(Unicode(50), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    EntityName = Column(Unicode, nullable=False)
    EntityGuid = Column(Unicode, nullable=False)
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    Remarks = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='MiscellaneousBuildingElement')
    BimDataModel = relationship('BimDataModel', back_populates='MiscellaneousBuildingElement')


class PropertyLeaseAgreement(Base):
    __tablename__ = 'PropertyLeaseAgreement'
    __table_args__ = (
        ForeignKeyConstraint(['LeaseId'], ['PropertyLease.Id'], ondelete='CASCADE', name='FK_PropertyLeaseAgreement_PropertyLease_LeaseId'),
        PrimaryKeyConstraint('Id', name='PK_PropertyLeaseAgreement')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    LeaseId = Column(ForeignKey('PropertyLease.Id', ondelete='CASCADE'), nullable=False, index=True)
    AgreementType = Column(Integer, nullable=False, server_default=text('((0))'))
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    Updated = Column(DATETIME2, nullable=False)
    UpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    Title = Column(Unicode)

    PropertyLease = relationship('PropertyLease', back_populates='PropertyLeaseAgreement')


class PropertyLeaseInspection(Base):
    __tablename__ = 'PropertyLeaseInspection'
    __table_args__ = (
        ForeignKeyConstraint(['LeaseId'], ['PropertyLease.Id'], ondelete='CASCADE', name='FK_PropertyLeaseInspection_PropertyLease_LeaseId'),
        PrimaryKeyConstraint('Id', name='PK_PropertyLeaseInspection')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    LeaseId = Column(ForeignKey('PropertyLease.Id', ondelete='CASCADE'), nullable=False, index=True)
    InspectionDate = Column(DATETIME2, nullable=False)
    Created = Column(DATETIME2, nullable=False)
    CreatedBy = Column(Unicode, nullable=False)
    Updated = Column(DATETIME2, nullable=False)
    UpdatedBy = Column(Unicode, nullable=False)
    Status = Column(Integer, nullable=False)

    PropertyLease = relationship('PropertyLease', back_populates='PropertyLeaseInspection')


class RentReviewDates(Base):
    __tablename__ = 'RentReviewDates'
    __table_args__ = (
        ForeignKeyConstraint(['LeaseId'], ['PropertyLease.Id'], ondelete='CASCADE', name='FK_RentReviewDates_PropertyLease_LeaseId'),
        PrimaryKeyConstraint('Id', name='PK_RentReviewDates')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    LeaseId = Column(ForeignKey('PropertyLease.Id', ondelete='CASCADE'), nullable=False, index=True)
    RentReview = Column(DATETIME2, nullable=False)
    AnnualRent = Column(DECIMAL(18, 2), nullable=False, server_default=text('((0.0))'))
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    Created = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    CreatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    Updated = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    UpdatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    Active = Column(Integer, nullable=False, server_default=text('((0))'))

    PropertyLease = relationship('PropertyLease', back_populates='RentReviewDates')


class RightOfRenewalDates(Base):
    __tablename__ = 'RightOfRenewalDates'
    __table_args__ = (
        ForeignKeyConstraint(['LeaseId'], ['PropertyLease.Id'], ondelete='CASCADE', name='FK_RightOfRenewalDates_PropertyLease_LeaseId'),
        PrimaryKeyConstraint('Id', name='PK_RightOfRenewalDates')
    )

    Id = Column(Integer, Identity(start=1, increment=1))
    LeaseId = Column(ForeignKey('PropertyLease.Id', ondelete='CASCADE'), nullable=False, index=True)
    RightOfRenewal = Column(DATETIME2, nullable=False)
    Created = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    CreatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    Updated = Column(DATETIME2, nullable=False, server_default=text("('0001-01-01T00:00:00.0000000')"))
    UpdatedBy = Column(Unicode, nullable=False, server_default=text("(N'')"))
    Status = Column(Integer, nullable=False, server_default=text('((0))'))

    PropertyLease = relationship('PropertyLease', back_populates='RightOfRenewalDates')


class SpaceEnclosureChild(Base):
    __tablename__ = 'SpaceEnclosureChild'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_SpaceEnclosureChild_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_SpaceEnclosureChild_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_SpaceEnclosureChild')
    )

    Guid = Column(Unicode(50), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True)
    ParentObjectGuid = Column(Unicode(50), nullable=False)
    ParentRelationshipType = Column(Integer, nullable=False, server_default=text('((21))'))
    BuildingElementType = Column(Integer, nullable=False, server_default=text('((0))'))
    GlazingArea = Column(Float(53), nullable=False)
    Area = Column(Float(53), nullable=False)
    Orientation = Column(TINYINT, nullable=False, server_default=text('(CONVERT([tinyint],(0)))'))
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    BuildingElementGuid = Column(Unicode(50))
    Remarks = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='SpaceEnclosureChild')
    BimDataModel = relationship('BimDataModel', back_populates='SpaceEnclosureChild')


class UsageClassification(Base):
    __tablename__ = 'UsageClassification'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_UsageClassification_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_UsageClassification_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_UsageClassification')
    )

    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    BuildingElementType = Column(Unicode, nullable=False, server_default=text("(N'UNKNOWN')"))
    PredefinedType = Column(Unicode, nullable=False, server_default=text("(N'NOT_DEFINED')"))
    PredefinedName = Column(Unicode, nullable=False, server_default=text("(N'NOT_DEFINED')"))
    PredefinedValue = Column(Unicode, nullable=False, server_default=text("(N'NOT_DEFINED')"))
    Status = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    Guid = Column(Unicode(50), nullable=False, server_default=text("(N'')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    Remarks = Column(Unicode)
    BuildingElementGuid = Column(Unicode)
    UserDefinedName = Column(Unicode)
    UserDefinedValue = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='UsageClassification')
    BimDataModel = relationship('BimDataModel', back_populates='UsageClassification')


class BuildingStorey(Base):
    __tablename__ = 'BuildingStorey'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingGuid', 'ModelId'], ['Building.Guid', 'Building.ModelId'], name='FK_BuildingStorey_Building_BuildingGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_BuildingStorey_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_BuildingStorey_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_BuildingStorey'),
        Index('IX_BuildingStorey_BuildingGuid_ModelId', 'BuildingGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    Elevation = Column(Float(53), nullable=False)
    NetHeight = Column(Float(53), nullable=False)
    GrossHeight = Column(Float(53), nullable=False)
    GrossFloorArea = Column(Float(53), nullable=False)
    GrossPerimeter = Column(Float(53), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    BuildingGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    Building = relationship('Building', back_populates='BuildingStorey')
    BimDataMigration = relationship('BimDataMigration', back_populates='BuildingStorey')
    BimDataModel = relationship('BimDataModel', back_populates='BuildingStorey')
    Beam = relationship('Beam', back_populates='BuildingStorey')
    Column_ = relationship('Column_', back_populates='BuildingStorey')
    OpeningContainer = relationship('OpeningContainer', back_populates='BuildingStorey')
    Ramp = relationship('Ramp', back_populates='BuildingStorey')
    Roof = relationship('Roof', back_populates='BuildingStorey')
    Slab = relationship('Slab', back_populates='BuildingStorey')
    SpatialZone = relationship('SpatialZone', back_populates='BuildingStorey')
    Stair = relationship('Stair', back_populates='BuildingStorey')
    Wall = relationship('Wall', back_populates='BuildingStorey')
    Space = relationship('Space', back_populates='BuildingStorey')
    Window = relationship('Window', back_populates='BuildingStorey')
    Door = relationship('Door', back_populates='BuildingStorey')


class Beam(Base):
    __tablename__ = 'Beam'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_Beam_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Beam_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Beam_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Beam'),
        Index('IX_Beam_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    IsExternal = Column(Boolean, nullable=False)
    HasOpening = Column(Boolean, nullable=False)
    Length = Column(Float(53), nullable=False)
    CrossSectionArea = Column(Float(53), nullable=False)
    OuterSurfaceArea = Column(Float(53), nullable=False)
    NetWeight = Column(Float(53), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    BuildingStoreyGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='Beam')
    BimDataMigration = relationship('BimDataMigration', back_populates='Beam')
    BimDataModel = relationship('BimDataModel', back_populates='Beam')


class Column_(Base):
    __tablename__ = 'Column'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_Column_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Column_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Column_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Column'),
        Index('IX_Column_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    IsExternal = Column(Boolean, nullable=False)
    Length = Column(Float(53), nullable=False)
    CrossSectionArea = Column(Float(53), nullable=False)
    OuterSurfaceArea = Column(Float(53), nullable=False)
    NetWeight = Column(Float(53), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    BuildingStoreyGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='Column_')
    BimDataMigration = relationship('BimDataMigration', back_populates='Column_')
    BimDataModel = relationship('BimDataModel', back_populates='Column_')


class OpeningContainer(Base):
    __tablename__ = 'OpeningContainer'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_OpeningContainer_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_OpeningContainer_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_OpeningContainer_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_OpeningContainer'),
        Index('IX_OpeningContainer_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    ContainerType = Column(Integer, nullable=False, server_default=text('((0))'))
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    Width = Column(Float(53), nullable=False)
    Height = Column(Float(53), nullable=False)
    Area = Column(Float(53), nullable=False)
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    BuildingStoreyGuid = Column(Unicode(50))
    ContainerGuid = Column(Unicode)
    ContainerElementValue = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='OpeningContainer')
    BimDataMigration = relationship('BimDataMigration', back_populates='OpeningContainer')
    BimDataModel = relationship('BimDataModel', back_populates='OpeningContainer')
    OpeningElement = relationship('OpeningElement', back_populates='OpeningContainer')
    Window = relationship('Window', back_populates='OpeningContainer')
    Door = relationship('Door', back_populates='OpeningContainer')


class Ramp(Base):
    __tablename__ = 'Ramp'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_Ramp_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Ramp_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Ramp_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Ramp'),
        Index('IX_Ramp_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    IsExternal = Column(Boolean, nullable=False, server_default=text('(CONVERT([bit],(0)))'))
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    BuildingStoreyGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='Ramp')
    BimDataMigration = relationship('BimDataMigration', back_populates='Ramp')
    BimDataModel = relationship('BimDataModel', back_populates='Ramp')
    RampFlight = relationship('RampFlight', back_populates='Ramp')


class Roof(Base):
    __tablename__ = 'Roof'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_Roof_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Roof_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Roof_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Roof'),
        Index('IX_Roof_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    GrossArea = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    HasOpening = Column(Boolean, nullable=False, server_default=text('(CONVERT([bit],(0)))'))
    NetArea = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    BuildingStoreyGuid = Column(Unicode(50))
    Origin = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='Roof')
    BimDataMigration = relationship('BimDataMigration', back_populates='Roof')
    BimDataModel = relationship('BimDataModel', back_populates='Roof')


class Slab(Base):
    __tablename__ = 'Slab'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_Slab_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Slab_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Slab_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Slab'),
        Index('IX_Slab_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    IsExternal = Column(Boolean, nullable=False)
    HasOpening = Column(Boolean, nullable=False)
    Thickness = Column(Float(53), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    GrossArea = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    NetArea = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    Volume = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    BuildingStoreyGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='Slab')
    BimDataMigration = relationship('BimDataMigration', back_populates='Slab')
    BimDataModel = relationship('BimDataModel', back_populates='Slab')


class SpatialZone(Base):
    __tablename__ = 'SpatialZone'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_SpatialZone_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_SpatialZone_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_SpatialZone_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_SpatialZone'),
        Index('IX_SpatialZone_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    IsExternal = Column(Boolean, nullable=False)
    FloorArea = Column(Float(53), nullable=False)
    Volume = Column(Float(53), nullable=False)
    AreaPerOccupant = Column(Float(53), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    BuildingStoreyGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='SpatialZone')
    BimDataMigration = relationship('BimDataMigration', back_populates='SpatialZone')
    BimDataModel = relationship('BimDataModel', back_populates='SpatialZone')
    Space = relationship('Space', back_populates='SpatialZone')


class Stair(Base):
    __tablename__ = 'Stair'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_Stair_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Stair_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Stair_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Stair'),
        Index('IX_Stair_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    IsExternal = Column(Boolean, nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    BottomElevation = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    TopElevation = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    BuildingStoreyGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='Stair')
    BimDataMigration = relationship('BimDataMigration', back_populates='Stair')
    BimDataModel = relationship('BimDataModel', back_populates='Stair')
    StairFlight = relationship('StairFlight', back_populates='Stair')


class Wall(Base):
    __tablename__ = 'Wall'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_Wall_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Wall_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Wall_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Wall'),
        Index('IX_Wall_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    IsExternal = Column(Boolean, nullable=False)
    HasOpening = Column(Boolean, nullable=False)
    Length = Column(Float(53), nullable=False)
    Height = Column(Float(53), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    Area = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    Thickness = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    Weight = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    Volume = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Orientation = Column(Integer, nullable=False, server_default=text('((0))'))
    OrientationAngle = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    BuildingStoreyGuid = Column(Unicode(50))
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    Remarks = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='Wall')
    BimDataMigration = relationship('BimDataMigration', back_populates='Wall')
    BimDataModel = relationship('BimDataModel', back_populates='Wall')


class OpeningElement(Base):
    __tablename__ = 'OpeningElement'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_OpeningElement_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_OpeningElement_BimDataModel_ModelId'),
        ForeignKeyConstraint(['OpeningContainerGuid', 'ModelId'], ['OpeningContainer.Guid', 'OpeningContainer.ModelId'], name='FK_OpeningElement_OpeningContainer_OpeningContainerGuid_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_OpeningElement'),
        Index('IX_OpeningElement_OpeningContainerGuid_ModelId', 'OpeningContainerGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    Width = Column(Float(53), nullable=False)
    Height = Column(Float(53), nullable=False)
    ContainerElementType = Column(Integer, nullable=False, server_default=text('((0))'))
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    Area = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    IsExternal = Column(Boolean, nullable=False, server_default=text('(CONVERT([bit],(0)))'))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    Remarks = Column(Unicode)
    OpeningContainerGuid = Column(Unicode(50))
    Origin = Column(NullType)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='OpeningElement')
    BimDataModel = relationship('BimDataModel', back_populates='OpeningElement')
    OpeningContainer = relationship('OpeningContainer', back_populates='OpeningElement')


class RampFlight(Base):
    __tablename__ = 'RampFlight'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_RampFlight_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_RampFlight_BimDataModel_ModelId'),
        ForeignKeyConstraint(['RampGuid', 'ModelId'], ['Ramp.Guid', 'Ramp.ModelId'], name='FK_RampFlight_Ramp_RampGuid_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_RampFlight'),
        Index('IX_RampFlight_RampGuid_ModelId', 'RampGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    IsExternal = Column(Boolean, nullable=False)
    Length = Column(Float(53), nullable=False)
    ClearWidth = Column(Float(53), nullable=False)
    Slope = Column(Float(53), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    RampGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='RampFlight')
    BimDataModel = relationship('BimDataModel', back_populates='RampFlight')
    Ramp = relationship('Ramp', back_populates='RampFlight')


class Space(Base):
    __tablename__ = 'Space'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_Space_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Space_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Space_BimDataModel_ModelId'),
        ForeignKeyConstraint(['SpatialZoneGuid', 'ModelId'], ['SpatialZone.Guid', 'SpatialZone.ModelId'], name='FK_Space_SpatialZone_SpatialZoneGuid_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Space'),
        Index('IX_Space_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId'),
        Index('IX_Space_SpatialZoneGuid_ModelId', 'SpatialZoneGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    IsExternal = Column(Boolean, nullable=False)
    AverageHeight = Column(Float(53), nullable=False)
    FinishedFloorHeight = Column(Float(53), nullable=False)
    Elevation = Column(Float(53), nullable=False)
    NetPerimeter = Column(Float(53), nullable=False)
    GrossPerimeter = Column(Float(53), nullable=False)
    FloorArea = Column(Float(53), nullable=False)
    Volume = Column(Float(53), nullable=False)
    WallArea = Column(Float(53), nullable=False)
    SurfaceArea = Column(Float(53), nullable=False)
    AreaPerOccupant = Column(Float(53), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    BuildingStoreyGuid = Column(Unicode(50))
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    Remarks = Column(Unicode)
    SpatialZoneGuid = Column(Unicode(50))
    Function = Column(Unicode)
    SpaceNumber = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='Space')
    BimDataMigration = relationship('BimDataMigration', back_populates='Space')
    BimDataModel = relationship('BimDataModel', back_populates='Space')
    SpatialZone = relationship('SpatialZone', back_populates='Space')
    Door = relationship('Door', foreign_keys='[Door.OpeningFromSpaceGuid, Door.ModelId]', back_populates='Space')
    Door_ = relationship('Door', foreign_keys='[Door.OpeningIntoSpaceGuid, Door.ModelId]', back_populates='Space_')
    LightFixture = relationship('LightFixture', back_populates='Space')
    SanitaryTerminal = relationship('SanitaryTerminal', back_populates='Space')
    SpaceEnclosure = relationship('SpaceEnclosure', back_populates='Space')


class StairFlight(Base):
    __tablename__ = 'StairFlight'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_StairFlight_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_StairFlight_BimDataModel_ModelId'),
        ForeignKeyConstraint(['StairGuid', 'ModelId'], ['Stair.Guid', 'Stair.ModelId'], name='FK_StairFlight_Stair_StairGuid_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_StairFlight'),
        Index('IX_StairFlight_StairGuid_ModelId', 'StairGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    IsExternal = Column(Boolean, nullable=False)
    Length = Column(Float(53), nullable=False)
    NumberOfRisers = Column(Integer, nullable=False)
    NumberOfThreads = Column(Integer, nullable=False)
    RiserHeight = Column(Float(53), nullable=False)
    ThreadLength = Column(Float(53), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    StairGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='StairFlight')
    BimDataModel = relationship('BimDataModel', back_populates='StairFlight')
    Stair = relationship('Stair', back_populates='StairFlight')


class Window(Base):
    __tablename__ = 'Window'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_Window_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Window_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Window_BimDataModel_ModelId'),
        ForeignKeyConstraint(['OpeningContainerGuid', 'ModelId'], ['OpeningContainer.Guid', 'OpeningContainer.ModelId'], name='FK_Window_OpeningContainer_OpeningContainerGuid_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Window'),
        Index('IX_Window_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId'),
        Index('IX_Window_OpeningContainerGuid_ModelId', 'OpeningContainerGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    IsExternal = Column(Boolean, nullable=False)
    Thickness = Column(Float(53), nullable=False)
    Area = Column(Float(53), nullable=False)
    PartitioningType = Column(Integer, nullable=False, server_default=text('((0))'))
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Height = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    LintelHeight = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    Width = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    Remarks = Column(Unicode)
    OpeningContainerGuid = Column(Unicode(50))
    BuildingStoreyGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='Window')
    BimDataMigration = relationship('BimDataMigration', back_populates='Window')
    BimDataModel = relationship('BimDataModel', back_populates='Window')
    OpeningContainer = relationship('OpeningContainer', back_populates='Window')
    WindowPanel = relationship('WindowPanel', back_populates='Window')


class Door(Base):
    __tablename__ = 'Door'
    __table_args__ = (
        ForeignKeyConstraint(['BuildingStoreyGuid', 'ModelId'], ['BuildingStorey.Guid', 'BuildingStorey.ModelId'], name='FK_Door_BuildingStorey_BuildingStoreyGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Door_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Door_BimDataModel_ModelId'),
        ForeignKeyConstraint(['OpeningContainerGuid', 'ModelId'], ['OpeningContainer.Guid', 'OpeningContainer.ModelId'], name='FK_Door_OpeningContainer_OpeningContainerGuid_ModelId'),
        ForeignKeyConstraint(['OpeningFromSpaceGuid', 'ModelId'], ['Space.Guid', 'Space.ModelId'], name='FK_Door_Space_OpeningFromSpaceGuid_ModelId'),
        ForeignKeyConstraint(['OpeningIntoSpaceGuid', 'ModelId'], ['Space.Guid', 'Space.ModelId'], name='FK_Door_Space_OpeningIntoSpaceGuid_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Door'),
        Index('IX_Door_BuildingStoreyGuid_ModelId', 'BuildingStoreyGuid', 'ModelId'),
        Index('IX_Door_OpeningContainerGuid_ModelId', 'OpeningContainerGuid', 'ModelId'),
        Index('IX_Door_OpeningFromSpaceGuid_ModelId', 'OpeningFromSpaceGuid', 'ModelId'),
        Index('IX_Door_OpeningIntoSpaceGuid_ModelId', 'OpeningIntoSpaceGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    IsExternal = Column(Boolean, nullable=False)
    Width = Column(Float(53), nullable=False)
    Height = Column(Float(53), nullable=False)
    OperationType = Column(Integer, nullable=False, server_default=text('((0))'))
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Name = Column(Unicode)
    LongName = Column(Unicode)
    Description = Column(Unicode)
    Remarks = Column(Unicode)
    OpeningIntoSpaceGuid = Column(Unicode(50))
    OpeningContainerGuid = Column(Unicode(50))
    Origin = Column(NullType)
    BuildingStoreyGuid = Column(Unicode(50))
    OpeningFromSpaceGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BuildingStorey = relationship('BuildingStorey', back_populates='Door')
    BimDataMigration = relationship('BimDataMigration', back_populates='Door')
    BimDataModel = relationship('BimDataModel', back_populates='Door')
    OpeningContainer = relationship('OpeningContainer', back_populates='Door')
    Space = relationship('Space', foreign_keys=[OpeningFromSpaceGuid, ModelId], back_populates='Door')
    Space_ = relationship('Space', foreign_keys=[OpeningIntoSpaceGuid, ModelId], back_populates='Door_')
    DoorPanel = relationship('DoorPanel', back_populates='Door')


class LightFixture(Base):
    __tablename__ = 'LightFixture'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_LightFixture_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_LightFixture_BimDataModel_ModelId'),
        ForeignKeyConstraint(['SpaceGuid', 'ModelId'], ['Space.Guid', 'Space.ModelId'], name='FK_LightFixture_Space_SpaceGuid_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_LightFixture'),
        Index('IX_LightFixture_SpaceGuid_ModelId', 'SpaceGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    SpaceGuid = Column(Unicode(50))
    Description = Column(Unicode)
    LongName = Column(Unicode)
    Name = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='LightFixture')
    BimDataModel = relationship('BimDataModel', back_populates='LightFixture')
    Space = relationship('Space', back_populates='LightFixture')
    Lamp = relationship('Lamp', back_populates='LightFixture')


class SanitaryTerminal(Base):
    __tablename__ = 'SanitaryTerminal'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_SanitaryTerminal_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_SanitaryTerminal_BimDataModel_ModelId'),
        ForeignKeyConstraint(['SpaceGuid', 'ModelId'], ['Space.Guid', 'Space.ModelId'], name='FK_SanitaryTerminal_Space_SpaceGuid_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_SanitaryTerminal'),
        Index('IX_SanitaryTerminal_SpaceGuid_ModelId', 'SpaceGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    SpaceGuid = Column(Unicode(50))
    Description = Column(Unicode)
    LongName = Column(Unicode)
    Name = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='SanitaryTerminal')
    BimDataModel = relationship('BimDataModel', back_populates='SanitaryTerminal')
    Space = relationship('Space', back_populates='SanitaryTerminal')


class SpaceEnclosure(Base):
    __tablename__ = 'SpaceEnclosure'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_SpaceEnclosure_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_SpaceEnclosure_BimDataModel_ModelId'),
        ForeignKeyConstraint(['SpaceGuid', 'ModelId'], ['Space.Guid', 'Space.ModelId'], name='FK_SpaceEnclosure_Space_SpaceGuid_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_SpaceEnclosure'),
        Index('IX_SpaceEnclosure_SpaceGuid_ModelId', 'SpaceGuid', 'ModelId')
    )

    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    BuildingElementType = Column(Integer, nullable=False, server_default=text('((0))'))
    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Area = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    GlazingArea = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    IsExternal = Column(Boolean, nullable=False, server_default=text('(CONVERT([bit],(0)))'))
    SpaceGuid = Column(Unicode(50))
    Remarks = Column(Unicode)
    BuildingElementGuid = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='SpaceEnclosure')
    BimDataModel = relationship('BimDataModel', back_populates='SpaceEnclosure')
    Space = relationship('Space', back_populates='SpaceEnclosure')


class WindowPanel(Base):
    __tablename__ = 'WindowPanel'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_WindowPanel_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_WindowPanel_BimDataModel_ModelId'),
        ForeignKeyConstraint(['WindowGuid', 'ModelId'], ['Window.Guid', 'Window.ModelId'], name='FK_WindowPanel_Window_WindowGuid_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_WindowPanel'),
        Index('IX_WindowPanel_WindowGuid_ModelId', 'WindowGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    OperationType = Column(Integer, nullable=False, server_default=text('((0))'))
    PanelPosition = Column(Integer, nullable=False, server_default=text('((0))'))
    FrameDepth = Column(Float(53), nullable=False)
    FrameThickness = Column(Float(53), nullable=False)
    Width = Column(Float(53), nullable=False)
    Height = Column(Float(53), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    WindowGuid = Column(Unicode(50))
    Remarks = Column(Unicode)
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='WindowPanel')
    BimDataModel = relationship('BimDataModel', back_populates='WindowPanel')
    Window = relationship('Window', back_populates='WindowPanel')


class DoorPanel(Base):
    __tablename__ = 'DoorPanel'
    __table_args__ = (
        ForeignKeyConstraint(['DoorGuid', 'ModelId'], ['Door.Guid', 'Door.ModelId'], name='FK_DoorPanel_Door_DoorGuid_ModelId'),
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_DoorPanel_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_DoorPanel_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_DoorPanel'),
        Index('IX_DoorPanel_DoorGuid_ModelId', 'DoorGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    OperationType = Column(Integer, nullable=False, server_default=text('((0))'))
    PanelPosition = Column(Integer, nullable=False, server_default=text('((0))'))
    PanelWidth = Column(Float(53), nullable=False)
    Width = Column(Float(53), nullable=False)
    Height = Column(Float(53), nullable=False)
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    PanelHeight = Column(Float(53), nullable=False, server_default=text('((0.0000000000000000e+000))'))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    DoorGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    Door = relationship('Door', back_populates='DoorPanel')
    BimDataMigration = relationship('BimDataMigration', back_populates='DoorPanel')
    BimDataModel = relationship('BimDataModel', back_populates='DoorPanel')


class Lamp(Base):
    __tablename__ = 'Lamp'
    __table_args__ = (
        ForeignKeyConstraint(['LastUpdatedMigrationId'], ['BimDataMigration.MigrationId'], ondelete='SET NULL', name='FK_Lamp_BimDataMigration_LastUpdatedMigrationId'),
        ForeignKeyConstraint(['LightFixtureGuid', 'ModelId'], ['LightFixture.Guid', 'LightFixture.ModelId'], name='FK_Lamp_LightFixture_LightFixtureGuid_ModelId'),
        ForeignKeyConstraint(['ModelId'], ['BimDataModel.ModelId'], ondelete='CASCADE', name='FK_Lamp_BimDataModel_ModelId'),
        PrimaryKeyConstraint('Guid', 'ModelId', name='PK_Lamp'),
        Index('IX_Lamp_LightFixtureGuid_ModelId', 'LightFixtureGuid', 'ModelId')
    )

    Guid = Column(Unicode(50), nullable=False)
    LastUpdatedDate = Column(DATETIME2, nullable=False, server_default=text('(getdate())'))
    LastUpdatedUserId = Column(Unicode(50), nullable=False)
    PredefinedType = Column(Integer, nullable=False, server_default=text('((0))'))
    ModelId = Column(ForeignKey('BimDataModel.ModelId', ondelete='CASCADE'), nullable=False, index=True, server_default=text("('00000000-0000-0000-0000-000000000000')"))
    LastUpdatedVersion = Column(Integer, nullable=False, server_default=text('((1))'))
    SysStartTime = Column(DATETIME2, nullable=False)
    SysEndTime = Column(DATETIME2, nullable=False)
    Remarks = Column(Unicode)
    LightFixtureGuid = Column(Unicode(50))
    LastUpdatedMigrationId = Column(ForeignKey('BimDataMigration.MigrationId', ondelete='SET NULL'), index=True)

    BimDataMigration = relationship('BimDataMigration', back_populates='Lamp')
    LightFixture = relationship('LightFixture', back_populates='Lamp')
    BimDataModel = relationship('BimDataModel', back_populates='Lamp')
