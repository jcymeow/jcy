from jcy_constants import *

# 下口
PF_BEACON_DOWNSTAIRS = [
    {
        "type": "Entity",
        "name": "jcy_entity_pointer",
        "id": 586091851,
        "components": [
            {
                "type": "TransformDefinitionComponent",
                "name": "prefab_TransformDefinitionComponent",
                "position": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "orientation": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 1.0
                },
                "scale": {
                    "x": 1.0,
                    "y": 25.0,
                    "z": 1.0
                },
                "inheritOnlyPosition": False
            },
            {
                "type": "PrefabPlacementDefinitionComponent",
                "name": "prefab_PrefabPlacementDefinitionComponent",
                "prefab": "data/hd/env/porory/beacon/pf_beacon_downstairs.json"
            }
        ]
    }
]

# 任务
PF_BEACON_QUEST = [
    {
        "type": "Entity",
        "name": "jcy_entity_pointer",
        "id": 586091852,
        "components": [
            {
                "type": "TransformDefinitionComponent",
                "name": "prefab_TransformDefinitionComponent",
                "position": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "orientation": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 1.0
                },
                "scale": {
                    "x": 1.0,
                    "y": 25.0,
                    "z": 1.0
                },
                "inheritOnlyPosition": False
            },
            {
                "type": "PrefabPlacementDefinitionComponent",
                "name": "prefab_PrefabPlacementDefinitionComponent",
                "prefab": "data/hd/env/porory/beacon/pf_beacon_quest.json"
            }
        ]
    }
]

# 上口
PF_BEACON_UPSTAIRS = [
    {
        "type": "Entity",
        "name": "jcy_entity_pointer",
        "id": 586091853,
        "components": [
            {
                "type": "TransformDefinitionComponent",
                "name": "prefab_TransformDefinitionComponent",
                "position": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "orientation": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 1.0
                },
                "scale": {
                    "x": 1.0,
                    "y": 25.0,
                    "z": 1.0
                },
                "inheritOnlyPosition": False
            },
            {
                "type": "PrefabPlacementDefinitionComponent",
                "name": "prefab_PrefabPlacementDefinitionComponent",
                "prefab": "data/hd/env/porory/beacon/pf_beacon_upstairs.json"
            }
        ]
    }
]

# 小站
PF_BEACON_WAYPOINT = [
    {
        "type": "Entity",
        "name": "jcy_entity_pointer",
        "id": 586091854,
        "components": [
            {
                "type": "TransformDefinitionComponent",
                "name": "prefab_TransformDefinitionComponent",
                "position": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "orientation": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 1.0
                },
                "scale": {
                    "x": 1.0,
                    "y": 25.0,
                    "z": 1.0
                },
                "inheritOnlyPosition": False
            },
            {
                "type": "PrefabPlacementDefinitionComponent",
                "name": "prefab_PrefabPlacementDefinitionComponent",
                "prefab": "data/hd/env/porory/beacon/pf_beacon_waypoint.json"
            }
        ]
    }
]

# 道具
PF_BEACON_ITEMS = [
    {
        "type": "Entity",
        "name": "jcy_entity_pointer",
        "id": 586091855,
        "components": [
            {
                "type": "TransformDefinitionComponent",
                "name": "prefab_TransformDefinitionComponent",
                "position": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "orientation": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 1.0
                },
                "scale": {
                    "x": 1.0,
                    "y": 25.0,
                    "z": 1.0
                },
                "inheritOnlyPosition": False
            },
            {
                "type": "PrefabPlacementDefinitionComponent",
                "name": "prefab_PrefabPlacementDefinitionComponent",
                "prefab": "data/hd/env/porory/beacon/pf_beacon_items.json"
            }
        ]
    }
]

