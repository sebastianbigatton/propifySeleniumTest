Feature: Search

  @GoogleSearch
  Scenario: Google search
    Given I open a "chrome" browser
    And I navigate to "https://www.google.com"
    When I fill in "Search" with "nationalhomerentals"
    And I press key "ENTER"
    Then I verify "National Home Rentals" link text is displayed
    And I close the browser

  @DatabaseTest
  Scenario: Populate data to temporary database
    Given A temporary Person database is created
    When Test data from "test_data/person.json" is populated to Person table
    Then Print all records in PERSON table
    And Database connection is closed