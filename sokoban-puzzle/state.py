class State:
    def __init__(self, player, boxes):
        self.player = player
        self.boxes = boxes

    def success(self, goals):
        # check if all boxes are on goals
        return all(map(lambda g: g in self.boxes, goals))

    def __repr__(self):
        return f"player: {self.player}, boxes: {self.boxes}"

    @staticmethod
    def manhattan(box, goal):
        return abs(box[0] - goal[0]) + abs(box[1] - goal[1])

    def distance(self, goals):
        copy_of_boxes = list(self.boxes)
        result = 0
        for goal in goals:
            closest_box = None
            closest_distance = float('inf')

            for box in copy_of_boxes:
                dist_to_goal = self.manhattan(box, goal)
                if dist_to_goal < closest_distance:
                    closest_box = box
                    closest_distance = dist_to_goal

            result += closest_distance
            copy_of_boxes.remove(closest_box)
        return result