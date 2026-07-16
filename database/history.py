"""
history.py

Stores and manages chat history for FactoryBrain AI.
"""

from datetime import datetime


class ChatHistory:

    def __init__(self):

        self.messages = []

    # ======================================
    # Add Message
    # ======================================

    def add_message(
        self,
        role,
        content
    ):

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        self.messages.append(message)

    # ======================================
    # Get History
    # ======================================

    def get_history(self):

        return self.messages

    # ======================================
    # Last N Messages
    # ======================================

    def get_last_messages(
        self,
        n=5
    ):

        return self.messages[-n:]

    # ======================================
    # Clear History
    # ======================================

    def clear(self):

        self.messages = []

    # ======================================
    # Export History
    # ======================================

    def export(self):

        return {
            "total_messages": len(
                self.messages
            ),
            "messages": self.messages
        }

    # ======================================
    # Print History
    # ======================================

    def display(self):

        print("\n===== CHAT HISTORY =====\n")

        for message in self.messages:

            print(
                f"[{message['timestamp']}] "
                f"{message['role'].upper()}: "
                f"{message['content']}"
            )


# ======================================
# Demo
# ======================================

if __name__ == "__main__":

    history = ChatHistory()

    history.add_message(
        "user",
        "Show me maintenance details for Pump A."
    )

    history.add_message(
        "assistant",
        "Pump A requires inspection every 6 months."
    )

    history.add_message(
        "user",
        "Was Valve X replaced?"
    )

    history.add_message(
        "assistant",
        "Yes, Valve X was replaced in Plant 2."
    )

    history.display()

    print("\nLast 2 Messages:")
    print(
        history.get_last_messages(2)
    )
