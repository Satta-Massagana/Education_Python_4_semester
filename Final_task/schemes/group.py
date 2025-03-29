from pydantic import BaseModel, Field
from typing import Optional, List

class GroupCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="My Group")
    description: Optional[str] = Field(None, max_length=255, example="Group for shared expenses")
    user_ids: Optional[List[int]] = Field(None, description="List of user IDs to add to the group.")

class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="Updated Group Name")
    description: Optional[str] = Field(None, max_length=255, example="Updated group description")
    user_ids: Optional[List[int]] = Field(None, description="List of user IDs to update group membership.")

class GroupList(BaseModel):
    id: int = Field(..., example=1)
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="Updated Group Name")
    description: Optional[str] = Field(None, max_length=255, example="Updated group description")
    user_ids: Optional[List[int]] = Field(None, description="List of user IDs to update group membership.")
