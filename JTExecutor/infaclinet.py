

from zeep import Client



class InfaWSHClient():
    
    def __init__(self,infaDomain,infaRepo,infaIntegrationService,infaUserName,infaUserPassword,infaSecurityDomain,MetadataWSDL,DataIntegrationWSDL):
    
        self.infaDomain = infaDomain
        self.infaRepo = infaRepo
        self.infaIntegrationService = infaIntegrationService
      
        self.metadata = Client(MetadataWSDL)
        self.dataIntegration = Client(DataIntegrationWSDL)
               
        self.soapHeader = self.metadata.service.login(RepositoryDomainName=self.infaDomain,
                                                       RepositoryName=self.infaRepo,
                                                       UserName=infaUserName,
                                                       Password=infaUserPassword,
                                                       UserNameSpace=infaSecurityDomain)['header']
        
      

    def startWorkflow(self,infaFolder,infaWorkflowName,infaWorkflowRunId='',infaWorkflowRunInstanceName='',infaParameterFileName='',infaParameters=''):
                
        self.dataIntegration.service.startWorkflow(_soapheaders=[self.soapHeader],
                                                   DIServiceInfo = {'ServiceName':self.infaIntegrationService,
                                                                    'DomainName':self.infaDomain},
                                                   FolderName=infaFolder,
                                                   WorkflowName=infaWorkflowName,
                                                   WorkflowRunId=infaWorkflowRunId,
                                                   WorkflowRunInstanceName=infaWorkflowRunInstanceName,                                                                
                                                   ParameterFileName=infaParameterFileName,
                                                   Parameters=[infaParameters],
                                                   RequestMode='NORMAL',
                                                   IsAbort='false')
        
        #result = self.getWorkflowDetails(infaFolder,infaWorkflowName,infaWorkflowRunId,infaWorkflowRunInstanceName)        
        #return result 
    
    
    def getWorkflowDetails(self,infaFolder,infaWorkflowName,infaWorkflowRunId='',infaWorkflowRunInstanceName=''):
        
        result = self.dataIntegration.service.getWorkflowDetails(_soapheaders=[self.soapHeader],
                                                                 DIServiceInfo = {'ServiceName':self.infaIntegrationService,
                                                                                  'DomainName':self.infaDomain},
                                                                 FolderName=infaFolder,
                                                                 WorkflowName=infaWorkflowName,
                                                                 WorkflowRunId=infaWorkflowRunId,
                                                                 WorkflowRunInstanceName=infaWorkflowRunInstanceName,                                                                 
                                                                 RequestMode='NORMAL',
                                                                 IsAbort='false'
                                                                 )
        return result
    
    
    def getWorkflowDetailsEx(self,infaFolder,infaWorkflowName,infaWorkflowRunId='',infaWorkflowRunInstanceName=''):
        
        result = self.dataIntegration.service.getWorkflowDetailsEx(_soapheaders=[self.soapHeader],
                                                                 DIServiceInfo = {'ServiceName':self.infaIntegrationService,
                                                                                  'DomainName':self.infaDomain},
                                                                 FolderName=infaFolder,
                                                                 WorkflowName=infaWorkflowName,
                                                                 WorkflowRunId=infaWorkflowRunId,
                                                                 WorkflowRunInstanceName=infaWorkflowRunInstanceName,
                                                                 )
        return result
    
    
    def getAllFolders(self):
        
        result = self.metadata.service.getAllFolders(_soapheaders=[self.soapHeader])
        
        return result
    
    def logout(self):
        
         self.metadata.service.logout(_soapheaders=[self.soapHeader])








'''
x = InfaWSHClient(infaDomain='Domain_DESKTOP-JTBO5ON',
                  infaRepo='infa_repo',
                  infaIntegrationService='infa_is',
                  DataIntegrationWSDL='http://localhost:7333/wsh/services/BatchServices/DataIntegration?WSDL',
                  MetadataWSDL='http://localhost:7333/wsh/services/BatchServices/Metadata?WSDL',
                  infaUserName='Administrator',
                  infaUserPassword='admin',
                  infaSecurityDomain='Native')


inParams = {'Parameters':[{'Scope':'global',
                           'Name':'$$VAR1',
                           'Value':'thisismeVAR1'},
                          {'Scope':'global',
                           'Name':'$$VAR2',
                           'Value':'thisismeVAR2'}
                          ]}

a = x.startWorkflow(infaFolder='folder',infaWorkflowName='wf_iWSH',infaParameters=inParams) 
a = x.getWorkflowDetails(infaFolder='folder',infaWorkflowName='wf_iWSH')

''' 
