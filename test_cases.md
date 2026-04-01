# Test Cases: Age Verification for Alcohol Products

## Missing Information/Requirements
- **Error message text**: What specific error message should be shown when age verification is not completed?
- **Checkbox placement**: Where exactly should the checkbox appear on cart/checkout screens?
- **Cross-platform specifics**: Different behavior needed for iOS/Android/Web?
- **Analytics events**: Specific event names and parameters for tracking
- **Session persistence**: How should checkbox state behave when cart is updated?
- **Backend validation**: Is server-side validation required in addition to client-side?

---

## Unit Tests (P0)

### TC-001: Feature Flag Detection
**Title**: Verify feature flag controls age verification display  
**Steps**:
1. Set feature flag `age_verification_alcohol` to true
2. Initialize component with cart containing alcohol-labeled items
3. Verify checkbox rendering logic returns true
4. Set feature flag to false
5. Verify checkbox rendering logic returns false

**Expected Result**: Component correctly responds to feature flag state  
**Priority**: P0  
**Test Level**: unit  
**Automation**: yes - critical feature toggle logic

### TC-002: Alcohol Item Detection Logic
**Title**: Verify detection of alcohol-labeled items in cart  
**Steps**:
1. Create cart with items having various labels including "alcohol"
2. Call alcohol detection function
3. Verify function returns true
4. Create cart with no alcohol-labeled items
5. Verify function returns false

**Expected Result**: Function correctly identifies presence of alcohol items  
**Priority**: P0  
**Test Level**: unit  
**Automation**: yes - core business logic

### TC-003: Checkbox Validation Logic
**Title**: Verify age verification validation  
**Steps**:
1. Set checkbox state to unchecked with alcohol items present
2. Call validation function
3. Verify validation returns false
4. Set checkbox state to checked
5. Verify validation returns true

**Expected Result**: Validation correctly checks checkbox state  
**Priority**: P0  
**Test Level**: unit  
**Automation**: yes - critical validation logic

---

## API Tests (P1)

### TC-004: Order Submission with Age Verification
**Title**: Verify order API handles age verification flag  
**Steps**:
1. Prepare order payload with alcohol items and ageVerified: true
2. Submit order via API
3. Verify order is accepted
4. Submit same order with ageVerified: false
5. Verify order is rejected with appropriate error

**Expected Result**: API correctly validates age verification status  
**Priority**: P1  
**Test Level**: api  
**Automation**: yes - API validation is deterministic

### TC-005: Cart Data Structure Validation
**Title**: Verify cart API returns alcohol labels correctly  
**Steps**:
1. Add alcohol-labeled items to cart via API
2. Retrieve cart data
3. Verify alcohol label is present in item metadata
4. Add non-alcohol items
5. Verify labels are correctly differentiated

**Expected Result**: Cart API correctly provides alcohol labeling data  
**Priority**: P1  
**Test Level**: api  
**Automation**: yes - data structure validation

---

## UI Tests (P0-P2)

### TC-006: Checkbox Display with Alcohol Items
**Title**: Age verification checkbox appears when cart contains alcohol  
**Steps**:
1. Enable feature flag `age_verification_alcohol`
2. Add alcohol-labeled item to cart
3. Navigate to cart/checkout screen
4. Verify checkbox with text "I confirm I am 18 years old" is displayed
5. Verify checkbox is initially unchecked

**Expected Result**: Checkbox is visible and properly labeled  
**Priority**: P0  
**Test Level**: ui  
**Automation**: yes - straightforward element verification

### TC-007: No Checkbox Without Alcohol Items
**Title**: Age verification checkbox hidden when no alcohol in cart  
**Steps**:
1. Enable feature flag `age_verification_alcohol`
2. Add only non-alcohol items to cart
3. Navigate to cart/checkout screen
4. Verify age verification checkbox is not displayed

**Expected Result**: No age verification checkbox visible  
**Priority**: P0  
**Test Level**: ui  
**Automation**: yes - element absence verification

