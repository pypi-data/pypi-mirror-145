from typing import Optional, List, Any, Dict

from pydantic import BaseModel, Field


class AcceleratorCreate(BaseModel):
    """
    Model for creating Accelerators
    """
    # This is all we need to know. Any additional information can be read from this source.
    source_code: str = Field(alias='sourceCode')

    class Config:
        allow_population_by_field_name = True


class AcceleratorArgument(BaseModel):
    """
    Records the fact that a given Accelerator requires a given argument.

    This is meant to mimic the TransformArgument as closely as possible
    to prevent the Web UI from having to write new code
    """
    name: str
    description: str
    type: str
    extra: Optional[Dict[str, Any]]

    class Config:
        allow_population_by_field_name = True


class AcceleratorDescription(BaseModel):
    """
    Defines how to describe an accelerator
    """
    name: str
    description: Optional[str]
    author: Optional[str]
    arguments: List[AcceleratorArgument]

    class Config:
        allow_population_by_field_name = True


class Accelerator(BaseModel):
    """
    Full front-end representation of an Accelerator
    """
    id: int
    create_author: int = Field(alias="createAuthor")
    description: AcceleratorDescription
    template: str

    class Config:
        allow_population_by_field_name = True


class AcceleratorBulk(BaseModel):
    """
    Model for listing lots of Accelerators; we don't want to send
    things like the full list of arguments with each Acc when listing
    """
    id: int
    create_author: int = Field(alias="createAuthor")
    description: AcceleratorDescription

    class Config:
        allow_population_by_field_name = True


class AcceleratorArgs(BaseModel):
    """
    Represents the arguments that get passed so some given
    Accelerator to create a Dataset
    """
    name: Optional[str]
    args: Dict[str, Any]

    class Config:
        allow_population_by_field_name = True