# 使者=紫色圆环
PF_BEACON_PURPLE = [
    {
        "type": "Entity",
        "name": "jcy_entity_pointer",
        "id": 586091856,
        "components": [
            {
                "type": "TransformDefinitionComponent",
                "name": "prefab_TransformDefinitionComponent",
                "position": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "orientation": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 1.0
                },
                "scale": {
                    "x": 1.0,
                    "y": 25.0,
                    "z": 1.0
                },
                "inheritOnlyPosition": False
            },
            {
                "type": "PrefabPlacementDefinitionComponent",
                "name": "prefab_PrefabPlacementDefinitionComponent",
                "prefab": "data/hd/env/porory/beacon/pf_beacon_herald.json"
            }
        ]
    }
]

# 出入口指引 长箭头
ROOMTILES_ARROW_LIGHT1 = [
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":230.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":260.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":290.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":320.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-20.0,"y":220.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-40.0,"y":240.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-60.0,"y":260.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-80.0,"y":280.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-30.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-60.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-90.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-120.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-20.0,"y":180.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-40.0,"y":160.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-60.0,"y":140.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-80.0,"y":120.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":1.0,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":170.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":1.0,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":140.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":1.0,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":110.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":1.0,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":80.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":1.0,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":20.0,"y":180.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":40.0,"y":160.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":60.0,"y":140.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":80.0,"y":120.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":30.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":60.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":90.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":120.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":20.0,"y":220.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":40.0,"y":240.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":60.0,"y":260.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":80.0,"y":280.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
]

# 出入口指引 双箭头
ROOMTILES_ARROW_LIGHT2 = [
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":230.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":260.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":290.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":320.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-20.0,"y":220.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-40.0,"y":240.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-60.0,"y":260.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-80.0,"y":280.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-30.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-60.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-90.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-120.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-20.0,"y":180.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-40.0,"y":160.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-60.0,"y":140.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":-80.0,"y":120.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":1.0,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":170.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":1.0,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":140.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":1.0,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":110.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":1.0,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":80.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":1.0,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":20.0,"y":180.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":40.0,"y":160.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":60.0,"y":140.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":80.0,"y":120.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.9239,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":30.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":60.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":90.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":120.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.7071,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},

    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":0.0,"y":200.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":20.0,"y":220.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":40.0,"y":240.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":60.0,"y":260.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999666,"components":[{"type":"TransformDefinitionComponent","name":"transform_entrance_light","position":{"x":80.0,"y":280.0,"z":346.4102},"orientation":{"x":0.0,"y":0.0,"z":0.3827,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_will_entrance_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
]

# 小站指引 长箭头
WAYPOINT_ARROW_LIGHT1 = [
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":-1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":230.0,"z":244.9490},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":-1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":260.0,"z":244.9490},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":-1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":290.0,"z":244.9490},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":-1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":320.0,"z":244.9490},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":-1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":229.9490,"y":220.0,"z":259.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":214.9490,"y":240.0,"z":274.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":199.9490,"y":260.0,"z":289.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":184.9490,"y":280.0,"z":304.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":224.9490,"y":200.0,"z":264.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":204.9490,"y":200.0,"z":284.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":184.9490,"y":200.0,"z":304.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":164.9490,"y":200.0,"z":324.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":229.9490,"y":180.0,"z":259.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":214.9490,"y":160.0,"z":274.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":199.9490,"y":140.0,"z":289.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":184.9490,"y":120.0,"z":304.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.7071,"y":0.0,"z":0.7071,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":170.0,"z":244.9490},"orientation":{"x":0.7071,"y":0.0,"z":0.7071,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":140.0,"z":244.9490},"orientation":{"x":0.7071,"y":0.0,"z":0.7071,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":110.0,"z":244.9490},"orientation":{"x":0.7071,"y":0.0,"z":0.7071,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":80.0,"z":244.9490},"orientation":{"x":0.7071,"y":0.0,"z":0.7071,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":259.9490,"y":180.0,"z":229.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":274.9490,"y":160.0,"z":214.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":289.9490,"y":140.0,"z":199.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":304.9490,"y":120.0,"z":184.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":264.9490,"y":200.0,"z":224.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":284.9490,"y":200.0,"z":204.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":304.9490,"y":200.0,"z":184.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":324.9490,"y":200.0,"z":164.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":259.9490,"y":220.0,"z":229.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":274.9490,"y":240.0,"z":214.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":289.9490,"y":260.0,"z":199.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":304.9490,"y":280.0,"z":184.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_WP.particles","hardKillOnDestroy":False}]},
]

