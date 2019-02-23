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


class Procedure:
    def __init__(self, name, return_type, function_decl, params=[]):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.function_decl = function_decl


@Operations.register_operation("create_procedure", "invoke_for_target")
@Operations.register_operation("replace_procedure", "replace")
class CreateProcedureOp(ReversibleOp):
    def reverse(self):
        return DropProcedureOp(self.target)


@Operations.register_operation("drop_procedure", "invoke_for_target")
class DropProcedureOp(ReversibleOp):
    def reverse(self):
        return CreateProcedureOp(self.trigger)


@Operations.implementation_for(CreateProcedureOp)
def create_procedure(operations, operation):
    operations.execute(
        f'''
        CREATE FUNCTION {operation.target.name} ({', '.join(operation.target.params)})
        RETURNS {operation.target.return_type} AS $$
        {operation.target.function_decl}
        $$ LANGUAGE plpgsql;
        '''  # noqa
    )


@Operations.implementation_for(DropProcedureOp)
def drop_procedure(operations, operation):
    operations.execute(
        f'''
        DROP FUNCTION IF EXISTS {operation.target.name}
        '''
    )
