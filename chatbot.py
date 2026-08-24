"""
chatbot.py
---------
TravelMate AI chatbot logic.

TravelMate is designed ONLY for travel and tourism related questions.

Examples of supported questions:
- Trip planning
- Tourist places
- Destinations
- Itinerary
- Hotels
- Flights
- Trains
- Buses
- Transport
- Travel budget
- Visa and passport
- Packing
- Best time to visit
- Travel safety
- Travel tips

Non-travel questions are politely rejected.
"""

from google import genai
from google.genai import types

import config


class Chatbot:
    """
    TravelMate AI chatbot.

    This class handles:
    1. Gemini connection
    2. Conversation history
    3. Travel-only system instruction
    4. Generating responses
    """

    def __init__(self):

        # Create Gemini client
        self.client = genai.Client(
            api_key=config.GEMINI_API_KEY
        )

        # Store conversation history
        #
        # Example:
        # {
        #     "session-id": [
        #         user message,
        #         assistant message
        #     ]
        # }
        self.histories = {}

    # --------------------------------------------------
    # Get / Create Conversation History
    # --------------------------------------------------

    def get_history(self, session_id):

        if session_id not in self.histories:
            self.histories[session_id] = []

        return self.histories[session_id]

    # --------------------------------------------------
    # Add Message To History
    # --------------------------------------------------

    def add_to_history(self, session_id, role, message):

        history = self.get_history(session_id)

        history.append(
            {
                "role": role,
                "message": message
            }
        )

        # Keep only recent conversation
        max_messages = config.MAX_HISTORY_TURNS * 2

        if len(history) > max_messages:
            self.histories[session_id] = history[
                -max_messages:
            ]

    # --------------------------------------------------
    # Build Conversation Context
    # --------------------------------------------------

    def build_context(self, session_id):

        history = self.get_history(session_id)

        if not history:
            return ""

        context_parts = []

        for item in history:

            role = item["role"]
            message = item["message"]

            if role == "user":
                context_parts.append(
                    f"User: {message}"
                )

            elif role == "assistant":
                context_parts.append(
                    f"TravelMate: {message}"
                )

        return "\n".join(context_parts)

    # --------------------------------------------------
    # Generate Response
    # --------------------------------------------------

    def get_response(self, session_id, user_message):

        user_message = user_message.strip()

        if not user_message:
            return "Please enter a travel-related question."

        # Get previous conversation
        conversation = self.build_context(session_id)

        # TravelMate instructions
        system_instruction = """
You are TravelMate AI, a specialized travel and tourism
assistant.

==================================================
MAIN RULE
==================================================

You ONLY answer questions related to:

- Travel
- Tourism
- Trip planning
- Vacation planning
- Destinations
- Tourist attractions
- Places to visit
- Itineraries
- Hotels and accommodation
- Flights
- Trains
- Buses
- Local transportation
- Car rentals
- Travel routes
- Travel budgets
- Travel expenses
- Visa information
- Passport information
- Travel documents
- Packing lists
- Travel safety
- Travel tips
- Best time to visit
- Weather information specifically for travel planning
- Family trips
- Solo trips
- Couple trips
- Group trips
- Honeymoon trips
- Adventure trips
- Weekend trips
- International travel
- Domestic travel
- Food recommendations specifically for travelers
- Tourist shopping
- Travel activities
- Travel schedules
- Destination comparisons

==================================================
STRICT TRAVEL-ONLY RULE
==================================================

If the user's question is NOT related to travel or tourism,
DO NOT answer the question.

Instead respond:

"I'm TravelMate AI. I can only help with travel and
tourism-related questions. Please ask me about destinations,
trip planning, itineraries, hotels, transportation, budgets,
or other travel topics."

Do NOT provide an answer to the unrelated question.

==================================================
TRAVEL CONTEXT RULE
==================================================

If the user asks a follow-up question that clearly refers
to the previous travel conversation, answer it.

Example:

User:
"Plan a 3 day trip to Ooty."

TravelMate:
Provides a 3 day Ooty plan.

User:
"What about day 2?"

This is a travel-related follow-up, so answer it.

==================================================
TRAVEL PLANNING
==================================================

When creating a trip plan, consider:

1. Destination
2. Number of days
3. Number of travelers
4. Approximate budget
5. Travel preferences
6. Places to visit
7. Transportation
8. Accommodation
9. Food
10. Activities
11. Travel time
12. Safety

If important information is missing, ask the user for it
when necessary.

==================================================
ACCURACY RULE
==================================================

Do NOT invent:

- Hotel prices
- Flight prices
- Train timings
- Bus timings
- Visa rules
- Opening hours
- Availability
- Live weather
- Live traffic
- Real-time booking information

If real-time information is not available, clearly say that
the information may need to be checked with the relevant
official service.

==================================================
RESPONSE STYLE
==================================================

Be:

- Friendly
- Simple
- Helpful
- Clear
- Concise

Use headings and bullet points when useful.

For travel plans, prefer:

Day 1
- Morning
- Afternoon
- Evening

Day 2
- Morning
- Afternoon
- Evening

==================================================
IMPORTANT
==================================================

You are NOT a general-purpose AI assistant.

Your identity is:

TravelMate AI

Your purpose is:

Helping users plan and understand travel and tourism.

Stay within this scope.
"""

        # Add conversation context
        if conversation:

            full_prompt = f"""
Previous conversation:

{conversation}

Current user message:

{user_message}

Continue the conversation as TravelMate AI.
"""

        else:

            full_prompt = user_message

        try:

            # Send request to Gemini
            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,

                contents=full_prompt,

                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.4,
                )
            )

            # Get Gemini response text
            bot_reply = response.text

            if not bot_reply:
                bot_reply = (
                    "Sorry, I couldn't generate a response. "
                    "Please try again."
                )

            # Save user message
            self.add_to_history(
                session_id,
                "user",
                user_message
            )

            # Save TravelMate response
            self.add_to_history(
                session_id,
                "assistant",
                bot_reply
            )

            return bot_reply

        except Exception as e:

            print(
                "Gemini Error:",
                str(e)
            )

            raise