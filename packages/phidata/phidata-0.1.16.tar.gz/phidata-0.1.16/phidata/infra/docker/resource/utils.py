from typing import Optional, List, Dict, Tuple

from typing_extensions import Literal

from phidata.infra.docker.resource.base import DockerResource
from phidata.infra.docker.resource.group import DockerResourceGroup
from phidata.infra.docker.resource.types import (
    DockerResourceInstallOrder,
    DockerResourceType,
)
from phidata.utils.log import logger


def get_install_weight_for_docker_resource(
    docker_resource_type: DockerResourceType, resource_group_weight: int = 100
) -> int:
    """Function which takes a DockerResource and resource_group_weight and returns the install
    weight for that resource.

    Understanding install weights for DockerResources:

    - Each DockerResource gets an install weight, which determines the order for installing that particular resource.
    - By default, DockerResources are installed in the order determined by the DockerResourceInstallOrder dict.
        The DockerResourceInstallOrder dict ensures volumes are created before containers
    - We can also provide a weight to the DockerResourceGroup, that weight determines the install order for resources of
        that resource group as compared to other resource groups.
    - We achieve this by multiplying the DockerResourceGroup.weight with the value from DockerResourceInstallOrder
        and by default using a weight of 100. So
        * Weights 1-10 are reserved
        * Choose weight 11-99 to deploy a resource group before all the "default" resources
        * Choose weight 101+ to deploy a resource group after all the "default" resources
        * Choosing weight 100 has no effect because that is the default install weight
    """
    resource_type_class_name = docker_resource_type.__class__.__name__
    if resource_type_class_name in DockerResourceInstallOrder.keys():
        install_weight = DockerResourceInstallOrder[resource_type_class_name]
        final_weight = resource_group_weight * install_weight
        # logger.debug(
        #     "Resource type: {} | RG Weight: {} | Install weight: {} | Final weight: {}".format(
        #         resource_type_class_name,
        #         resource_group_weight,
        #         install_weight,
        #         final_weight,
        #     )
        # )
        return final_weight

    return 5000


def get_docker_resources_from_group(
    docker_resource_group: DockerResourceGroup,
    type_filter: Optional[str] = None,
) -> Optional[List[DockerResourceType]]:
    """Parses the DockerResourceGroup and returns an array of DockerResources
    after applying the type_filter (if any). This function also flattens any
    List[DockerResourceType] attributes. Eg: it will flatten List[DockerContainer]

    Args:
        docker_resource_group:
        type_filter: DockerResourceType to filter by

    Returns:
        List[DockerResourceType]: List of filtered and flattened DockerResources
    """

    # List of resources to return, we use the Union type: DockerResourceType
    # to hold all DockerResources
    docker_resources: List[DockerResourceType] = []
    # logger.debug(f"Flattening {docker_resource_group.name}")

    # Now we populate the docker_resources list with the resources
    # we also flatten any list resources
    # This will loop over each key of the DockerResourceGroup model
    # resource = key
    # resource_data = value in the current DockerResourceGroup object
    for resource, resource_data in docker_resource_group.__dict__.items():
        # logger.debug("resource: {}".format(resource))
        # logger.debug("resource_data: {}".format(resource_data))

        # When we check for isinstance(resource_data, DockerResource)
        # we filter out all keys which are not a subclass of the resource_data
        # thereby leaving out only DockerResource types

        # Check if the resource is a single DockerResourceType or a List[DockerResourceType]
        # If it is a List[DockerResourceType], flatten the resources, verify each element
        # of the list is a subclass of DockerResource and add to the docker_resources list
        if isinstance(resource_data, list):
            for _r in resource_data:
                if isinstance(_r, DockerResource):
                    # If type_filter are provided then skip over DockerResources
                    # that are not in the type_filter
                    if type_filter is not None and isinstance(type_filter, str):
                        # logger.debug(f"type_filter: {type_filter.lower()}")
                        # logger.debug(f"class: {_r.__class__.__name__.lower()}")
                        if type_filter.lower() not in _r.__class__.__name__.lower():
                            logger.debug(
                                "{}:{} filtered out".format(
                                    _r.get_resource_type(), _r.get_resource_name()
                                )
                            )
                            continue
                    docker_resources.append(_r)  # type: ignore

        # If its a single resource, verify that the resource is a subclass of
        # DockerResource and add it to the docker_resources list
        elif isinstance(resource_data, DockerResource):
            # If type_filter are provided then skip if DockerResource
            # is not in the type_filter
            if type_filter is not None and isinstance(type_filter, str):
                if type_filter.lower() not in resource_data.__class__.__name__.lower():
                    logger.debug(
                        "{}:{} filtered out".format(
                            resource_data.get_resource_type(),
                            resource_data.get_resource_name(),
                        )
                    )
                    continue
            docker_resources.append(resource_data)  # type: ignore

    return docker_resources


