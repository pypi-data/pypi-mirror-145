from dataclasses import Field
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class DatalakeSchema(BaseModel):
    id: str = Field(alias='datalake_id')

class OrganizationSchema(BaseModel):
    id: str = Field(alias='organization_id')
    name: str = Field(alias='organization_name')
class DatasetSchema(BaseModel):
    id: str = Field(alias='dataset_id')
    name: str = Field(alias='dataset_name')
    version: str = Field(alias='version')

class ModelSchema(BaseModel):
    id: str = Field(alias='model_id')
    name: str = Field(alias='network_name')
    type: str = Field(alias='type')

class ProjectSchema(BaseModel):
    id: str = Field(alias='project_id')
    name: str = Field(alias='project_name')

class DeploymentSchema(BaseModel):
    id: str = Field(alias='pk')
    name: str = Field(alias='name')
    oracle_host: Optional[str] = Field(default=None, alias='oracle_url')
    serving_host: Optional[str] = Field(default=None, alias='serving_url')

class DataSchema(BaseModel):
    picture_id: str = Field(alias='picture_id')
    external_url: str = Field(alias='external_url')
    internal_key: str = Field(alias='internal_key')

class PictureSchema(BaseModel):
    picture_id: str = Field(alias='picture_id')
    external_url: str = Field(alias='external_url')
    internal_key: str = Field(alias='internal_key')
    width: int = Field(alias='width')
    height: int = Field(alias='height')
    tags: Optional[List[str]] = Field(default=None, alias='tag')

class ExperimentSchema(BaseModel):
    id: str = Field(alias='id')
    name: str = Field(alias='name')
    files: Optional[List[dict]] = Field(default=[], alias='files')

class UserSchema(BaseModel):
    username: str = Field(alias='username')

class WorkerSchema(BaseModel):
    id: str = Field(alias='pk')
    user: UserSchema = Field(alias='user')

class ScanSchema(BaseModel):
    id: str = Field(alias='id')
    name: str = Field(alias='name')

class RunSchema(BaseModel):
    id: str = Field(alias='id') 
    config: dict = Field(alias='config') 
    requirements: List[dict] = Field(default=[], alias='requirements') 
    script: Optional[str] = Field(default=None, alias='script') 
    script_object_name: Optional[str] = Field(default=None, alias='script_object_name') 