# 小站指引 双箭头
WAYPOINT_ARROW_LIGHT2 = [
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":-1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":230.0,"z":244.9490},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":-1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":260.0,"z":244.9490},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":-1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":290.0,"z":244.9490},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":-1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":320.0,"z":244.9490},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":-1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":229.9490,"y":220.0,"z":259.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":214.9490,"y":240.0,"z":274.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":199.9490,"y":260.0,"z":289.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":184.9490,"y":280.0,"z":304.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":224.9490,"y":200.0,"z":264.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":204.9490,"y":200.0,"z":284.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":184.9490,"y":200.0,"z":304.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":164.9490,"y":200.0,"z":324.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":229.9490,"y":180.0,"z":259.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":214.9490,"y":160.0,"z":274.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":199.9490,"y":140.0,"z":289.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":184.9490,"y":120.0,"z":304.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.7071,"y":0.0,"z":0.7071,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":170.0,"z":244.9490},"orientation":{"x":0.7071,"y":0.0,"z":0.7071,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":140.0,"z":244.9490},"orientation":{"x":0.7071,"y":0.0,"z":0.7071,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":110.0,"z":244.9490},"orientation":{"x":0.7071,"y":0.0,"z":0.7071,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":80.0,"z":244.9490},"orientation":{"x":0.7071,"y":0.0,"z":0.7071,"w":0.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":259.9490,"y":180.0,"z":229.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":274.9490,"y":160.0,"z":214.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":289.9490,"y":140.0,"z":199.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":304.9490,"y":120.0,"z":184.9490},"orientation":{"x":0.6533,"y":0.0,"z":0.6533,"w":-0.3827},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":264.9490,"y":200.0,"z":224.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":284.9490,"y":200.0,"z":204.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":304.9490,"y":200.0,"z":184.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":324.9490,"y":200.0,"z":164.9490},"orientation":{"x":0.5,"y":0.0,"z":0.5,"w":-0.7071},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
                                                                                            
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":244.9490,"y":200.0,"z":244.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":259.9490,"y":220.0,"z":229.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":274.9490,"y":240.0,"z":214.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":289.9490,"y":260.0,"z":199.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":9999999777,"components":[{"type":"TransformDefinitionComponent","name":"transform_portal_light","position":{"x":304.9490,"y":280.0,"z":184.9490},"orientation":{"x":0.2706,"y":0.0,"z":0.2706,"w":-0.9239},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False},{"type":"VfxDefinitionComponent","name":"vfx_portal_light","filename":"data/hd/vfx2/particles/common/fx_horadric_light_Exit.particles","hardKillOnDestroy":False}]},
]

