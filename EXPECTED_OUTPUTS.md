# Expected Outputs for Demo Examples

## Formal Logic Examples

### 1. Coverage → Approve
**Input**: `((active_policy ∧ premium_paid) ∧ (valid_claim_date ∧ ¬excluded_condition)) → claim_approved`

**Expected Result**:
- Status: ✓ LOGICALLY VALID
- Verification Result: PASS
- Paradox Detected: None
- Deployment Risk: LOW — Safe to deploy

**Reason**: Valid conditional rule (implication). Not a contradiction or paradox.

---

### 2. Contradiction
**Input**: `approved ∧ ¬approved`

**Expected Result**:
- Status: ✗ INVALID / CONTRADICTION
- Verification Result: FAIL
- Paradox Detected: None
- SMT Solver: Unsatisfiable (contradiction) or Error (but detected via pattern matching)
- Deployment Risk: HIGH — Rule contains logical contradiction

**Reason**: Direct contradiction - something cannot be both true and false simultaneously.

---

### 3. Deductible Logic
**Input**: `(deductible_met ∧ service_covered) → (pay ∧ ¬copay_waived)`

**Expected Result**:
- Status: ✓ LOGICALLY VALID
- Verification Result: PASS
- Paradox Detected: None
- Deployment Risk: LOW — Safe to deploy

**Reason**: Valid conditional rule (implication). Not a contradiction or paradox.

---

### 4. Circular Dependency
**Input**: `∀p:Prop . V(p) ↔ ¬V(p)`

**Expected Result**:
- Status: ⚠️ PARADOX / CIRCULAR DEPENDENCY
- Verification Result: FAIL (paradoxes are invalid)
- Paradox Detected: YES — Self-reference
- Deployment Risk: CRITICAL — Circular dependency detected

**Reason**: Self-referential paradox (Liar Paradox). Creates impossible logical situation.

---

## Natural Language Examples

### 1. Coverage Check
**Input**: "If the patient has active coverage and the claim amount is within the annual limit, then the claim should be approved"

**Expected Result**:
- Status: ✓ LOGICALLY CONSISTENT
- Logical Consistency: PASS
- Paradox Detected: None
- Translation Confidence: 85%
- Deployment Risk: LOW — Appears consistent

**Reason**: Valid implication rule. Correctly translated and verified.

---

### 2. Contradiction
**Input**: "The claim is approved and the claim is denied"

**Expected Result**:
- Status: ✗ POTENTIAL ISSUE
- Logical Consistency: FAIL
- Paradox Detected: None
- Translation: `approved ∧ ¬approved`
- Deployment Risk: MEDIUM — Review recommended

**Reason**: Contradiction detected via pattern_type="contradiction" in API.

---

### 3. Deductible Logic
**Input**: "If the deductible is met and the service is covered, then pay the claim minus copay"

**Expected Result**:
- Status: ✓ LOGICALLY CONSISTENT
- Logical Consistency: PASS
- Paradox Detected: None
- Translation Confidence: 80%
- Deployment Risk: LOW — Appears consistent

**Reason**: Valid implication rule. Correctly translated and verified.

---

### 4. Circular Rule
**Input**: "This policy is valid if and only if this policy is not valid"

**Expected Result**:
- Status: ⚠️ PARADOX / CIRCULAR RULE
- Logical Consistency: FAIL
- Paradox Detected: YES — Liar Paradox
- Translation: `∀p:Prop . V(p) ↔ ¬V(p)`
- Deployment Risk: HIGH — Circular dependency detected

**Reason**: Self-referential paradox detected via pattern_type="liar_paradox" in API.

---

## Summary

✅ **Valid Examples** (should PASS):
- Coverage → Approve (formal)
- Deductible Logic (formal)
- Coverage Check (natural)
- Deductible Logic (natural)

❌ **Invalid Examples** (should FAIL):
- Contradiction (formal) - INVALID
- Contradiction (natural) - INVALID
- Circular Dependency (formal) - PARADOX
- Circular Rule (natural) - PARADOX
