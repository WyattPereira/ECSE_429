Feature: Manage categories for a todo item
  As a user, I want to add or remove categories for a todo item to organize my tasks better.

  Background:
    Given the API is running

  Scenario Outline: Adding a category to a todo item
    Given a category ID <category_id> to add to the todo
    And a todo item with ID <todo_id>
    When I send a POST request to add the category to the todo
    Then <expected_outcome>


        Examples:
      | todo_id | category_id | expected_outcome                  |
      | 1       | 2          | the category should be linked to the todo successfully |
      | 9999    | 2          | I should receive a not found error     |
      | 1      | "invalid_id"| I should receive an invalid ID format error |

  Scenario Outline: Removing a category from a todo item
    Given a category ID <category_id> linked to the todo
    And a todo item with ID <todo_id>
    When I send a DELETE request to remove the category from the todo
    Then <expected_outcome>
    And the system is reset

    Examples:
      | todo_id | category_id | expected_outcome                  |
      | 1       | 2          | the category should be removed from the todo successfully |
      | 9999    | 2          | I should receive a not found error     |
      | 1       | "invalid_id"| I should receive an invalid ID format error |
