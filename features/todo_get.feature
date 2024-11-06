# Wyatt Pereira
# 261113290
Feature: Retrieve a specific todo item
  As a user, I want to retrieve a specific todo item using its ID to view its details.

  Background:
    Given the API is running

  Scenario Outline: Retrieving a todo item by ID
    Given a todo item with ID <todo_id>
    When I send a GET request for the todo
    Then <expected_outcome>
    And the system is reset

    Examples:
      | todo_id       | expected_outcome                     |
      | 1             | the todo details should be returned  |
      | 9999          | I should receive a not found error   |
      | "invalid_id"  | I should receive an invalid ID format error |
