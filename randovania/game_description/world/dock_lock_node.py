import dataclasses
from typing import Optional

from randovania.game_description.resources.resource_info import ResourceInfo, ResourceGain
from randovania.game_description.world.node import NodeContext
from randovania.game_description.world.dock_node import DockNode
from randovania.game_description.world.node_identifier import NodeIdentifier
from randovania.game_description.world.resource_node import ResourceNode


@dataclasses.dataclass(frozen=True)
class DockLockNode(ResourceNode):
    dock_identifier: NodeIdentifier

    def resource(self, context: NodeContext) -> ResourceInfo:
        return self.dock_identifier

    def can_collect(self, context: NodeContext) -> bool:
        if context.current_resources.get(self.resource(context), 0) > 0:
            return False

        weakness = context.patches.dock_weakness.get(self.dock_identifier)
        if weakness is None:
            return False

        context.patches.dock_connection

        # TODO

        return True

    def resource_gain_on_collect(self, context: NodeContext) -> ResourceGain:
        raise NotImplementedError

    def _get_dock(self, context: NodeContext) -> DockNode:
        result = context.node_provider.node_by_identifier(self.dock_identifier)
        assert isinstance(result, DockNode)
        return result

    def _get_connecting_dock(self, context: NodeContext) -> Optional[DockNode]:
        identifier = context.patches.dock_connection.get(self.dock_identifier)
        if identifier is None:
            return None

        node = context.node_provider.node_by_identifier(identifier)
        if isinstance(node, DockNode):
            return node
        else:
            return None

    def bleh(self, context: NodeContext):

        node = self._get_dock(context)
        forward_weakness = context.patches.dock_weakness.get(self.dock_identifier,
                                                             node.default_dock_weakness)
        requirement = forward_weakness.requirement

        # TODO: only add requirement if the blast shield has not been destroyed yet

        if isinstance(target_node, DockNode):
            # TODO: Target node is expected to be a dock. Should this error?
            back_weakness = patches.dock_weakness.get(self.identifier_for_node(target_node),
                                                      target_node.default_dock_weakness)
            if back_weakness.lock_type == DockLockType.FRONT_BLAST_BACK_BLAST:
                requirement = RequirementAnd([requirement, back_weakness.requirement])

            elif back_weakness.lock_type == DockLockType.FRONT_BLAST_BACK_IMPOSSIBLE:
                # FIXME: this should check if we've already openend the back
                if back_weakness != forward_weakness:
                    requirement = Requirement.impossible()

        yield target_node, requirement
