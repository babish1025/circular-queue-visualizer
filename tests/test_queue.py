"""
Unit Tests for CircularQueue Engine
Validates all required edge cases, modulo wrap-around, and physical vs logical states.
"""

import unittest
from queue_engine import CircularQueue, QueueOverflowError, QueueUnderflowError


class TestCircularQueue(unittest.TestCase):

    def test_01_empty_queue(self):
        cq = CircularQueue(capacity=5)
        self.assertTrue(cq.is_empty())
        self.assertFalse(cq.is_full())
        self.assertEqual(cq.front, -1)
        self.assertEqual(cq.rear, -1)
        self.assertEqual(cq.size, 0)
        self.assertEqual(cq.display(), [])
        self.assertEqual(cq.get_physical_array(), [None, None, None, None, None])

    def test_02_single_enqueue(self):
        cq = CircularQueue(capacity=5)
        res = cq.enqueue(10)
        self.assertTrue(res["success"])
        self.assertEqual(cq.front, 0)
        self.assertEqual(cq.rear, 0)
        self.assertEqual(cq.size, 1)
        self.assertEqual(cq.display(), [10])
        self.assertEqual(cq.get_physical_array()[0], 10)

    def test_03_multiple_enqueue(self):
        cq = CircularQueue(capacity=5)
        cq.enqueue(10)
        cq.enqueue(20)
        cq.enqueue(30)
        self.assertEqual(cq.front, 0)
        self.assertEqual(cq.rear, 2)
        self.assertEqual(cq.size, 3)
        self.assertEqual(cq.display(), [10, 20, 30])

    def test_04_full_queue(self):
        cq = CircularQueue(capacity=3)
        cq.enqueue("A")
        cq.enqueue("B")
        cq.enqueue("C")
        self.assertTrue(cq.is_full())
        self.assertFalse(cq.is_empty())
        self.assertEqual(cq.size, 3)

    def test_05_overflow(self):
        cq = CircularQueue(capacity=3)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.enqueue(3)
        with self.assertRaises(QueueOverflowError):
            cq.enqueue(4)

    def test_06_dequeue(self):
        cq = CircularQueue(capacity=4)
        cq.enqueue(100)
        cq.enqueue(200)
        res = cq.dequeue()
        self.assertEqual(res["removed_value"], 100)
        self.assertEqual(cq.front, 1)
        self.assertEqual(cq.rear, 1)
        self.assertEqual(cq.size, 1)
        self.assertEqual(cq.display(), [200])

    def test_07_underflow(self):
        cq = CircularQueue(capacity=3)
        with self.assertRaises(QueueUnderflowError):
            cq.dequeue()

    def test_08_peek(self):
        cq = CircularQueue(capacity=3)
        with self.assertRaises(QueueUnderflowError):
            cq.peek()
        cq.enqueue("X")
        cq.enqueue("Y")
        peek_res = cq.peek()
        self.assertEqual(peek_res["front_element"], "X")
        # Ensure peek did not alter queue
        self.assertEqual(cq.size, 2)
        self.assertEqual(cq.front, 0)

    def test_09_clear(self):
        cq = CircularQueue(capacity=4)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.clear()
        self.assertTrue(cq.is_empty())
        self.assertEqual(cq.front, -1)
        self.assertEqual(cq.rear, -1)
        self.assertEqual(cq.size, 0)
        self.assertEqual(cq.get_physical_array(), [None, None, None, None])

    def test_10_reset(self):
        cq = CircularQueue(capacity=4)
        cq.enqueue(1)
        cq.reset(capacity=6)
        self.assertEqual(cq.capacity, 6)
        self.assertTrue(cq.is_empty())
        self.assertEqual(len(cq.get_physical_array()), 6)

    def test_11_wrap_around_and_physical_vs_logical(self):
        """
        The critical test requested in the master prompt:
        Capacity = 5
        Enqueue: 10, 20, 30, 40, 50
        Dequeue: 10, 20
        Enqueue: 60, 70
        Expected:
          Physical: [60, 70, 30, 40, 50]
          Logical:  [30, 40, 50, 60, 70]
          front = 2
          rear = 1
        """
        cq = CircularQueue(capacity=5)
        for v in [10, 20, 30, 40, 50]:
            cq.enqueue(v)
        
        self.assertEqual(cq.get_physical_array(), [10, 20, 30, 40, 50])
        self.assertEqual(cq.display(), [10, 20, 30, 40, 50])
        self.assertEqual(cq.front, 0)
        self.assertEqual(cq.rear, 4)

        # Dequeue 10 and 20
        d1 = cq.dequeue()
        self.assertEqual(d1["removed_value"], 10)
        self.assertEqual(cq.front, 1)

        d2 = cq.dequeue()
        self.assertEqual(d2["removed_value"], 20)
        self.assertEqual(cq.front, 2)
        self.assertEqual(cq.rear, 4)

        # Enqueue 60 (wrap around from rear=4 to rear=(4+1)%5 = 0)
        e60 = cq.enqueue(60)
        self.assertTrue(e60["wrapped"])
        self.assertEqual(cq.rear, 0)

        # Enqueue 70 (rear=(0+1)%5 = 1)
        e70 = cq.enqueue(70)
        self.assertEqual(cq.rear, 1)

        # Verify exact conditions
        self.assertEqual(cq.front, 2)
        self.assertEqual(cq.rear, 1)
        self.assertEqual(cq.size, 5)
        self.assertTrue(cq.is_full())

        # Physical array should be [60, 70, 30, 40, 50]
        self.assertEqual(cq.get_physical_array(), [60, 70, 30, 40, 50])

        # Logical FIFO queue should be [30, 40, 50, 60, 70]
        self.assertEqual(cq.display(), [30, 40, 50, 60, 70])

    def test_12_empty_after_full_dequeues(self):
        cq = CircularQueue(capacity=3)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.dequeue()
        cq.dequeue()
        self.assertTrue(cq.is_empty())
        self.assertEqual(cq.front, -1)
        self.assertEqual(cq.rear, -1)

    def test_13_state_structure(self):
        cq = CircularQueue(capacity=3)
        cq.enqueue(99)
        state = cq.get_state()
        self.assertTrue(state["success"])
        self.assertEqual(state["capacity"], 3)
        self.assertEqual(state["size"], 1)
        self.assertEqual(state["front"], 0)
        self.assertEqual(state["rear"], 0)
        self.assertEqual(len(state["slots"]), 3)
        self.assertTrue(state["slots"][0]["is_front"])
        self.assertTrue(state["slots"][0]["is_rear"])
        self.assertEqual(state["slots"][0]["pointer_tag"], "FRONT & REAR")


if __name__ == "__main__":
    unittest.main()
