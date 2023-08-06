""" GraphQL Helper Objects """
from enum import Enum
from typing import NamedTuple

GraphQLVariableName = str
GraphQLVariableDataName = str


class GraphQLVariableType(Enum):
    REQUIRED_STRING = 'String!'
    OPTIONAL_STRING = 'String'
    CREATE_PROJECT_INPUT = 'CreateProjectInput!'
    UPDATE_PROJECT_INPUT = 'UpdateProjectInput!'


class GraphQLQueryVariable(NamedTuple):
    variableName: GraphQLVariableName
    variableDataName: GraphQLVariableDataName
    variableType: GraphQLVariableType
