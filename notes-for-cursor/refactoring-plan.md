# Recipe Refactoring Plan: Universalize Repeated Content

## Problem
Recipes are repeating universal content:
- Storage & Reheating sections (nearly identical across all recipes)
- Troubleshooting sections (many universal items mixed with recipe-specific)
- Safety checks (already partially extracted but still repeated)
- Universal reheating method (already in core_techniques.md but still repeated)

## Goal
Shrink recipes to 1 page (front) by extracting universal content to reference files.

---

## Proposed Structure

### New/Expanded Reference Files

#### 1. `04_reference/universal_troubleshooting.md` (NEW)
**Universal troubleshooting items:**
- Rice is crunchy? → Add 1/4 cup water, 2 mins HP, QR
- Rice is mushy? → Too much liquid. Check exact amount.
- Chicken is dry? → Skipped the rest. Always rest 5 mins.
- Frozen chicken not done? → Add 2-4 mins HP, 10m NR
- No trivet? → See bachelor_hacks.md
- Burn Error? → Don't panic! Can create Socarrat
- Chicken Shrinkage → Normal, balances with rice

**Recipe-specific items stay in recipe:**
- Glaze too thin/thick (honey garlic)
- Butter mount issues (buffalo)
- Fond building issues (fond method)

#### 2. Expand `02_techniques/meal_prep_storage.md` (EXISTING - expand it)
**Already covers:** Container strategy (glass vs. plastic, recommendations)
**Add to it:**
- Storage guidelines (cool quickly, 3-4 days, label with date)
- Universal reheating method (splash of water, 3:30 mins, level 7)
- Freezing guidelines (individual portions, ziplock bags)
- Burrito/taco conversion (universal tip)
- Reheating tips by component (rice, chicken, acids, herbs)

**Recipe-specific items stay in recipe:**
- Glaze storage tips (honey garlic)
- Tzatziki storage (Greek lemon)
- Special reheating for specific techniques

#### 3. Expand `04_reference/safety_check.md`
**Already exists but recipes still repeat:**
- Quick Diagnosis Flow
- Meat: Fully Cooked vs. Funky
- Rice: Edible vs. Weird
- Beans: Edible vs. Weird

**Action:** Recipes should just reference this, not repeat it.

---

## Recipe Structure After Refactoring

### What Stays in Recipe (Front Page)
1. **Header** (Profile, Method, Total Time)
2. **New Lego Block** section
3. **Ingredients** (with checkboxes)
4. **Execution** (Phases 1, 2, 3, 4)
5. **Recipe-Specific Chemistry Notes** (what's unique to this recipe)
6. **Recipe-Specific Substitutions** (unique to this recipe)
7. **Recipe-Specific Troubleshooting** (only unique issues)

### What Gets Referenced (Bottom of Recipe)
```
---

## 📚 Universal References

**For universal troubleshooting:** See `04_reference/universal_troubleshooting.md`
**For meal prep & storage:** See `02_techniques/meal_prep_storage.md`
**For safety checks:** See `04_reference/safety_check.md`
**For reheating method:** See `02_techniques/core_techniques.md` (Universal Microwave Reheating Method) OR `02_techniques/meal_prep_storage.md` (includes reheating)

---

## Recipe-Specific Notes

[Only recipe-unique content here - glaze scaling, special techniques, etc.]

---
```

---

## Implementation Plan

### Phase 1: Create/Expand Reference Files
1. ✅ Create `04_reference/universal_troubleshooting.md` (DONE)
2. ✅ Expand `02_techniques/meal_prep_storage.md` (DONE - added storage/reheating guidelines)
3. ✅ Verify `04_reference/safety_check.md` is complete (DONE - already exists)

### Phase 2: Update Recipes
1. Remove universal content from recipes
2. Add reference section at bottom
3. Keep only recipe-specific content
4. Test that recipes still make sense

### Phase 3: Update Template
1. Update `templates/recipe_template.md` to reflect new structure
2. Add reference section template

---

## Benefits

1. **Shorter recipes** - Focus on what's unique
2. **Easier maintenance** - Update once, applies everywhere
3. **Better organization** - Universal content in logical places
4. **Print-friendly** - Recipes fit on 1 page (front)
5. **Clearer learning** - Recipe shows what's new, references show what's universal

---

## Example: Before vs. After

### Before (Current)
- Recipe: 250+ lines
- Universal troubleshooting: 15+ items repeated
- Universal storage: 10+ lines repeated
- Safety checks: 20+ lines repeated

### After (Refactored)
- Recipe: ~150 lines (fits on 1 page)
- Universal troubleshooting: Reference link
- Universal storage: Reference link
- Safety checks: Reference link
- Recipe-specific content: Clear and focused

---

## Files to Update

### New Files
- `04_reference/universal_troubleshooting.md` ✅

### Expanded Files
- `02_techniques/meal_prep_storage.md` ✅ (added storage/reheating guidelines)

### Files to Refactor
- `03_recipes/chipotle_burrito_bowl.md` (keep as Initiation Recipe - most complete)
- `03_recipes/balsamic_chicken_bowl.md`
- `03_recipes/buffalo_chicken_wing_bowl.md`
- `03_recipes/chipotle_burrito_bowl_fond_method.md`
- `03_recipes/simple_rice_bowl.md`
- `03_recipes/honey_garlic_chicken_bowl.md`

### Files to Update
- `templates/recipe_template.md`
- `README.md` (update directory structure)

---

**Status:** Planning phase - ready for implementation
