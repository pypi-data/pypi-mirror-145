import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from typing import Any, List


class TwizStateManager:
    user_table: Any
    state_table: Any
    user_id: str

    def __init__(self, user_id: str, user_table_name: str = 'UserTable', state_table_name: str = 'StateTable'):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.user_table = dynamodb.Table(user_table_name)
        self.state_table = dynamodb.Table(state_table_name)
        self.user_id = user_id

    # ----- TABLE READ AND WRITE ----- #
    def read_user_attributes(self):
        try:
            response = self.user_table.get_item(Key={'user_id': self.user_id})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']

    def write_user_attributes(self, map_attributes: dict):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        response = self.user_table.update_item(
            Key={'user_id': self.user_id},
            UpdateExpression="set map_attributes=:attr",
            ExpressionAttributeValues={':attr': map_attributes},
            ReturnValues="UPDATED_NEW"
        )
        return response

    def read_session_state(self,) -> dict:
        try:
            response = self.state_table.get_item(Key={'session_id': self.session_id})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']

    def write_state_attribute(self, attribute_name: str, attribute_val: any):
        """
        Returns the updated items
        """
        # TODO - IDK the return type
        response = self.user_table.update_item(
            Key={'session_id': self.session_id},
            UpdateExpression=f"set {attribute_name}=:attr",
            ExpressionAttributeValues={':attr': attribute_val},
            ReturnValues="UPDATED_NEW"
        )
        return response

    # ----- PROPERTIES ----- #
    @property
    def conversation_id(self) -> str:
        return self.user_attributes.get('conversationId', None)

    @property
    def conversation_states(self) -> List:
        response = self.state_table.query(
            # Add the name of the index you want to use in your query.
            IndexName="user_id-creation_date_time-index",
            KeyConditionExpression=Key('user_id').eq(self.user_id))
        return response['Items']

    @property
    def current_state(self) -> dict:
        return self.conversation_states[-1]  # TODO - check it returns in date-time asc. We want the latest

    @property
    def last_state(self) -> Any:  # -> dict | None
        if len(self.conversation_states) > 1:
            return self.conversation_states[-2]
        else:
            return None

    @property
    def session_id(self) -> str:
        return self.current_state.get('session_id', None)

    @property
    def session_history(self) -> List:
        return self.state_table.query(KeyConditionExpression=Key('session_id').eq(self.session_id))

    @property
    def user_attributes(self) -> dict:
        return self.read_user_attributes().get('map_attributes', None)  # TODO - check this returns json correctly