# 掉落光柱
ENTITY_DROP_LIGHT = {
    "type": "Entity",
    "name": "jcy_entity_pointer",
    "id": 9999999888,
    "components": [
        {
            "type": "TransformDefinitionComponent",
            "name": "transform_drop_light",
            "position": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "orientation": {
                "x": 0,
                "y": 0,
                "z": 0,
                "w": 1
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "inheritOnlyPosition": False
        },
        {
            "type": "VfxDefinitionComponent",
            "name": "vfx_drop_light",
            "filename": "data/hd/vfx/particles/overlays/object/horadric_light/fx_horadric_light.particles",
            "hardKillOnDestroy": False
        }
    ]
}

# 掉落特效
ENTITY_DROP_EFFECT = {
    "type": "Entity",
    "name": "jcy_entity_pointer",
    "id": 586091857,
    "components": [
        {
            "type": "TransformDefinitionComponent",
            "name": "transform_drop_effect",
            "position": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "orientation": {
                "x": 0,
                "y": 0,
                "z": 0,
                "w": 1
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "inheritOnlyPosition": False
        },
        {
            "type": "VfxDefinitionComponent",
            "name": "vfx_drop_effect",
            "filename": "data/hd/vfx/particles/overlays/common/valkyriestart/valkriestart_overlay.particles",
            "hardKillOnDestroy": False
        }
    ]
}


# 怪物-光源-微光
ENTITY_MONSTER_LIGHT1 = {
    "type": "Entity",
    "name": "entity_monster_light",
    "id": 7467890901,
    "components": [
        {
            "type": "TransformDefinitionComponent",
            "name": "transform_monster_light",
            "position": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "orientation": {
                "x": 0,
                "y": 0,
                "z": 0,
                "w": 1
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "inheritOnlyPosition": False
        },
        {
            "type": "PointLightDefinitionComponent",
            "name": "vfx_monster_light",
            "color": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "power": 150,
            "radius": 15,
            "attenuation": 1,
            "lightMask": 1,
            "isLocalLight": False,
            "diffuseContribution": 1,
            "specularContribution": 1
        }
    ]
}

# 怪物-光源-柔光
ENTITY_MONSTER_LIGHT2 = {
    "type": "Entity",
    "name": "entity_monster_light",
    "id": 7467890902,
    "components": [
        {
            "type": "TransformDefinitionComponent",
            "name": "entity_torso_TransformDefinition",
            "position": {
                "x": 0.0,
                "y": 3.0,
                "z": 0.0
            },
            "orientation": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "scale": {
                "x": 1.0,
                "y": 1.0,
                "z": 1.0
            },
            "inheritOnlyPosition": False
        },
        {
            "type": "PointLightDefinitionComponent",
            "name": "white_light",
            "color": {
                "x": 1.0,
                "y": 1.0,
                "z": 1.0
            },
            "power": 300.0,
            "radius": 10.0,
            "attenuation": 1.0,
            "lightMask": 1,
            "diffuseContribution": 1.0,
            "specularContribution": 1.0,
            "isLocalLight": False
        }
    ]
}

# 怪物-光源-强光
ENTITY_MONSTER_LIGHT3 = {
    "type": "Entity",
    "name": "entity_monster_light",
    "id": 7467890903,
    "components": [
        {
            "type": "VfxDefinitionComponent",
            "name": "entity_root_VfxDefinition",
            "filename": "data/hd/vfx/particles/missiles/lightning_strike/lightning_lightningstrike.particles",
            "hardKillOnDestroy": True
        },
        {
            "type": "TransformDefinitionComponent",
            "name": "component_transform1",
            "position": {
                "x": 0,
                "y": 3,
                "z": 0
            },
            "orientation": {
                "x": 1.2,
                "y": 0,
                "z": 0,
                "w": 1.0
            },
            "scale": {
                "x": 50,
                "y": 50,
                "z": 50
            },
            "inheritOnlyPosition": False
        }
    ]
}

# 巴尔环
ENTITY_BAAL_SHIELD = [
    {
        "type": "Entity",
        "name": "jcy_entity_pointer",
        "id": 1731987216,
        "components": [
            {
                "type": "VfxDefinitionComponent",
                "name": "vfx_entity_VfxDefinition",
                "filename": "data/hd/vfx/particles/overlays/common/baal_on_throne/baalshield.particles",
                "hardKillOnDestroy": False
            },
            {
                "type": "TransformDefinitionComponent",
                "name": "vfx_entity_TransformDefinition",
                "position": {
                    "x": 0.0,
                    "y": 2.0,
                    "z": 0.0
                },
                "orientation": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 1.0
                },
                "scale": {
                    "x": 1.0,
                    "y": 1.0,
                    "z": 1.0
                },
                "inheritOnlyPosition": False
            }
        ]
    }
]

# 钻石十字架
ENTITY_STAR_CROSS = [
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":32.3,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":31.0,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":30.3,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":29.6,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":28.9,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":28.2,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":27.5,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":26.8,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":26.1,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":25.4,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":24.7,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":24.0,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":23.3,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":22.6,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":21.9,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":21.2,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":20.5,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":19.8,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":19.1,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":18.4,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":17.7,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":17.0,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":16.3,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":15.6,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":14.9,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":14.2,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":13.5,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":12.8,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":12.1,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":11.4,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":10.7,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":10.0,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":9.3,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":8.6,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":7.9,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":7.2,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.0,"y":6.5,"z":0.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":0.5,"y":24.7,"z":-0.5},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":1.0,"y":24.7,"z":-1.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":1.5,"y":24.7,"z":-1.5},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":2.0,"y":24.7,"z":-2.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":2.5,"y":24.7,"z":-2.5},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":3.0,"y":24.7,"z":-3.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":3.5,"y":24.7,"z":-3.5},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":-0.5,"y":24.7,"z":0.5},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":-1.0,"y":24.7,"z":1.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":-1.5,"y":24.7,"z":1.5},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":-2.0,"y":24.7,"z":2.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":-2.5,"y":24.7,"z":2.5},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":-3.0,"y":24.7,"z":3.0},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]},
    {"type":"Entity","name":"jcy_entity_pointer","id":2101618603,"components":[{"type":"VfxDefinitionComponent","name":"entity_iceglint","filename":"data/hd/vfx/particles/missiles/expansion_iceglint/fx_ice_glint.particles","hardKillOnDestroy":True},{"type":"TransformDefinitionComponent","name":"vfx_transform","position":{"x":-3.5,"y":24.7,"z":3.5},"orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},"scale":{"x":1.0,"y":1.0,"z":1.0},"inheritOnlyPosition":False}]}
]

# 使者Nickname
ENTITY_NICKNAME_HERALD = [
    {
        "type": "Entity",
        "name": "jcy_entity_pointer",
        "id": 2238451436,
        "components": [
            {
                "type": "VfxDefinitionComponent",
                "name": "vfx_VfxDefinition",
                "filename": "data/hd/vfx2/particles/common/herald.particles",
                "hardKillOnDestroy": True
            },
            {
                "type": "TransformDefinitionComponent",
                "name": "vfx_TransformDefinition",
                "position": {
                    "x": 0.0,
                    "y": 10.5,
                    "z": 0.0
                },
                "orientation": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 1.0
                },
                "scale": {
                    "x": 1.0,
                    "y": 1.0,
                    "z": 1.0
                },
                "inheritOnlyPosition": False
            }
        ]
    }
]

# 怪物危险标记
ENTITY_MONSTER_DANGEROUS = {
    "type": "Entity",
    "name": "entity_monster_dangerous",
    "id": 7467890051,
    "components": [
        {
            "type": "VfxDefinitionComponent",
            "name": "vxf_monster_dangerous",
            "filename": "data/hd/vfx/particles/objects/vfx_only/arcane_rune_5/vfx_arcanerune_5.particles",
            "hardKillOnDestroy": False
        },
        {
            "type": "TransformDefinitionComponent",
            "name": "vfx4294962040_component_transform",
            "position": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "orientation": {
                "x": 0,
                "y": 0,
                "z": 0,
                "w": 1
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "inheritOnlyPosition": False
        }
    ]
}

# A1兵营指引
ENTITY_COURTE_POINTER = {
    "type": "Entity",
    "name": "entity_court_pointer",
    "id": 7467890060,
    "components": [
        {
            "type": "VfxDefinitionComponent",
            "name": "entity_root_VfxDefinition",
            "filename": "data/hd/vfx2/particles/common/directionarrows_0315.particles",
            "hardKillOnDestroy": False
        },
        {
            "type": "TransformDefinitionComponent",
            "name": "component_transform1",
            "position": {
                "x": 304,
                "y": 20,
                "z": 336.8
            },
            "orientation": {
                "x": 0,
                "y": 0,
                "z": 0.7071,
                "w": 1
            },
            "scale": {
                "x": 1.0,
                "y": 1.0,
                "z": 1.0
            },
            "inheritOnlyPosition": False
        }
    ]
}

# A1兵营指引
ENTITY_COURTN_POINTER = {
    "type": "Entity",
    "name": "entity_court_pointer",
    "id": 7467890061,
    "components": [
        {
            "type": "VfxDefinitionComponent",
            "name": "entity_root_VfxDefinition",
            "filename": "data/hd/vfx2/particles/common/directionarrows_0045.particles",
            "hardKillOnDestroy": False
        },
        {
            "type": "TransformDefinitionComponent",
            "name": "component_transform1",
            "position": {
                "x": 328.9,
                "y": 20,
                "z": 245
            },
            "orientation": {
                "x": 0.7071,
                "y": 0,
                "z": 0,
                "w": 1
            },
            "scale": {
                "x": 1.0,
                "y": 1.0,
                "z": 1.0
            },
            "inheritOnlyPosition": False
        }
    ]
}

# A1兵营指引
ENTITY_COURTW_POINTER = {
    "type": "Entity",
    "name": "entity_court_pointer",
    "id": 7467890062,
    "components": [
        {
            "type": "VfxDefinitionComponent",
            "name": "entity_root_VfxDefinition",
            "filename": "data/hd/vfx2/particles/common/directionarrows_0135.particles",
            "hardKillOnDestroy": False
        },
        {
            "type": "TransformDefinitionComponent",
            "name": "component_transform1",
            "position": {
                "x": 324,
                "y": 20,
                "z": 286
            },
            "orientation": {
                "x": 0,
                "y": 0,
                "z": -0.7071,
                "w": 1
            },
            "scale": {
                "x": 1.0,
                "y": 1.0,
                "z": 1.0
            },
            "inheritOnlyPosition": False
        }
    ]
}

# A5尼拉塞克指引 
ENTITY_NIHLE_POINTER = {
    "type": "Entity",
    "name": "entity_nihl_pointer",
    "id": 7467890070,
    "components": [
        {
            "type": "VfxDefinitionComponent",
            "name": "entity_root_VfxDefinition",
            "filename": "data/hd/vfx2/particles/common/directionarrows_0315.particles",
            "hardKillOnDestroy": False
        },
        {
            "type": "TransformDefinitionComponent",
            "name": "component_transform1",
            "position": {
                "x": 420.0,
                "y": 4,
                "z": 453
            },
            "orientation": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "inheritOnlyPosition": False
        }
    ]
}

# A5尼拉塞克指引 
ENTITY_NIHLN_POINTER = {
    "type": "Entity",
    "name": "entity_nihl_pointer",
    "id": 7467890071,
    "components": [
        {
            "type": "VfxDefinitionComponent",
            "name": "entity_root_VfxDefinition",
            "filename": "data/hd/vfx2/particles/common/directionarrows_0045.particles",
            "hardKillOnDestroy": False
        },
        {
            "type": "TransformDefinitionComponent",
            "name": "component_transform1",
            "position": {
                "x": 420.0,
                "y": 4,
                "z": 453
            },
            "orientation": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "inheritOnlyPosition": False
        }
    ]
}

# A5尼拉塞克指引 
ENTITY_NIHLS_POINTER = {
    "type": "Entity",
    "name": "entity_nihl_pointer",
    "id": 7467890072,
    "components": [
        {
            "type": "VfxDefinitionComponent",
            "name": "entity_root_VfxDefinition",
            "filename": "data/hd/vfx2/particles/common/directionarrows_0225.particles",
            "hardKillOnDestroy": False
        },
        {
            "type": "TransformDefinitionComponent",
            "name": "component_transform1",
            "position": {
                "x": 420.0,
                "y": 4,
                "z": 453
            },
            "orientation": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "inheritOnlyPosition": False
        }
    ]
}

# A5尼拉塞克指引 
ENTITY_NIHLW_POINTER = {
    "type": "Entity",
    "name": "entity_nihl_pointer",
    "id": 7467890073,
    "components": [
        {
            "type": "VfxDefinitionComponent",
            "name": "entity_root_VfxDefinition",
            "filename": "data/hd/vfx2/particles/common/directionarrows_0135.particles",
            "hardKillOnDestroy": False
        },
        {
            "type": "TransformDefinitionComponent",
            "name": "component_transform1",
            "position": {
                "x": 420.0,
                "y": 4,
                "z": 453
            },
            "orientation": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "inheritOnlyPosition": False
        }
    ]
}

# DONTTOUCH
ENTITY_DONT_TOUCH = {
    "type": "ClickCatcherWidget",
    "name": "donttouch",
    "fields": {
        "rect": {
            "x": 0,
            "y": 0,
            "width": 0,
            "height": 0
        }
    }
}

ENTITY_HUD_QUEST = {
    "type": "LevelUpButtonWidget",
    "name": "QuestAlert",
    "fields": {
        "type": "quests",
        "labels": [
            "@CfgQuestLog",
            "@CfgQuestLog"
        ],
        "isFloating": True,
        "rect": {
            "x": 406,
            "y": -164
        },
        "filename": "PANEL/HUD_02/quest_button",
        "leftPanelOffset": {
            "x": 1080
        },
        "newStatsButtonOverlapOffset": {
            "y": -210
        },
        "hoveredFrame": 3,
        "disabledFrame": 2,
        "disabledTint": {
            "a": 1
        }
    },
    "children": [
        {
            "type": "TextBoxWidget",
            "name": "Label",
            "fields": {
                "anchor": {
                    "x": 0.5
                },
                "rect": {
                    "y": -3
                },
                "fontType": "16pt",
                "style": {
                    "pointSize": "$XMediumLargeFontSize",
                    "alignment": {
                        "v": "bottom",
                        "h": "center"
                    },
                    "spacing": "$MinimumSpacing",
                    "dropShadow": "$DefaultDropShadow"
                }
            }
        }
    ]
}


# 技能图标位置
# 0123
# 456789
SKILL_ICON_POSITION = [
    {"x": 	123.00	, "y": 	100.00	, "z": 	129.00	},
    {"x": 	124.50	, "y": 	100.00	, "z": 	127.50	},
    {"x": 	126.00	, "y": 	100.00	, "z": 	126.00	},
    {"x": 	127.50	, "y": 	100.00	, "z": 	124.50	},
    {"x": 	115.90	, "y": 	92.90	, "z": 	124.00	},
    {"x": 	119.90	, "y": 	94.50	, "z": 	124.00	},
    {"x": 	123.90	, "y": 	96.10	, "z": 	124.00	},
    {"x": 	127.90	, "y": 	97.80	, "z": 	124.00	},
    {"x": 	131.90	, "y": 	99.50	, "z": 	124.00	},
    {"x": 	135.90	, "y": 	101.20	, "z": 	124.00	},
]

HIRE_KEYS = {
    1: "rougehire",
    2: "act2hire",
    3: "act3hire",
    51: "act5hire1",
    52: "act5hire2",
}

HIRE_SOUNDS = {
    2: {
        0:{
            "guard_death_hd1": {"FileName": r"monster\guard\monster_guard_death_1_hd.flac"},
            "guard_death_hd2": {"FileName": r"monster\guard\monster_guard_death_2_hd.flac"},
            "guard_death_hd3": {"FileName": r"monster\guard\monster_guard_death_3_hd.flac"},
            "guard_hit_hd1": {"FileName": r"monster\guard\monster_guard_gethit_1_hd.flac"},
            "guard_hit_hd2": {"FileName": r"monster\guard\monster_guard_gethit_2_hd.flac"},
            "guard_hit_hd3": {"FileName": r"monster\guard\monster_guard_gethit_3_hd.flac"},
            "guard_hit_hd4": {"FileName": r"monster\guard\monster_guard_gethit_4_hd.flac"},
        },
        1:{
            "guard_death_hd1": {"FileName": r"monster\rogue\death1_hd.flac"},
            "guard_death_hd2": {"FileName": r"monster\rogue\death2_hd.flac"},
            "guard_death_hd3": {"FileName": r"monster\rogue\death1_hd.flac"},
            "guard_hit_hd1": {"FileName": r"monster\rogue\gethit1_hd.flac"},
            "guard_hit_hd2": {"FileName": r"monster\rogue\gethit2_hd.flac"},
            "guard_hit_hd3": {"FileName": r"monster\rogue\gethit3_hd.flac"},
            "guard_hit_hd4": {"FileName": r"monster\rogue\gethit4_hd.flac"},
        },
    }
}

HIRE_NAMES = {
    2: {
        0: {
            "merca201": {"zhTW": "哈撒迪", "zhCN": "哈扎德"},
            "merca202": {"zhTW": "艾利希爾", "zhCN": "阿西兹尔"},
            "merca203": {"zhTW": "阿撒爾", "zhCN": "艾兹瑞尔"},
            "merca204": {"zhTW": "亞斯哈", "zhCN": "阿萨布"},
            "merca205": {"zhTW": "克哈蘭", "zhCN": "卡兰"},
            "merca206": {"zhTW": "哈辛", "zhCN": "哈辛"},
            "merca207": {"zhTW": "羅森", "zhCN": "拉赞"},
            "merca208": {"zhTW": "艾米羅", "zhCN": "艾米罗"},
            "merca209": {"zhTW": "培撒姆", "zhCN": "普拉桑"},
            "merca210": {"zhTW": "費索", "zhCN": "菲泽尔"},
            "merca211": {"zhTW": "傑馬利", "zhCN": "杰马里"},
            "merca212": {"zhTW": "卡辛姆", "zhCN": "卡辛"},
            "merca213": {"zhTW": "古爾薩", "zhCN": "古札"},
            "merca214": {"zhTW": "米山", "zhCN": "米山"},
            "merca215": {"zhTW": "雷哈拉", "zhCN": "勒哈纳斯"},
            "merca216": {"zhTW": "杜爾加", "zhCN": "杜尔加"},
            "merca217": {"zhTW": "尼爾亞", "zhCN": "妮拉吉"},
            "merca218": {"zhTW": "伊尔赞", "zhCN": "伊尔赞"},
            "merca219": {"zhTW": "撒那利", "zhCN": "扎纳尔西"},
            "merca220": {"zhTW": "瓦黑德", "zhCN": "瓦希德"},
            "merca221": {"zhTW": "維克懷特", "zhCN": "维希亚特"},
        },
        1: {
            "merca201": {"zhTW": "哈莎蒂", "zhCN": "哈莎蒂"},
            "merca202": {"zhTW": "艾莉希爾", "zhCN": "艾莉希尔"},
            "merca203": {"zhTW": "愛斯瑞爾", "zhCN": "爱斯瑞尔"},
            "merca204": {"zhTW": "阿珊碧", "zhCN": "阿珊碧"},
            "merca205": {"zhTW": "嘉蘭", "zhCN": "嘉兰"},
            "merca206": {"zhTW": "哈欣", "zhCN": "哈欣"},
            "merca207": {"zhTW": "蘿珊", "zhCN": "萝珊"},
            "merca208": {"zhTW": "艾米莉", "zhCN": "艾米莉"},
            "merca209": {"zhTW": "普拉姍", "zhCN": "普拉姗"},
            "merca210": {"zhTW": "菲澤麗", "zhCN": "菲泽丽"},
            "merca211": {"zhTW": "吉瑪麗", "zhCN": "吉玛丽"},
            "merca212": {"zhTW": "卡欣", "zhCN": "卡欣"},
            "merca213": {"zhTW": "古爾莎", "zhCN": "古尔莎"},
            "merca214": {"zhTW": "米姍", "zhCN": "米姗"},
            "merca215": {"zhTW": "蕾拉斯", "zhCN": "蕾拉斯"},
            "merca216": {"zhTW": "蒂爾嘉", "zhCN": "蒂尔嘉"},
            "merca217": {"zhTW": "妮拉姬", "zhCN": "妮拉姬"},
            "merca218": {"zhTW": "伊爾姗", "zhCN": "伊尔姗"},
            "merca219": {"zhTW": "莎娜莉", "zhCN": "莎娜莉"},
            "merca220": {"zhTW": "瓦希多", "zhCN": "瓦希多"},
            "merca221": {"zhTW": "薇希婭", "zhCN": "薇希娅"},
        },
    }
}
