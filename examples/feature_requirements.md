# Type: User Story
## Summary: Add age verification checkbox for alcohol-labeled items in cart
## Feature Flag: age_verification_alcohol

## Description

As a customer,
I want to confirm that I am at least 18 years old when purchasing alcohol products,
So that I can comply with legal requirements and complete my order.

## Acceptance Criteria

### Scenario 1: Display checkbox when alcohol item is in cart

Given the feature flag age_verification_alcohol is enabled
And the user has at least one item in the cart with the label "alcohol" (provided by backend)
When the user views the cart or checkout screen
Then a checkbox with the text "I confirm I am 18 years old" is displayed

### Scenario 2: Do not display checkbox when no alcohol items

Given the feature flag age_verification_alcohol is enabled
And the cart contains no items labeled "alcohol"
When the user views the cart or checkout
Then the age confirmation checkbox is not displayed

### Scenario 3: Prevent order placement if checkbox is not selected

Given the feature flag age_verification_alcohol is enabled
And the cart contains at least one "alcohol" labeled item
And the checkbox is not selected
When the user attempts to place an order
Then the order is blocked
And the user sees an error message indicating age confirmation is required

### Scenario 4: Allow order placement when checkbox is selected

Given the feature flag age_verification_alcohol is enabled
And the cart contains at least one "alcohol" labeled item
And the checkbox is selected
When the user places the order
Then the order is successfully submitted

### Scenario 5: Feature flag disabled behavior

Given the feature flag age_verification_alcohol is disabled
When the user interacts with the cart or checkout
Then no age verification checkbox is shown
And order placement is not blocked based on age confirmation

## Technical Notes

The "alcohol" label is received from backend and already processed/rendered on the client.

Frontend should detect presence of this label in cart items.

Checkbox state must persist within the session until checkout is completed or cart is updated.

Validation should occur before order submission (client-side + optional backend validation).

## Definition of Done

Feature is controlled via feature flag

All acceptance criteria pass

UI/UX reviewed and approved

Analytics event added (checkbox shown, checked, error triggered)

QA validated across platforms (iOS, Android, Web if applicable)

