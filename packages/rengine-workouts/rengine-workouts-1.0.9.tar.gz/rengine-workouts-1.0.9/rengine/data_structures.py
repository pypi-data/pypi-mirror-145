from random import shuffle
class StrengthExerciseQueueNode:
    """"""
    def __init__(self, exercise_name: str, priority: float) -> None:
        self.next = None
        self.previous = None
        self.exercise_name = exercise_name
        self.priority = priority

    def __str__(self):
        return f"({self.exercise_name}-{self.priority})"


class StrengthExerciseQueue:
    """Queue that generates next strength exercise should do in particular muscle group which goes along with priorities."""

    def __init__(self, exercises: list = None, randomly_order_equal_priorities = True) -> None:
        self.head = None
        self.tail = None
        if(exercises):
            if(randomly_order_equal_priorities):
                shuffle(exercises)
            for exercise in exercises:
                self.add(*exercise)


                

    def add(self, exercise_name: str, priority: float):
        """Similar performance to a priority where smaller numbers have precedence in queue. When exercise is added it moves forward."""
        node = StrengthExerciseQueueNode(exercise_name, priority)
        if(self.head == None):
            self.head = node
            self.tail = node
            return
        n = self.tail
        while(n and n.priority>node.priority):
            n = n.next

        #inserted node becomes head of queue as it has the smallest priority value
        if(n == None):
            self.head.next = node
            prev_head = self.head
            self.head = node
            self.head.previous = prev_head
            return
        
        #Inserted node has largest priority value and becomes tail
        if(n == self.tail):
            node.next = self.tail
            self.tail = node
            n.previous = self.tail
            return

        #Inserted node is in middle of queue somewhere
        next_node = n
        previous_node = n.previous
        next_node.previous = node
        previous_node.next = node
        node.next = next_node
        node.previous = previous_node

    def get(self):
        """Gets next element in queue then sends to tail."""

        if(self.head == self.tail):
            return self.head

        element = self.head
        self.head = element.previous
        self.head.next = None
        element.next = self.tail
        self.tail.previous = element
        element.previous = None
        self.tail = element
        return element

    def __str__(self):
        node_str = "TAIL --"
        n = self.tail
        while(n):
            node_str += " " + str(n)
            n = n.next
        node_str += " -- HEAD"
        

        return node_str


        



        
if __name__ == "__main__":
    queue = StrengthExerciseQueue([
        ("Barbell Deadlift", 1),
        ("Barbell Squat", 1),
        ("Sumo Deadlift", 2)

    ])
    for i in range(6):
        print(f"Day {i+1}: {queue.get().exercise_name}")




 
        