### TC-008: Order Blocked Without Age Verification
**Title**: Order submission prevented when checkbox unchecked  
**Steps**:
1. Enable feature flag and add alcohol items to cart
2. Navigate to checkout with checkbox unchecked
3. Attempt to place order
4. Verify order submission is blocked
5. Verify error message is displayed

**Expected Result**: Order blocked with error message shown  
**Priority**: P0  
**Test Level**: ui  
**Automation**: partially - error message text needs manual verification

### TC-009: Successful Order with Age Verification
**Title**: Order completes when age verification checkbox is checked  
**Steps**:
1. Enable feature flag and add alcohol items to cart
2. Navigate to checkout
3. Check age verification checkbox
4. Complete order placement
5. Verify order is successfully submitted

**Expected Result**: Order processes normally  
**Priority**: P0  
**Test Level**: ui  
**Automation**: yes - happy path scenario

### TC-010: Feature Flag Disabled Behavior
**Title**: No age verification when feature flag disabled  
**Steps**:
1. Disable feature flag `age_verification_alcohol`
2. Add alcohol-labeled items to cart
3. Navigate through cart and checkout
4. Complete order placement
5. Verify no age verification checkbox appears
6. Verify order completes without age verification

**Expected Result**: Normal checkout flow without age verification  
**Priority**: P0  
**Test Level**: ui  
**Automation**: yes - feature flag testing

### TC-011: Checkbox State Persistence
**Title**: Checkbox state persists during session  
**Steps**:
1. Add alcohol items and check age verification checkbox
2. Navigate away from checkout
3. Return to checkout
4. Verify checkbox remains checked
5. Update cart contents
6. Verify checkbox state behavior

**Expected Result**: Checkbox state persists appropriately  
**Priority**: P1  
**Test Level**: ui  
**Automation**: no - requires session state validation across navigation

### TC-012: Mixed Cart Behavior
**Title**: Checkbox appears with mixed alcohol/non-alcohol items  
**Steps**:
1. Add both alcohol and non-alcohol items to cart
2. Navigate to checkout
3. Verify age verification checkbox is displayed
4. Remove all alcohol items
5. Verify checkbox disappears

**Expected Result**: Checkbox visibility responds to cart changes  
**Priority**: P1  
**Test Level**: ui  
**Automation**: yes - dynamic UI behavior

### TC-013: Multiple Alcohol Items
**Title**: Single checkbox for multiple alcohol items  
**Steps**:
1. Add multiple different alcohol-labeled items to cart
2. Navigate to checkout
3. Verify only one age verification checkbox appears
4. Complete checkout with checkbox checked

**Expected Result**: Single checkbox handles multiple alcohol items  
**Priority**: P1  
**Test Level**: ui  
**Automation**: yes - UI element counting

### TC-014: Accessibility Compliance
**Title**: Age verification checkbox meets accessibility standards  
**Steps**:
1. Display age verification checkbox
2. Verify checkbox has proper ARIA labels
3. Test keyboard navigation to checkbox
4. Test screen reader compatibility
5. Verify color contrast meets WCAG standards

**Expected Result**: Checkbox is fully accessible  
**Priority**: P1  
**Test Level**: ui  
**Automation**: partially - automated a11y tools + manual testing

### TC-015: Visual Design Validation
**Title**: Checkbox matches design specifications  
**Steps**:
1. Display age verification checkbox
2. Verify checkbox styling matches design mockups
3. Test responsive behavior across screen sizes
4. Verify checkbox positioning relative to other elements

**Expected Result**: Checkbox appearance matches approved designs  
**Priority**: P2  
**Test Level**: ui  
**Automation**: no - requires visual comparison

### TC-016: Error Message Display and Styling
**Title**: Age verification error message appears correctly  
**Steps**:
1. Attempt checkout with alcohol items and unchecked checkbox
2. Verify error message appears in correct location
3. Verify error message styling (color, typography)
4. Verify error message disappears when checkbox is checked

**Expected Result**: Error message is properly displayed and dismissed  
**Priority**: P1  
**Test Level**: ui  
**Automation**: partially - message appearance can be automated, styling requires manual verification