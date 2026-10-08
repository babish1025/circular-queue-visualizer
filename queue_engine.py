"""
Circular Queue Engine
Academic Data Structures - Pure Python Implementation
Authors: Babish P K, Bersha S K, Alisha, Jharna (2026)
"""

from typing import Any, Dict, List, Optional, Tuple


class QueueOverflowError(Exception):
    """Raised when enqueuing into a full circular queue."""
    pass


class QueueUnderflowError(Exception):
    """Raised when dequeuing or peeking from an empty circular queue."""
    pass


class CircularQueue:
    """
    A fixed-capacity Circular Queue using modulo arithmetic.
    
    Front points to the first valid element.
    Rear points to the last inserted element.
    Empty state: front = -1, rear = -1, size = 0.
    Modulo formula:
      Next rear = (rear + 1) % capacity
      Next front = (front + 1) % capacity
    """

    def __init__(self, capacity: int = 5):
        if capacity < 2:
            raise ValueError("Capacity must be at least 2")
        if capacity > 12:
            raise ValueError("Capacity cannot exceed 12 for optimal visualization")
        
        self.capacity: int = int(capacity)
        self.queue: List[Optional[Any]] = [None] * self.capacity
        self.front: int = -1
        self.rear: int = -1
        self.size: int = 0
        self.last_operation_info: Dict[str, Any] = {
            "type": "INITIALIZE",
            "message": f"Circular Queue initialized with capacity {self.capacity}",
            "steps": [
                f"Created array of size {self.capacity}",
                "Set FRONT = -1, REAR = -1, SIZE = 0"
            ],
            "wrapped": False
        }

    def is_empty(self) -> bool:
        """Returns True if the queue has no elements."""
        return self.size == 0

    def is_full(self) -> bool:
        """Returns True if the queue has reached maximum capacity."""
        return self.size == self.capacity

    def enqueue(self, value: Any) -> Dict[str, Any]:
        """
        Inserts an element into the circular queue.
        Calculates next rear position using (rear + 1) % capacity.
        """
        # Validate input
        if value is None or str(value).strip() == "":
            raise ValueError("Value cannot be empty")

        # Convert to int or clean string/number
        val_str = str(value).strip()
        try:
            val_clean = int(val_str)
        except ValueError:
            try:
                val_clean = float(val_str)
            except ValueError:
                val_clean = val_str

        # Check overflow
        if self.is_full():
            info = {
                "success": False,
                "error": "OVERFLOW",
                "message": f"Queue Overflow! Cannot enqueue '{val_clean}' because queue is full ({self.size}/{self.capacity}).",
                "steps": [
                    f"Check condition: size ({self.size}) == capacity ({self.capacity}) → TRUE",
                    f"Alternative check: (rear + 1) % capacity == (({self.rear} + 1) % {self.capacity}) == {self.front} == FRONT",
                    "OVERFLOW detected: Insertion rejected to prevent data overwriting."
                ],
                "wrapped": False
            }
            self.last_operation_info = info
            raise QueueOverflowError(info["message"])

        steps = []
        steps.append(f"STEP 1: Verified queue is not full ({self.size}/{self.capacity}).")

        prev_rear = self.rear
        wrapped = False

        if self.is_empty():
            self.front = 0
            self.rear = 0
            steps.append(f"STEP 2: Queue was empty. Set FRONT = 0, REAR = 0.")
        else:
            calc_next = (prev_rear + 1) % self.capacity
            steps.append(f"STEP 2: Current REAR = {prev_rear}.")
            steps.append(f"STEP 3: Calculate next REAR = ({prev_rear} + 1) % {self.capacity} = {calc_next}.")
            if calc_next < prev_rear:
                wrapped = True
                steps.append(f"STEP 4: Circular wrap-around occurred! REAR wrapped from {prev_rear} to {calc_next}.")
            else:
                steps.append(f"STEP 4: REAR updated from {prev_rear} to {calc_next}.")
            self.rear = calc_next

        self.queue[self.rear] = val_clean
        self.size += 1
        steps.append(f"STEP 5: Inserted value '{val_clean}' at physical array index {self.rear}.")
        steps.append(f"STEP 6: Updated queue size to {self.size}.")

        wrap_detail = None
        if wrapped:
            wrap_detail = {
                "from_index": prev_rear,
                "to_index": self.rear,
                "formula": f"({prev_rear} + 1) % {self.capacity} = {self.rear}",
                "message": f"REAR WRAPPED: {prev_rear} → {self.rear}"
            }

        op_info = {
            "success": True,
            "operation": "ENQUEUE",
            "value": val_clean,
            "inserted_at": self.rear,
            "front": self.front,
            "rear": self.rear,
            "size": self.size,
            "capacity": self.capacity,
            "wrapped": wrapped,
            "wrap_detail": wrap_detail,
            "steps": steps,
            "message": f"Successfully enqueued '{val_clean}' at index {self.rear}."
        }
        self.last_operation_info = op_info
        return op_info

    def dequeue(self) -> Dict[str, Any]:
        """
        Removes and returns the front element from the circular queue.
        Advances front using (front + 1) % capacity.
        """
        if self.is_empty():
            info = {
                "success": False,
                "error": "UNDERFLOW",
                "message": "Queue Underflow! Cannot dequeue from an empty queue.",
                "steps": [
                    f"Check condition: size ({self.size}) == 0 or front == -1 → TRUE",
                    "UNDERFLOW detected: No elements available to remove."
                ],
                "wrapped": False
            }
            self.last_operation_info = info
            raise QueueUnderflowError(info["message"])

        steps = []
        steps.append(f"STEP 1: Verified queue is not empty (Size: {self.size}).")

        removed_val = self.queue[self.front]
        removed_idx = self.front
        self.queue[removed_idx] = None
        self.size -= 1
        steps.append(f"STEP 2: Retrieved element '{removed_val}' from index {removed_idx} (FRONT).")

        prev_front = self.front
        wrapped = False

        if self.size == 0:
            self.front = -1
            self.rear = -1
            steps.append("STEP 3: Queue is now empty. Reset FRONT = -1, REAR = -1.")
        else:
            next_front = (prev_front + 1) % self.capacity
            steps.append(f"STEP 3: Calculate next FRONT = ({prev_front} + 1) % {self.capacity} = {next_front}.")
            if next_front < prev_front:
                wrapped = True
                steps.append(f"STEP 4: Circular wrap-around occurred! FRONT wrapped from {prev_front} to {next_front}.")
            else:
                steps.append(f"STEP 4: FRONT updated from {prev_front} to {next_front}.")
            self.front = next_front

        wrap_detail = None
        if wrapped:
            wrap_detail = {
                "from_index": prev_front,
                "to_index": self.front,
                "formula": f"({prev_front} + 1) % {self.capacity} = {self.front}",
                "message": f"FRONT WRAPPED: {prev_front} → {self.front}"
            }

        op_info = {
            "success": True,
            "operation": "DEQUEUE",
            "removed_value": removed_val,
            "removed_from": removed_idx,
            "front": self.front,
            "rear": self.rear,
            "size": self.size,
            "capacity": self.capacity,
            "wrapped": wrapped,
            "wrap_detail": wrap_detail,
            "steps": steps,
            "message": f"Successfully dequeued '{removed_val}' from index {removed_idx}."
        }
        self.last_operation_info = op_info
        return op_info

    def peek(self) -> Dict[str, Any]:
        """
        Returns the front element without removing it.
        """
        if self.is_empty():
            info = {
                "success": False,
                "error": "UNDERFLOW",
                "message": "Queue is empty! No element to peek.",
                "steps": [
                    "Check condition: size == 0 → TRUE",
                    "PEEK requires at least 1 element."
                ],
                "wrapped": False
            }
            self.last_operation_info = info
            raise QueueUnderflowError(info["message"])

        val = self.queue[self.front]
        steps = [
            f"STEP 1: Inspected FRONT index ({self.front}).",
            f"STEP 2: Found element '{val}'.",
            "STEP 3: Queue state unchanged (Non-destructive inspection)."
        ]

        op_info = {
            "success": True,
            "operation": "PEEK",
            "front_element": val,
            "front_index": self.front,
            "size": self.size,
            "capacity": self.capacity,
            "steps": steps,
            "message": f"Front element is '{val}' at index {self.front}."
        }
        self.last_operation_info = op_info
        return op_info

    def display(self) -> List[Any]:
        """
        Returns the logical FIFO sequence of elements currently in the queue,
        starting at front and ending at rear.
        """
        if self.is_empty():
            return []

        logical = []
        curr = self.front
        for _ in range(self.size):
            logical.append(self.queue[curr])
            curr = (curr + 1) % self.capacity
        return logical

    def clear(self) -> Dict[str, Any]:
        """
        Resets all slots in the current queue while maintaining capacity.
        """
        self.queue = [None] * self.capacity
        self.front = -1
        self.rear = -1
        self.size = 0

        op_info = {
            "success": True,
            "operation": "CLEAR",
            "message": "All queue slots cleared. FRONT and REAR reset to -1.",
            "steps": [
                "Set all array slots to None/Empty",
                "Reset FRONT = -1, REAR = -1, SIZE = 0"
            ],
            "wrapped": False
        }
        self.last_operation_info = op_info
        return op_info

    def reset(self, capacity: Optional[int] = None) -> Dict[str, Any]:
        """
        Resets the queue, optionally with a new capacity.
        """
        new_cap = int(capacity) if capacity is not None else self.capacity
        if new_cap < 2 or new_cap > 12:
            raise ValueError("Capacity must be between 2 and 12.")
        
        self.capacity = new_cap
        self.queue = [None] * self.capacity
        self.front = -1
        self.rear = -1
        self.size = 0

        op_info = {
            "success": True,
            "operation": "RESET",
            "capacity": self.capacity,
            "message": f"Queue reset with capacity {self.capacity}.",
            "steps": [
                f"Reallocated array with capacity {self.capacity}",
                "Set FRONT = -1, REAR = -1, SIZE = 0"
            ],
            "wrapped": False
        }
        self.last_operation_info = op_info
        return op_info

    def get_physical_array(self) -> List[Optional[Any]]:
        """Returns the actual underlying array contents."""
        return list(self.queue)

    def get_state(self) -> Dict[str, Any]:
        """
        Generates full snapshot of physical array, logical FIFO queue,
        slot metadata, and pointers for frontend visualization.
        """
        slots = []
        for idx in range(self.capacity):
            val = self.queue[idx]
            is_occ = val is not None
            is_f = (idx == self.front) and (self.front != -1)
            is_r = (idx == self.rear) and (self.rear != -1)

            pointer_tag = ""
            if is_f and is_r:
                pointer_tag = "FRONT & REAR"
            elif is_f:
                pointer_tag = "FRONT"
            elif is_r:
                pointer_tag = "REAR"

            slots.append({
                "index": idx,
                "value": val,
                "is_occupied": is_occ,
                "is_front": is_f,
                "is_rear": is_r,
                "pointer_tag": pointer_tag
            })

        logical = self.display()

        return {
            "success": True,
            "capacity": self.capacity,
            "size": self.size,
            "front": self.front,
            "rear": self.rear,
            "is_empty": self.is_empty(),
            "is_full": self.is_full(),
            "physical_array": self.get_physical_array(),
            "logical_queue": logical,
            "slots": slots,
            "last_operation": self.last_operation_info
        }
