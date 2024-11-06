# Wyatt Pereira
# 261113290
Feature: Update an existing todo item
  As a user, I want to update an existing todo item to keep its details current.

  Background:
    Given the API is running

  Scenario Outline: Updating a todo item
    Given an updated todo payload
    And a todo item with ID <todo_id>
    When I send a PUT request to update the todo
    Then <expected_outcome>
    And the system is reset


    Examples:
      | todo_id       | expected_outcome                        |
      | 1             | the todo should be updated successfully |
      | 9999          | I should receive a not found error      |
      | "invalid_id"  | I should receive an invalid ID format error |