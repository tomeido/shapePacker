import numpy as np

class ShapePacker():
    def __init__(self, field_depth, field_width, voids):
        self.field_depth = field_depth
        self.field_width = field_width
        self.field = np.zeros((field_depth, field_width), dtype=int)
        self.add_twos(voids)

    def add_twos(self, voids):
        indices = np.random.choice(range(self.field_depth * self.field_width), voids, replace=False)
        for index in indices:
            row = index // self.field_width
            col = index % self.field_width
            self.field[row, col] = 2

    
    def rotate_shape(self, shape):
        return np.rot90(shape)

    def mirror_shape(self, shape):
        return np.fliplr(shape)

    def alt_shapes(self, shapes):
        rotated_shapes = []
        for shape in shapes:
            rotated_shapes.append(shape)
            shape = self.rotate_shape(shape)
            rotated_shapes.append(shape)
            shape = self.rotate_shape(shape)
            rotated_shapes.append(shape)
            shape = self.rotate_shape(shape)
            rotated_shapes.append(shape)
            shape = self.rotate_shape(shape)
            shape = self.mirror_shape(shape)
            rotated_shapes.append(shape)
            shape = self.rotate_shape(shape)
            rotated_shapes.append(shape)
            shape = self.rotate_shape(shape)
            rotated_shapes.append(shape)
            shape = self.rotate_shape(shape)
            rotated_shapes.append(shape)
        return rotated_shapes

    def pack_shapes(self, shapes):
        packed_shapes = []
        for i in range(self.field_depth):
            for j in range(self.field_width):
                if self.field[i,j] == 0:
                    for shape in shapes:
                        try:
                            if self.can_place_shape(shape, (i, j)):
                                packed_shapes.append((shape, (i, j)))
                                self.place_shape(shape, (i, j))
                                self.space_field(shape, (i, j), spacing)
                        except:                      
                            continue
        return packed_shapes

    def can_place_shape(self, shape, pos):
        for i in range(shape.shape[0]):
            for j in range(shape.shape[1]):
                if shape[i, j] != 0 and self.field[pos[0] + i, pos[1] + j] != 0:
                    return False
        return True

    def place_shape(self, shape, pos):
        for i in range(shape.shape[0]):
            for j in range(shape.shape[1]):
                if shape[i, j] != 0:
                    # Place the shape element
                    self.field[pos[0] + i, pos[1] + j] = shape[i, j]

    def space_field(self, shape, pos, distance):
        for i in range(shape.shape[0]):
            for j in range(shape.shape[1]):
                # Check for adjacent zeros and update to 3
                if shape[i, j] == 1:
                    # Check surrounding cells (up, down, left, right)
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        for step in range(1, distance + 1):
                            new_row = pos[0] + i + step * di
                            new_col = pos[1] + j + step * dj
                            # Check if within field bounds and is a zero
                            if 0 <= new_row < self.field_depth and 0 <= new_col < self.field_width and self.field[new_row, new_col] == 0:
                                self.field[new_row, new_col] = 9
                            else:
                                continue

if __name__ == "__main__":
    field_depth = 10
    field_width = 10
    voids = 10
    spacing = 5
    # Define the example shape properly
    shapes = [np.array([(1, 1, 1), (0, 0, 1)])]  # Example shape

    packer = ShapePacker(field_depth, field_width, voids)
    alt_shapes = packer.alt_shapes(shapes)
    packed_shapes = packer.pack_shapes(alt_shapes)

    print(packed_shapes)
    print(packer.field)

