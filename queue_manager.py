"""
Queue Manager Module
Acts as controller coordinating the in-memory CircularQueue, database logging,
and Professor Demo steps.
"""

import uuid
from typing import Dict, Any, List, Optional
from queue_engine import CircularQueue, QueueOverflowError, QueueUnderflowError
from database import db_service


class QueueManager:
    def __init__(self, capacity: int = 5):
        self.session_uuid = str(uuid.uuid4())
        self.queue = CircularQueue(capacity=capacity)
        # Log initial session
        db_service.log_operation(
            session_uuid=self.session_uuid,
            operation="INIT",
            value=None,
            front=-1,
            rear=-1,
            size=0,
            capacity=capacity,
            wrapped=False,
            message=f"Initialized queue with capacity {capacity}"
        )

    def create_queue(self, capacity: int) -> Dict[str, Any]:
        self.session_uuid = str(uuid.uuid4())
        self.queue = CircularQueue(capacity=capacity)
        db_service.log_operation(
            session_uuid=self.session_uuid,
            operation="CREATE",
            value=None,
            front=-1,
            rear=-1,
            size=0,
            capacity=capacity,
            wrapped=False,
            message=f"Created new queue with capacity {capacity}"
        )
        state = self.get_state()
        state["message"] = f"Created Circular Queue with capacity {capacity}"
        return state

    def enqueue(self, value: Any) -> Dict[str, Any]:
        try:
            op_info = self.queue.enqueue(value)
            db_service.log_operation(
                session_uuid=self.session_uuid,
                operation="ENQUEUE",
                value=op_info["value"],
                front=self.queue.front,
                rear=self.queue.rear,
                size=self.queue.size,
                capacity=self.queue.capacity,
                wrapped=op_info.get("wrapped", False),
                message=op_info["message"]
            )
            state = self.get_state()
            state["operation_result"] = op_info
            return state
        except QueueOverflowError as e:
            db_service.log_operation(
                session_uuid=self.session_uuid,
                operation="OVERFLOW",
                value=value,
                front=self.queue.front,
                rear=self.queue.rear,
                size=self.queue.size,
                capacity=self.queue.capacity,
                wrapped=False,
                message=str(e)
            )
            state = self.get_state()
            state["success"] = False
            state["error"] = "OVERFLOW"
            state["message"] = str(e)
            state["operation_result"] = self.queue.last_operation_info
            return state
        except Exception as e:
            state = self.get_state()
            state["success"] = False
            state["error"] = "INVALID"
            state["message"] = str(e)
            return state

    def dequeue(self) -> Dict[str, Any]:
        try:
            op_info = self.queue.dequeue()
            db_service.log_operation(
                session_uuid=self.session_uuid,
                operation="DEQUEUE",
                value=op_info["removed_value"],
                front=self.queue.front,
                rear=self.queue.rear,
                size=self.queue.size,
                capacity=self.queue.capacity,
                wrapped=op_info.get("wrapped", False),
                message=op_info["message"]
            )
            state = self.get_state()
            state["operation_result"] = op_info
            return state
        except QueueUnderflowError as e:
            db_service.log_operation(
                session_uuid=self.session_uuid,
                operation="UNDERFLOW",
                value=None,
                front=self.queue.front,
                rear=self.queue.rear,
                size=self.queue.size,
                capacity=self.queue.capacity,
                wrapped=False,
                message=str(e)
            )
            state = self.get_state()
            state["success"] = False
            state["error"] = "UNDERFLOW"
            state["message"] = str(e)
            state["operation_result"] = self.queue.last_operation_info
            return state

    def peek(self) -> Dict[str, Any]:
        try:
            op_info = self.queue.peek()
            db_service.log_operation(
                session_uuid=self.session_uuid,
                operation="PEEK",
                value=op_info["front_element"],
                front=self.queue.front,
                rear=self.queue.rear,
                size=self.queue.size,
                capacity=self.queue.capacity,
                wrapped=False,
                message=op_info["message"]
            )
            state = self.get_state()
            state["operation_result"] = op_info
            return state
        except QueueUnderflowError as e:
            state = self.get_state()
            state["success"] = False
            state["error"] = "UNDERFLOW"
            state["message"] = str(e)
            state["operation_result"] = self.queue.last_operation_info
            return state

    def display(self) -> Dict[str, Any]:
        logical = self.queue.display()
        state = self.get_state()
        op_info = {
            "success": True,
            "operation": "DISPLAY",
            "logical_order": logical,
            "message": "Displaying logical FIFO queue order." if logical else "Queue is empty.",
            "steps": [
                f"Starting at FRONT index {self.queue.front}",
                f"Advancing using (index + 1) % {self.queue.capacity} for {self.queue.size} elements",
                f"FIFO Output: {' → '.join(map(str, logical)) if logical else 'Empty'}"
            ]
        }
        state["operation_result"] = op_info
        return state

    def clear(self) -> Dict[str, Any]:
        op_info = self.queue.clear()
        db_service.log_operation(
            session_uuid=self.session_uuid,
            operation="CLEAR",
            value=None,
            front=-1,
            rear=-1,
            size=0,
            capacity=self.queue.capacity,
            wrapped=False,
            message="Cleared queue"
        )
        state = self.get_state()
        state["operation_result"] = op_info
        return state

    def reset(self, capacity: Optional[int] = None) -> Dict[str, Any]:
        op_info = self.queue.reset(capacity=capacity)
        self.session_uuid = str(uuid.uuid4())
        db_service.log_operation(
            session_uuid=self.session_uuid,
            operation="RESET",
            value=None,
            front=-1,
            rear=-1,
            size=0,
            capacity=self.queue.capacity,
            wrapped=False,
            message=f"Reset queue with capacity {self.queue.capacity}"
        )
        state = self.get_state()
        state["operation_result"] = op_info
        return state

    def get_state(self) -> Dict[str, Any]:
        base_state = self.queue.get_state()
        base_state["session_uuid"] = self.session_uuid
        base_state["db_status"] = db_service.get_status()
        return base_state

    @staticmethod
    def get_professor_demo_script() -> List[Dict[str, Any]]:
        """
        The academic demo sequence specified in master prompt:
        Capacity 5:
        1. Create capacity 5
        2. Enqueue 10
        3. Enqueue 20
        4. Enqueue 30
        5. Enqueue 40
        6. Enqueue 50
        7. Attempt Enqueue 60 (OVERFLOW!)
        8. Dequeue (removes 10)
        9. Dequeue (removes 20)
        10. Enqueue 60 (REAR WRAPPED 4 -> 0!)
        11. Enqueue 70 (REAR moves to 1)
        Final: Logical 30 -> 40 -> 50 -> 60 -> 70, Physical [60, 70, 30, 40, 50]
        """
        return [
            {"action": "create", "capacity": 5, "description": "1. Initialize Circular Queue with Capacity = 5"},
            {"action": "enqueue", "value": 10, "description": "2. Enqueue 10 (FRONT = 0, REAR = 0)"},
            {"action": "enqueue", "value": 20, "description": "3. Enqueue 20 (REAR advances to 1)"},
            {"action": "enqueue", "value": 30, "description": "4. Enqueue 30 (REAR advances to 2)"},
            {"action": "enqueue", "value": 40, "description": "5. Enqueue 40 (REAR advances to 3)"},
            {"action": "enqueue", "value": 50, "description": "6. Enqueue 50 (Queue is now FULL: Size = 5)"},
            {"action": "enqueue", "value": 60, "description": "7. Attempt Enqueue 60 → OVERFLOW demonstration!"},
            {"action": "dequeue", "description": "8. Dequeue element 10 (FRONT advances to Index 1)"},
            {"action": "dequeue", "description": "9. Dequeue element 20 (FRONT advances to Index 2)"},
            {"action": "enqueue", "value": 60, "description": "10. Enqueue 60 → REAR WRAPS: (4 + 1) % 5 = 0!"},
            {"action": "enqueue", "value": 70, "description": "11. Enqueue 70 → REAR moves to Index 1 (Queue is FULL)"},
            {"action": "display", "description": "12. Final State: Physical=[60, 70, 30, 40, 50], Logical=30→40→50→60→70"}
        ]


# Singleton manager instance
queue_manager = QueueManager(capacity=5)
