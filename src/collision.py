import pygame as pg

from physics import Position


def resolve_collisions(physics_objects: ["PhysicsObject"]):
    for i in range(0, len(physics_objects)):
        for j in range(i + 1, len(physics_objects)):
            object1 = physics_objects[i]
            object2 = physics_objects[j]
            if object1.solid and object2.solid:
                overlap = pg.sprite.collide_mask(object1.element, object2.element);

                if overlap:
                    print("col", overlap)
                    # resolve x collision

                    # resolve y collision
                    
                else:
                    print("ncol")
                pass
            