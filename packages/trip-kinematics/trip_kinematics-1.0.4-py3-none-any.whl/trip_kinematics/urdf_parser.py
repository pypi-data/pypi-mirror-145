from collections import defaultdict
from typing import Dict, List

import defusedxml.ElementTree as ET
import numpy as np
from trip_kinematics.Utility import Rotation
from trip_kinematics.Transformation import Transformation


def from_urdf(filename: str) -> List[Transformation]:
    """Converts a robot specified in a URDF file into a list of :py:class:`Transformation` objects.

    If the <origin> tag does not specify xyz and rpy values or the tag is omitted, these default
    to (0, 0, 0). <axis> defaults to (0, 0, 1).

    Args:
        filename (str): Path to URDF file.

    Raises:
        ValueError: Could not parse URDF file.

    Returns:
        List[Transformation]: List of transformations that describe the robot.
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    joints = root.findall('joint')
    joint_name_to_transformations = {}

    joint_info = _build_joint_info(joints)

    root_joints = [name for name, value in joint_info.items() if not value['parent']]

    for i, joint in enumerate(joints):
        name = joint.get('name')
        if not name:
            raise ValueError('Missing name field in URDF file')
        joint_info[name]['joint_index'] = i

    for joint in joints:
        joint_name_to_transformations[joint.get('name')] = _get_transformations_for_joint(joint)

    transformations = []
    for joint in root_joints:
        transformations.extend(_create_transformations_from_tree(joint,
                                                                 joint_info,
                                                                 joint_name_to_transformations,
                                                                 None)
                               )

    return transformations


def align_vectors(target: np.ndarray, to_align: np.ndarray) -> np.ndarray:
    """Calculates a rotation matrix that rotates to_align so that it becomes parallel to target.
    Based on work by Íñigo Quílez and Kevin Moran. See:

    "Avoiding Trigonometry", by Íñigo Quílez
    https://iquilezles.org/www/articles/noacos/noacos.htm

    "How to Calculate a Rotation Matrix to Align Vector A to Vector B in 3D", by Kevin Moran
    https://gist.github.com/kevinmoran/b45980723e53edeb8a5a43c49f134724

    Args:
        target (np.ndarray): 3D Vector.
        to_align (np.ndarray): 3D Vector.

    Returns:
        np.ndarray: 3x3 rotation matrix.
    """
    target = target / np.linalg.norm(target)
    to_align = to_align / np.linalg.norm(to_align)

    # If the vectors are parallel but in opposite directions, return a 180 degree rotation
    if np.array_equal(target, -to_align):
        return -np.identity(3)

    align_axis = np.cross(target, to_align)
    cos_angle = np.dot(target, to_align)
    k = 1 / (1 + cos_angle)

    result = np.array([[(align_axis[0] * align_axis[0] * k) + cos_angle,
                        (align_axis[1] * align_axis[0] * k) - align_axis[2],
                        (align_axis[2] * align_axis[0] * k) + align_axis[1]],
                       [(align_axis[0] * align_axis[1] * k) + align_axis[2],
                        (align_axis[1] * align_axis[1] * k) + cos_angle,
                        (align_axis[2] * align_axis[1] * k) - align_axis[0]],
                       [(align_axis[0] * align_axis[2] * k) - align_axis[1],
                        (align_axis[1] * align_axis[2] * k) + align_axis[0],
                        (align_axis[2] * align_axis[2] * k) + cos_angle]])
    return result


def _build_joint_info(joints: List) -> Dict[str, Dict]:
    """Creates a dictionary representing parent-child relationships between joints. Used by
    :py:func:`from_urdf()` to build a tree of joints.

    Args:
        joints (List[ET.Element]): List of <joint> tags from the URDF file.

    Returns:
        dict[str, Dict]: A dictionary representing parent-child relationships between joints.
    """
    # Keep track of parent and children links of joints
    # and use that to search for the parent joint of each joint
    joint_info = {
        joint.get('name'): {
            'child_link': joint.find('child').get('link'),
            'parent_link': joint.find('parent').get('link')
        } for joint in joints}

    parent_link_to_joint = defaultdict(list)
    child_link_to_joint = defaultdict(list)

    for joint in joints:
        parent_link_to_joint[joint.find('parent').get('link')].append(joint.get('name'))
        child_link_to_joint[joint.find('child').get('link')].append(joint.get('name'))

    for val in joint_info.values():
        val['parent'] = child_link_to_joint[val['parent_link']]
        val['child'] = parent_link_to_joint[val['child_link']]

    return joint_info


def _get_transformations_for_joint(joint) -> List[List]:
    """Generates the parameters for the transformations for the input joint. One joint is
    represented by up to five transformations. These are:

        1. origin translation and 2. origin rotation (both taken from the <origin> tag of the URDF),
        3. a rotation that makes joint movement parallel to the z axis of the local coord. system,
        4. the joint movement (the only dynamic transformation of the five),
        5. the inverse transformation of number 3.

    Args:
        joint (ET.Element): A <joint> tag in the URDF file.

    Raises:
        ValueError: Could not parse URDF file.

    Returns:
        List[List]: A list of parameters for up to four py:class:`Transformation` objects that
        describe the input joint.
    """
    # Read properties from urdf
    name = joint.get('name')
    type_ = joint.get('type')
    origin = joint.find('origin')
    joint_transformations = []

    # File needs to specify a joint type for each joint
    try:
        assert type_ is not None
    except AssertionError as err:
        raise ValueError(f'Error: Invalid URDF file ({err})') from err

    if type_ not in ['fixed', 'continuous', 'revolute', 'prismatic', 'floating', 'planar']:
        raise ValueError(f"Unsupported joint type {type_}")

    type_to_mov_dict = {
        'fixed': [{}, []],
        'continuous': [{'rz': 0}, ['rz']],
        'revolute': [{'rz': 0}, ['rz']],
        'prismatic': [{'tz': 0}, ['tz']],
        'floating': [{}, []],  # treating floating and planar as fixed until implemented
        'planar': [{}, []],
    }

    # Default values if origin rotation or translation are not specified
    if origin is None:
        xyz_vals = '0 0 0'
        rpy_vals = '0 0 0'
    else:
        xyz_vals = origin.get('xyz')
        rpy_vals = origin.get('rpy')
        if xyz_vals is None:
            xyz_vals = '0 0 0'
        if rpy_vals is None:
            rpy_vals = '0 0 0'
    origin_xyz = np.array(list(map(float, xyz_vals.split(' '))))
    origin_rpy = np.array(list(map(float, rpy_vals.split(' '))))

    if type_ in ['fixed', 'floating', 'planar']:
        axis = None     # Fixed joints have no axis
        # floating and planar are added to have no axis as they are not yet implemented

    elif type_ in ['continuous', 'revolute', 'prismatic']:
        axis = joint.find('axis')
        # Default to (0, 0, 1) if the axis is unspecified. Note that there does not seem to be
        # a standard default value for the axis. Maybe better to remove the default to prevent
        # potential confusion?
        if axis is None:
            axis = '0 0 1'
        else:
            axis = axis.get('xyz')
        axis = np.array(list(map(float, axis.split(' '))))
        axis /= np.linalg.norm(axis)

    # For each joint, define up to five transformations
    # Transformation 1 (tra): defined by the translation of the origin
    tra = [name + '_tra', {'tx': origin_xyz[0], 'ty': origin_xyz[1], 'tz': origin_xyz[2]}, []]

    # Transformation 2 (rot): defined by the rotation of the origin
    rot_quat = Rotation.from_euler('xyz', [*origin_rpy], degrees=False).as_quat()
    rot = [name + '_rot',
           {'qw': rot_quat[0],
            'qx': rot_quat[1],
            'qy': rot_quat[2],
            'qz': rot_quat[3]},
           [],
           ]

    joint_transformations.extend([tra, rot])

    if axis is not None and not np.array_equal(axis, np.array([0, 0, 1])):
        # Transformation 3 (sta): aligns the joint's axis of movement with the z axis of the
        # coordinate system. Only necessary for movable joints (therefore axis is not None) if
        # the axis is not already parallel to the z axis
        align_transformation = align_vectors(np.array([0, 0, 1]), axis)
        align_quat = Rotation.from_matrix(align_transformation).as_quat()
        sta = [name + '_sta',
               {'qw': align_quat[0],
                'qx': align_quat[1],
                'qy': align_quat[2],
                'qz': align_quat[3]},
               [],
               ]

        # Transformation 5 (unsta): after aligning with the z axis and adding motion of movable
        # joint, reverses the alignment so that we are still in the correct coordinate system.
        # (Note that the movement of the joint is applied between sta and unsta)
        unalign_transformation = np.linalg.inv(align_transformation)
        unalign_quat = Rotation.from_matrix(unalign_transformation).as_quat()
        unsta = [name + '_unsta',
                 {'qw': unalign_quat[0],
                  'qx': unalign_quat[1],
                  'qy': unalign_quat[2],
                  'qz': unalign_quat[3]},
                 [],
                 ]

        joint_transformations.append(sta)
        # unsta will be appended after the joint movement transformation

    # Transformation 4 (mov): represents the movement of the joint. This is the only transformation
    # with state variables.
    mov = [name + '_mov', *type_to_mov_dict[type_]]
    joint_transformations.append(mov)

    if axis is not None and not np.array_equal(axis, np.array([0, 0, 1])):
        joint_transformations.append(unsta)

    return joint_transformations


def _create_transformations_from_tree(joint: str,
                                      joint_info: Dict[str, Dict],
                                      joint_name_to_transformations: Dict[str, List],
                                      parent: Transformation) -> List[Transformation]:
    """Recursively builds a tree of py:class:`Transformation` objects, starting from the root and
    traversing the tree towards the children.

    Args:
        joint (str): Name of the joint.
        joint_info (Dict[str, Dict]): Represents the relationships between all joints.
        joint_name_to_transformations (Dict[str, List]): Contains the parameters for the
                                                         py:class:`Transformation` objects.
        parent (Transformation, optional): The parent of current joint. Should be None for the root,
                                           is set recursively for its children.

    Returns:
        List[Transformation]: List of py:class:`Transformation` objects for input node and all its
                              descendants.
    """
    transformations_list = []

    for transformation in joint_name_to_transformations[joint]:
        # transformation[1] is the parametric description of the transformations
        # If len(transformation) > 2, then the transformation has state variables
        is_nonzero = any(i != 0 for i in transformation[1].values()) or len(transformation[2]) > 0
        if is_nonzero:
            tmp = Transformation(name=transformation[0],
                                 values=transformation[1],
                                 state_variables=transformation[2],
                                 parent=parent)
            transformations_list.append(tmp)
            parent = tmp

    tmp = Transformation(name=joint, values={}, parent=parent)
    transformations_list.append(tmp)
    parent = tmp

    if joint_info[joint]['child']:
        for child in joint_info[joint]['child']:
            transformations_list.extend(
                _create_transformations_from_tree(child,
                                                  joint_info,
                                                  joint_name_to_transformations,
                                                  parent)
            )

    return transformations_list
