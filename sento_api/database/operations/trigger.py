# Copyright (C) 2019 Roberto García Calero (garcalrob@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Based on https://alembic.sqlalchemy.org/en/latest/cookbook.html#create-operations-for-the-target-objects # noqa

from alembic.operations import Operations
from sento_api.database.operations.reversible import ReversibleOp


class Trigger:
    def __init__(self, name, when, event, table_name, function_type,
                 function_name, function_args, additional_opts=''):
        self.name = name
        self.when = when
        self.event = event
        self.table_name = table_name
        self.additional_opts = additional_opts
        self.function_type = function_type
        self.function_name = function_name
        self.function_args = function_args


@Operations.register_operation("create_trigger", "invoke_for_target")
@Operations.register_operation("replace_trigger", "replace")
class CreateTriggerOp(ReversibleOp):
    def reverse(self):
        return DropTriggerOp(self.target)


@Operations.register_operation("drop_trigger", "invoke_for_target")
class DropTriggerOp(ReversibleOp):
    def reverse(self):
        return CreateTriggerOp(self.trigger)


@Operations.implementation_for(CreateTriggerOp)
def create_view(operations, operation):
    operations.execute(
        f'''
        CREATE TRIGGER {operation.target.name}
        {operation.target.when} {operation.target.event}
        ON {operation.target.table_name}
        {operation.target.additional_opts}
        EXECUTE {operation.target.function_type}
        {operation.target.function_name} ({', '.join(operation.target.function_args)})
        '''  # noqa
    )


@Operations.implementation_for(DropTriggerOp)
def drop_view(operations, operation):
    operations.execute(
        f'''
        DROP TRIGGER IF EXISTS {operation.target.name}
        ON {operation.target.table_name}
        '''
    )
