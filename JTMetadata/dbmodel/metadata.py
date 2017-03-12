

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine

metadata = MetaData()

infaWorkflows = Table('infaWorkflows', metadata,
           Column('workflowId', Integer, primary_key=True),
           Column('workflowName',String(100)),
           Column('workflowParamId',Integer )
           )

infaWorkflowParams = Table('infaWorkflowParams', metadata,
           Column('workflowParamid', Integer, primary_key=True),
           Column('workflowId', Integer, ForeignKey('infaWorkflows.workflowId')),
           Column('paramName', String(100)),
           Column('paramValue',String(500))
           )

#engine = create_engine('oracle+cx_oracle://jtorchestrator:admin@127.0.0.1:1521/xe',echo=True)
#metadata.create_all(engine)

