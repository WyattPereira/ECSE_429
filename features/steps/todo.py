# Wyatt Pereira
# 261113290
import subprocess
import time

import requests
from behave import given, when, then

BASE_URL = "http://localhost:4567/todos"

# Background
@given("the API is running")
def step_check_server_running(context):
    try:
        response = requests.get("http://localhost:4567/todos")
        assert response.status_code == 200, "Server is not responding as expected."
    except requests.ConnectionError:
        raise AssertionError("Server is not running at http://localhost:4567. Please start the server.")

# Story Test 1: Create a New Todo Item

@given("valid todo payload")
def step_given_valid_todo_payload(context):
    context.payload = {"title": "New Task", "description": "A sample task description"}

@given("incomplete todo payload")
def step_given_incomplete_todo_payload(context):
    context.payload = {"description": "Missing title field"}

@given("invalid todo payload")
def step_given_invalid_todo_payload(context):
    context.payload = "Not a JSON"  # This simulates a malformed payload

@when("I send a POST request to create a new todo")
def step_when_post_create_todo(context):
    context.response = requests.post(BASE_URL, json=context.payload)

@then("the todo should be created successfully")
def step_then_todo_created(context):
    assert context.response.status_code == 201, "Expected 201, got {}".format(context.response.status_code)

@then("I should receive a bad request error")
def step_then_bad_request(context):
    assert context.response.status_code == 400, "Expected 400, got {}".format(context.response.status_code)

# Story Test 2: Retrieve a Specific Todo Item by ID

@given("a todo item with ID {todo_id}")
def step_given_todo_id(context, todo_id):
    context.todo_id = todo_id

@when("I send a GET request for the todo")
def step_when_get_todo_by_id(context):
    context.response = requests.get(f"{BASE_URL}/{context.todo_id}")

@then("the todo details should be returned")
def step_then_todo_retrieved(context):
    assert context.response.status_code == 200, "Expected 200, got {}".format(context.response.status_code)
    data = context.response.json()
    assert "title" in data['todos'][0] and "doneStatus" in data['todos'][0] and "description" in data['todos'][0], "Todo item data missing expected fields"

@then("I should receive a not found error")
def step_then_not_found_error(context):
    assert context.response.status_code == 404, "Expected 404, got {}".format(context.response.status_code)

@then("I should receive an invalid ID format error")
def step_then_invalid_id_error(context):
    assert context.response.status_code == 404, "Expected 404, got {}".format(context.response.status_code)

# Story Test 3: Update an Existing Todo Item

@given("an updated todo payload")
def step_given_updated_todo_payload(context):
    context.payload = {"title": "Updated Task", "description": "Updated description"}

@when("I send a PUT request to update the todo")
def step_when_put_update_todo(context):
    context.response = requests.put(f"{BASE_URL}/{context.todo_id}", json=context.payload)

@then("the todo should be updated successfully")
def step_then_todo_updated(context):
    assert context.response.status_code == 200, "Expected 200, got {}".format(context.response.status_code)
    data = context.response.json()
    assert data["title"] == "Updated Task" and data["description"] == "Updated description", "Todo update failed"

# Story Test 4: Delete a Todo Item

@when("I send a DELETE request for the todo")
def step_when_delete_todo(context):
    context.response = requests.delete(f"{BASE_URL}/{context.todo_id}")

@then("the todo should be deleted successfully")
def step_then_todo_deleted(context):
    assert context.response.status_code == 200, "Expected 200, got {}".format(context.response.status_code)

# Story Test 5: Manage Categories for a Todo Item

@given("a category ID {category_id} to add to the todo")
def step_given_category_id(context, category_id):
    context.category_id = category_id
    context.payload = {"id": context.category_id}

@given("a category ID {category_id} linked to the todo")
def step_given_category_id(context, category_id):
    context.category_id = category_id

@when("I send a POST request to add the category to the todo")
def step_when_post_add_category(context):
    context.response = requests.post(f"{BASE_URL}/{context.todo_id}/categories", json=context.payload)

@then("the category should be linked to the todo successfully")
def step_then_category_added(context):
    assert context.response.status_code == 201, "Expected 201, got {}".format(context.response.status_code)

@when("I send a DELETE request to remove the category from the todo")
def step_when_delete_category(context):
    context.response = requests.delete(f"{BASE_URL}/{context.todo_id}/categories/{context.category_id}")

@then("the category should be removed from the todo successfully")
def step_then_category_removed(context):
    assert context.response.status_code == 200, "Expected 200, got {}".format(context.response.status_code)


# System reset functions
@then("the system is reset")
def reset_system_to_initial_state(context):
    # Restarts the server to reset all initial values

    try:
        response = requests.get("http://localhost:4567/shutdown")
        if response.status_code == 200:
            print("Server shutdown successfully.")
        else:
            print(f"Failed to shutdown server: {response.status_code}")
    except requests.ConnectionError:
        print("Connection error occurred while trying to shut down the server.")

    time.sleep(0.01)

    start_server()

def start_server():
    # Start the server whilst suppressing its startup text
    subprocess.Popen(["java", "-jar", "features/runTodoManagerRestAPI-1.5.5.jar"],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    time.sleep(0.01)  # Give server time to start

    # Verify server is running
    try:
        response = requests.get("http://localhost:4567/todos")
        assert response.status_code == 200
    except requests.ConnectionError:
        raise AssertionError("Server failed to start.")

