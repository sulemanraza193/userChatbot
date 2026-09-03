import json

from groq import Groq

from ..config import GROQ_API_KEY

from ..tools.user_tools import (
    create_user,
    find_user,
    update_user,
    delete_user,
    list_users,
)


if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing from .env")


client = Groq(
    api_key=GROQ_API_KEY
)


MODEL = "openai/gpt-oss-120b"


SYSTEM_PROMPT = """
You are an AI assistant for managing users in a database.

You are being used by an authorized administrator.

Your job is to understand natural language requests
and use the available tools to manage users.

SUPPORTED OPERATIONS:

- Create users
- Find users
- List users
- Update users
- Delete users

IMPORTANT RULES:

1. Never invent user information.

2. When the administrator provides an email,
   use that email exactly.

3. Emails are case-insensitive.

4. If the administrator wants to update a user by name,
   ALWAYS call find_user first.

5. If exactly one user matches the name,
   use that user's email to perform the update.

6. If multiple users match,
   ask the administrator which user they mean.

7. Only update fields explicitly requested.

8. Never change unspecified fields.

9. If a user does not exist,
   clearly explain that.

10. For delete requests, use delete_user.

11. For create requests, use create_user.

12. For find/search requests, use find_user.

13. For requests to list all users, use list_users.

14. Never claim an operation succeeded unless
    the tool actually returned success=True.

15. After using a tool, explain the actual result
    returned by that tool.

16. Keep responses concise and friendly.

EXAMPLES:

"Add john.smith@xyz.com with phone +92332"
→ create_user

"Find john.smith@xyz.com"
→ find_user

"Update john.smith@xyz.com city to Lahore"
→ update_user

"Update Samantha's city to Cordoba"
→ find_user first
→ if exactly one Samantha exists
→ update_user using Samantha's email

"Remove john.smith@xyz.com"
→ delete_user

"Show me all users"
→ list_users
"""


# ---------------------------------------------------------
# TOOL DEFINITIONS
# ---------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_user",
            "description": "Create a new user in the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "User email address"
                    },
                    "name": {
                        "type": "string",
                        "description": "User name"
                    },
                    "phone": {
                        "type": "string",
                        "description": "User phone number"
                    },
                    "city": {
                        "type": "string",
                        "description": "User city"
                    },
                    "country": {
                        "type": "string",
                        "description": "User country"
                    },
                },
                "required": ["email"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "find_user",
            "description": "Find users by email or name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "User email address"
                    },
                    "name": {
                        "type": "string",
                        "description": "User name"
                    },
                },
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "update_user",
            "description": "Update an existing user's information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Email of the user to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "New user name"
                    },
                    "phone": {
                        "type": "string",
                        "description": "New phone number"
                    },
                    "city": {
                        "type": "string",
                        "description": "New city"
                    },
                    "country": {
                        "type": "string",
                        "description": "New country"
                    },
                },
                "required": ["email"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "delete_user",
            "description": "Delete a user by email.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Email of the user to delete"
                    },
                },
                "required": ["email"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "list_users",
            "description": "List all users in the database.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]


# ---------------------------------------------------------
# FUNCTION MAP
# ---------------------------------------------------------

FUNCTION_MAP = {
    "create_user": create_user,
    "find_user": find_user,
    "update_user": update_user,
    "delete_user": delete_user,
    "list_users": list_users,
}


# ---------------------------------------------------------
# CHAT FUNCTION
# ---------------------------------------------------------

def chat_with_gemini(message: str):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": message,
        },
    ]

    try:

        # Allow multiple rounds of tool calling
        for _ in range(5):

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0,
            )

            assistant_message = response.choices[0].message

            # Add assistant message to conversation
            messages.append(assistant_message)

            # No tool call -> final answer
            if not assistant_message.tool_calls:
                return assistant_message.content

            # Execute every requested tool
            for tool_call in assistant_message.tool_calls:

                function_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print(
                    "GROQ TOOL:",
                    function_name,
                    arguments
                )

                function = FUNCTION_MAP.get(function_name)

                if not function:

                    tool_result = {
                        "success": False,
                        "message": f"Unknown tool: {function_name}"
                    }

                else:

                    try:

                        tool_result = function(**arguments)

                    except Exception as error:

                        print("TOOL ERROR:", error)

                        tool_result = {
                            "success": False,
                            "message": str(error)
                        }

                # Send tool result back to the model
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(
                            tool_result,
                            default=str
                        ),
                    }
                )

        return "I was unable to complete the request."

    except Exception as error:

        print("GROQ ERROR:", error)

        raise error

   
        
