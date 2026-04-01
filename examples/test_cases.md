# Test Cases: Add Age Verification for Alcohol

## Missing Information in Ticket
- **UI Design Details**: No specific UI placement, styling, or visual design provided
- **Error Message Text**: Exact error message content not specified
- **Session Persistence Details**: How checkbox state should behave across page refreshes/navigation
- **Analytics Requirements**: Specific events and parameters not defined
- **Platform Scope**: Mobile apps vs web unclear
- **Accessibility Requirements**: No WCAG compliance mentioned
- **Multiple Alcohol Items**: Behavior when cart has multiple alcohol items
- **API Validation**: Whether backend validates age confirmation on order submission

---

## P0 - Critical Test Cases

### UI Level Tests

#### TC-001: Display Age Verification Checkbox with Alcohol Items
**Priority**: P0  
**Test Level**: UI  
**Automation**: Yes - Core functionality validation

**Steps**:
1. Enable feature flag `age_verification_alcohol`
2. Add item with "alcohol" label to cart
3. Navigate to cart/checkout screen

**Expected Result**:
- Checkbox with text "I confirm I am 18 years old" is displayed
- Checkbox is initially unchecked

#### TC-002: Block Order Without Age Confirmation
**Priority**: P0  
**Test Level**: UI  
**Automation**: Yes - Critical business logic

**Steps**:
1. Enable feature flag `age_verification_alcohol`
2. Add alcohol-labeled item to cart
3. Leave age verification checkbox unchecked
4. Attempt to place order

**Expected Result**:
- Order is blocked
- Error message displayed indicating age confirmation required
- User remains on checkout page

#### TC-003: Allow Order With Age Confirmation
**Priority**: P0  
**Test Level**: UI  
**Automation**: Yes - Happy path validation

**Steps**:
1. Enable feature flag `age_verification_alcohol`
2. Add alcohol-labeled item to cart
3. Check age verification checkbox
4. Place order

**Expected Result**:
- Order proceeds successfully
- No age-related error messages

### API Level Tests

#### TC-004: Backend Validates Age Confirmation
**Priority**: P0  
**Test Level**: API  
**Automation**: Yes - Security validation

**Steps**:
1. Submit order API request with alcohol items
2. Omit age confirmation parameter or set to false

**Expected Result**:
- API returns error (400/422)
- Order is not created
- Appropriate error message returned

---

## P1 - High Priority Test Cases

### UI Level Tests

#### TC-005: Hide Checkbox Without Alcohol Items
**Priority**: P1  
**Test Level**: UI  
**Automation**: Yes - Core functionality

**Steps**:
1. Enable feature flag `age_verification_alcohol`
2. Add non-alcohol items to cart
3. View cart/checkout screen

**Expected Result**:
- Age verification checkbox is not displayed

#### TC-006: Feature Flag Disabled Behavior
**Priority**: P1  
**Test Level**: UI  
**Automation**: Yes - Feature flag validation

**Steps**:
1. Disable feature flag `age_verification_alcohol`
2. Add alcohol-labeled items to cart
3. Attempt to place order

**Expected Result**:
- No age verification checkbox shown
- Order placement not blocked by age confirmation
- Normal checkout flow continues

#### TC-007: Mixed Cart Items
**Priority**: P1  
**Test Level**: UI  
**Automation**: Yes - Common scenario

**Steps**:
1. Enable feature flag
2. Add both alcohol and non-alcohol items to cart
3. View cart/checkout

**Expected Result**:
- Age verification checkbox is displayed
- Checkbox behavior same as alcohol-only cart

#### TC-008: Remove All Alcohol Items
**Priority**: P1  
**Test Level**: UI  
**Automation**: No - Complex state management, better for manual testing

**Steps**:
1. Add alcohol items to cart (checkbox appears)
2. Remove all alcohol items from cart
3. Observe UI changes

**Expected Result**:
- Age verification checkbox disappears
- No validation errors on checkout

### Unit Level Tests

#### TC-009: Detect Alcohol Label in Cart
**Priority**: P1  
**Test Level**: Unit  
**Automation**: Yes - Simple logic validation

**Steps**:
1. Mock cart with items containing "alcohol" label
2. Call alcohol detection function

**Expected Result**:
- Function returns true for alcohol presence

#### TC-010: Checkbox State Management
**Priority**: P1  
**Test Level**: Unit  
**Automation**: Yes - State logic validation

**Steps**:
1. Initialize checkbox state
2. Toggle checkbox
3. Verify state persistence

**Expected Result**:
- State changes correctly tracked
- State persists within session

---

## P2 - Medium Priority Test Cases

### UI Level Tests

#### TC-011: Checkbox Visual Accessibility
**Priority**: P2  
**Test Level**: UI  
**Automation**: No - Requires human accessibility testing

**Steps**:
1. Enable feature flag and add alcohol items
2. Test with screen reader
3. Test keyboard navigation
4. Test high contrast mode

**Expected Result**:
- Checkbox properly announced by screen reader
- Focusable via keyboard
- Visible in high contrast mode
- Proper ARIA labels

#### TC-012: Session Persistence Across Navigation
**Priority**: P2  
**Test Level**: UI  
**Automation**: No - Session behavior best tested manually

**Steps**:
1. Add alcohol items, check age verification
2. Navigate away from checkout
3. Return to checkout
4. Refresh page

**Expected Result**:
- Checkbox state maintained during session
- State behavior on refresh defined and consistent

#### TC-013: Multiple Alcohol Items
**Priority**: P2  
**Test Level**: UI  
**Automation**: Yes - Edge case validation

**Steps**:
1. Add multiple different alcohol-labeled items
2. View checkout

**Expected Result**:
- Single age verification checkbox (not one per item)
- Checkbox applies to entire order

### API Level Tests

#### TC-014: Order Payload Contains Age Confirmation
**Priority**: P2  
**Test Level**: API  
**Automation**: Yes - Data validation

**Steps**:
1. Complete checkout with age verification checked
2. Inspect order submission payload

**Expected Result**:
- Age confirmation field present in API request
- Value correctly reflects checkbox state

### Unit Level Tests

#### TC-015: Feature Flag State Handling
**Priority**: P2  
**Test Level**: Unit  
**Automation**: Yes - Configuration testing

**Steps**:
1. Test component behavior with feature flag enabled/disabled
2. Verify no console errors when flag changes

**Expected Result**:
- Clean feature flag integration
- No JavaScript errors

#### TC-016: Edge Case: Empty Cart
**Priority**: P2  
**Test Level**: Unit  
**Automation**: Yes - Edge case validation

**Steps**:
1. Test alcohol detection with empty cart
2. Test with null/undefined cart data

**Expected Result**:
- No errors thrown
- Graceful handling of edge cases

---

## Edge Cases & Error Scenarios

### TC-017: Network Error During Order Submission
**Priority**: P2  
**Test Level**: UI  
**Automation**: No - Network simulation complex

**Steps**:
1. Check age verification
2. Simulate network failure during order submission
3. Retry order

**Expected Result**:
- Appropriate error handling
- Checkbox state preserved
- User can retry without re-checking

### TC-018: Rapid Cart Updates
**Priority**: P2  
**Test Level**: UI  
**Automation**: No - Timing-dependent behavior

**Steps**:
1. Rapidly add/remove alcohol items
2. Observe checkbox appearance/disappearance

**Expected Result**:
- UI updates correctly without flickering
- No race conditions