# Wyatt Pereira
# 261113290
Feature: Delete a todo item
  As a user, I want to delete a todo item when it is no longer needed.

  Background:
    Given the API is running

  Scenario Outline: Deleting a todo item
    Given a todo item with ID <todo_id>
    When I send a DELETE request for the todo
    Then <expected_outcome>
    And the system is reset

    Examples:
      | todo_id       | expected_outcome                  |
      | 1             | the todo should be deleted successfully |
      | 9999          | I should receive a not found error     |
      | "invalid_id"  | I should receive an invalid ID format error |
