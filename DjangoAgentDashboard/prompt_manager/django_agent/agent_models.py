from pydantic import BaseModel

# Project
class DjangoAppPlan(BaseModel):
    name: str
    models: list[str]
    views: list[str]


class DjangoProjectPlan(BaseModel):
    project_name: str
    apps: list[DjangoAppPlan]


# Models
class ModelOutput(BaseModel):
    app: str
    model:  str
    code:   str


class ModelsOutput(BaseModel):
    models: list[ModelOutput]


# Templates
class TemplateOutput(BaseModel):
    view: str
    html: str


class TemplatesOutput(BaseModel):
    templates: list[TemplateOutput]


# Views
class ViewOutput(BaseModel):
    app: str
    view: str
    code: str

class ViewsOutput(BaseModel):
    views: list[ViewOutput]


# Urls
class UrlOutput(BaseModel):
    app: str
    view: str
    code: str

class UrlsOutput(BaseModel):
    urls: list[UrlOutput]

# Forms
class FormOutput(BaseModel):
    code: str
    model: str

class FormsOutput(BaseModel):
    forms: list[FormOutput]

#Scaffold
class FileWriteRequest(BaseModel):
    path: str
    filename: str
    content: str