def dedup_docker_resources(
    docker_resources_with_weight: List[Tuple[DockerResourceType, int]],
) -> List[Tuple[DockerResourceType, int]]:
    if docker_resources_with_weight is None:
        raise ValueError

    deduped_resources: List[Tuple[DockerResourceType, int]] = []
    prev_rsrc: Optional[DockerResourceType] = None
    prev_weight: Optional[int] = None
    for rsrc, weight in docker_resources_with_weight:
        # First item of loop
        if prev_rsrc is None:
            prev_rsrc = rsrc
            prev_weight = weight
            deduped_resources.append((rsrc, weight))
            continue

        # Compare resources with same weight only
        if weight == prev_weight:
            if (
                rsrc.get_resource_type() == prev_rsrc.get_resource_type()
                and rsrc.get_resource_name() == prev_rsrc.get_resource_name()
                and rsrc.get_resource_name() is not None
            ):
                # If resource type and name are the same, skip the resource
                # Note: resource.name cannot be None
                continue

        # If the loop hasn't been continued by the if blocks above,
        # add the resource and weight to the deduped_resources list
        deduped_resources.append((rsrc, weight))
        # update the previous resource for comparison
        prev_rsrc = rsrc
        prev_weight = weight
    return deduped_resources


def filter_and_flatten_docker_resource_groups(
    docker_resource_groups: Dict[str, DockerResourceGroup],
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    sort_order: Literal["create", "delete"] = "create",
) -> Optional[List[DockerResourceType]]:
    """This function parses the docker_resource_groups dict and returns a filtered array of
    DockerResources sorted in the order requested. create == install order, delete == reverse
    Desc:
        1. Iterate through each DockerResourceGroup
        2. If group is enabled, get the DockerResources from that group
        3. Return a list of all DockerResources from 2.

    Args:
        docker_resource_groups: Dict[str, DockerResourceGroup]
            Dict of {resource_group_name : DockerResourceGroup}
        name_filter: Filter DockerResourceGroup by name
        type_filter: Filter DockerResourceGroup by type
        sort_order: create or delete

    Returns:
        List[DockerResourceType]: List of filtered DockerResources
    """

    # The list of DockerResources that will be returned
    filtered_docker_resources: List[DockerResourceType] = []
    logger.debug("Flattening DockerResourceGroups")

    # Step 1: Create docker_resource_list_with_weight
    # A List of Tuples where each tuple is a (DockerResource, Resource Group Weight)
    # This list helps us sort the DockerResources
    # based on their resource group weight using get_install_weight_for_docker_resource
    docker_resource_list_with_weight: List[Tuple[DockerResourceType, int]] = []
    if docker_resource_groups:
        # Iterate through docker_resource_groups
        for docker_rg_name, docker_rg in docker_resource_groups.items():
            # logger.debug("docker_rg_name: {}".format(docker_rg_name))
            # logger.debug("docker_rg: {}".format(docker_rg))

            # If name_filters are provided then filter out DockerResourceGroups
            # that are not in the name_filters
            if name_filter is not None:
                if name_filter not in docker_rg_name:
                    logger.debug(f"name_filter: {name_filter}")
                    logger.debug(f"docker_rg_name: {docker_rg_name}")
                    logger.debug("Group {} filtered out".format(docker_rg_name))
                    continue

            # Only process enabled DockerResourceGroup
            if docker_rg.enabled:
                # If type_filter are provided the only get resources matching type_filter
                # logger.debug("App: {}".format(docker_rg_name))
                docker_resources = get_docker_resources_from_group(
                    docker_rg, type_filter
                )
                if docker_resources:
                    for _docker_rsrc in docker_resources:
                        docker_resource_list_with_weight.append(
                            (_docker_rsrc, docker_rg.weight)
                        )

    # Sort the resources in install order
    if sort_order == "create":
        docker_resource_list_with_weight.sort(
            key=lambda x: get_install_weight_for_docker_resource(x[0], x[1])
        )
    elif sort_order == "delete":
        docker_resource_list_with_weight.sort(
            key=lambda x: get_install_weight_for_docker_resource(x[0], x[1]),
            reverse=True,
        )

    # De-duplicate DockerResources
    # Mainly used to remove the extra Network resources
    deduped_docker_resources: List[
        Tuple[DockerResourceType, int]
    ] = dedup_docker_resources(docker_resource_list_with_weight)
    # deduped_docker_resources = docker_resource_list_with_weight
    # logger.debug("DockerResource list")
    # logger.debug(
    #     "\n".join(
    #         "Name: {}, Type: {}, Weight: {}".format(
    #             rsrc.name, rsrc.resource_type, weight
    #         )
    #         for rsrc, weight in deduped_docker_resources
    #     )
    # )

    # drop the weight from the deduped_docker_resources tuple
    filtered_docker_resources = [x[0] for x in deduped_docker_resources]
    # logger.debug("filtered_docker_resources: {}".format(filtered_docker_resources))
    return filtered_docker_resources
