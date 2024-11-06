Feature: Create a new todo item
  As a user, I want to create a new todo item so I can keep track of tasks.

  Background:
    Given the API is running

  Scenario Outline: Creating a todo item
    Given <payload_type> todo payload
    When I send a POST request to create a new todo
    Then <expected_outcome>
    And the system is reset

    Examples:
      | payload_type      | expected_outcome                  |
      | valid             | the todo should be created successfully |
      | incomplete        | I should receive a bad request error    |
      | invalid           | I should receive a bad request error    |
