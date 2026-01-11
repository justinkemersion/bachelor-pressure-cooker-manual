# The Bachelor's Pressure Cooker Manual

## 🎯 Mission

A high-utility, printable cookbook designed for the everyday bachelor using a pressure cooker (Instant Pot Rio or similar). This is a **Technical Manual for Flavor** - focusing on quality, repeatability, and understanding the chemistry behind great food.

---

## 🎓 The Initiation Recipe Philosophy

**Your Master Reference:** `03_recipes/chipotle_burrito_bowl.md` is your **Initiation Recipe** - your foundational reference that you'll visit again and again.

**Why Chipotle?** It's familiar (you've had it), it's forgiving (hard to mess up), and it teaches all the fundamentals:
- Sequential cooking method
- Timing and liquid ratios
- Safety checks ("What to Worry About")
- Meal prep and reheating
- Flavor chemistry basics

**The Philosophy:**
- **For Beginners:** Master this recipe first - it teaches you everything
- **For Pros:** Come back here when you need to remember the fundamentals
- **For Everyone:** This is your reference manual - when you forget the liquid ratio, timing, or safety checks, this is where you look

**Think of it like:** Your master reference document. Even seasoned pros forget the basics - this is your "cheat sheet" to remember what's important.

---

## 🧱 The Lego Blocks Philosophy

**Every Recipe is a Building Block:**

Each recipe in this cookbook is designed as a **modular component** - like Lego blocks:
- **Learn the technique** from one recipe
- **Apply it to others** - mix and match
- **Build new combinations** - combine techniques from different recipes

**New Recipes = New Lego Pieces:**
- The Balsamic recipe introduces **Italian/Mediterranean flavor profiles**
- The Fond Method introduces **searing and reduction techniques**
- Each new recipe adds new "Lego pieces" you can use elsewhere

**The System:**
1. **Initiation Recipe** = Your reference manual (come back anytime)
2. **Other Recipes** = Modular building blocks (mix and match)
3. **New Techniques** = New Lego pieces (add to your toolkit)

**Example:** Master the sequential cooking method from Chipotle, learn the balsamic drizzle technique, combine them with the fond-building method - now you can create your own variations!

---

### Core Principles

1. **Quality Over Convenience** - Separate cooking when needed to avoid rubbery chicken, mushy rice, or weird bean consistency
2. **Flavor Chemistry** - Understand spices, acids, and umami to build balanced dishes
3. **Meal Prep Built-In** - Every recipe includes storage and reheating guidance
4. **Pantry Flexibility** - Substitution guides help adapt recipes to what's on hand
5. **Print-Ready** - Designed for lamination and spiral binding

---

## 📁 Repository Structure

**Complete directory map with file descriptions:**

```
Bachelor-Cookbook/
│
├── 01_fundamentals/                    # Core knowledge base - learn these first
│   ├── bachelor_hacks.md               # Smart shortcuts, substitutions, pantry flexibility
│   │                                   # → Bouillon cubes, rice types, frozen veg shortcuts
│   ├── spices_and_flavor.md            # Flavor chemistry: spices, acids, umami, fresh peppers
│   │                                   # → Heat levels, safety (gloves/ziplock hack), infusion methods
│   └── timing_charts.md                # Complete pressure cooker timing reference
│                                       # → Chicken cuts, rice types, beans (canned/dried/soaked)
│
├── 02_techniques/                      # Cooking methods and meal prep systems
│   ├── bulk_prep_and_freezing.md       # The $10 chicken strategy, marinade & freeze system
│   │                                   # → Individual portions, freezer bags, thawing methods
│   ├── core_techniques.md             # Core pressure cooker techniques
│   │                                   # → Sequential cooking, PIP method, liquid logic, reheating
│   └── marinades.md                    # Complete marinade recipe collection
│                                       # → Pantry Hero, Tex-Mex, Italian, Asian, Mediterranean
│
├── 03_recipes/                         # Actual recipes - your cookbook
│   ├── chipotle_burrito_bowl.md        # 🎓 INITIATION RECIPE - Master reference & cheat sheet
│   │                                   # → Most thorough, teaches all fundamentals, visit again & again
│   ├── chipotle_burrito_bowl_fond_method.md  # Alternative: searing + reduction glaze technique
│   │                                           # → Builds fond, creates drizzle, different flavor depth
│   ├── balsamic_chicken_bowl.md        # Italian/Mediterranean flavor profile
│   │                                   # → Introduces balsamic drizzle, fat balance, Cannellini beans
│   └── [future recipes]                # All other recipes (concise, build on Initiation Recipe)
│
├── 04_reference/                       # Quick lookup tables - keep these handy
│   ├── bachelors_essentials.md         # Pocket shopping list (Tier 1/2/3 priorities)
│   │                                   # → Must-have essentials, build-up items, nice-to-have upgrades
│   ├── glossary.md                     # Abbreviations (HP, NR, QR) and cooking terms
│   │                                   # → "Soaked" beans explained, pressure cooker terminology
│   ├── safety_check.md                 # Safety & chemistry logic (extracted from Initiation Recipe)
│   │                                   # → Doneness checks, what's safe vs. throw out, troubleshooting
│   └── timing_dictionary.md            # High-contrast quick reference table
│                                       # → Fast lookup for cook times, release methods, bachelor notes
│
├── 05_print/                           # Print-ready compiled versions
│   └── [generated files]               # PDF/HTML versions for lamination and spiral binding
│
├── templates/                         # Recipe templates for consistency
│   └── recipe_template.md              # Standard recipe format - use for new recipes
│                                       # → Includes "Building on Foundation" and "New Lego Block" sections
│
├── tests/                              # Pytest test suite for cookbook validation
│   ├── test_content_validation.py      # Checks recipe format, completeness, required sections
│   ├── test_references.py              # Validates all cross-references exist
│   ├── test_timing_consistency.py      # Ensures timing accuracy across all files
│   └── README.md                       # Test suite documentation
│
├── notes-for-cursor/                   # Development notes and style examples (not for print)
│   ├── balsamic_chicken_bowl-style-example.md  # Print-ready formatting example
│   └── recipe-style-check-and-more.md           # Style guidelines and development notes
│
├── venv/                               # Python virtual environment (gitignored)
│                                       # → Run `./setup.sh` to create and install dependencies
│
├── setup.sh                            # Automated setup script
│                                       # → Creates venv, installs requirements, runs tests
├── requirements-dev.txt                # Python dependencies (pytest, pytest-cov)
├── pytest.ini                          # Pytest configuration
└── README.md                           # This file - project overview and guide
```

### 📍 Quick Navigation Guide

**New to pressure cooking?** Start here:
1. `03_recipes/chipotle_burrito_bowl.md` ← **Initiation Recipe** (master this first!)
2. `01_fundamentals/spices_and_flavor.md` ← Learn flavor chemistry
3. `02_techniques/core_techniques.md` ← Understand the methods

**Need a quick lookup?**
- `04_reference/timing_dictionary.md` ← Cook times at a glance
- `04_reference/safety_check.md` ← Is it safe? Troubleshooting
- `04_reference/glossary.md` ← What does "NR" mean?

**Creating a new recipe?**
- `templates/recipe_template.md` ← Start here
- Reference `01_fundamentals/` for timing and flavor guidance

**Meal prep & shortcuts?**
- `04_reference/bachelors_essentials.md` ← Pocket shopping list (print this!)
- `01_fundamentals/bachelor_hacks.md` ← Substitutions and smart shortcuts
- `02_techniques/bulk_prep_and_freezing.md` ← The $10 chicken strategy

---

## 🧪 The Flavor Chemistry Framework

### The Three Pillars

1. **Spices** - Base flavors (garlic powder, onion powder, oregano, cumin, etc.)
2. **Acids** - Brightness (lemon, lime, vinegar) - added post-cook
3. **Umami** - Depth (Worcestershire, soy sauce, tomato paste) - added during cooking

### Critical Rules

1. **Acid/Fat Balance** - Heavy/fatty dishes MUST have acid drizzle
2. **Maillard Logic** - Always sear proteins before pressure cooking (builds fond)
3. **Rice/Protein Separation** - Use PIP method when needed to prevent texture issues
4. **Late-Stage Drizzle** - Acids and fresh herbs go on AFTER cooking
5. **Flavor Profile Consistency** - Don't mix profiles (no cumin in Italian, no balsamic in Tex-Mex)

---

## 📋 Standard Timing Constants

| Ingredient | State | Time | Release |
| :--- | :--- | :--- | :--- |
| Chicken Thighs | Thawed | 8-10m HP | 10m NR |
| Chicken Thighs | Frozen | 12-15m HP | 10m NR |
| White Basmati Rice | Rinsed | 6m HP | 10m NR (1:1 ratio) |
| Jasmine Rice | Rinsed | 4m HP | 10m NR (1:1 ratio) |

**See `01_fundamentals/timing_charts.md` for complete reference.**

---

## 🛠 Print Standards

When creating recipes, follow these markdown standards for print-readiness:

### Front/Back Page Layout (Spiral-Bound Strategy)

**Consistent Organization:** All recipes follow a front/back layout for easy navigation:

**📄 FRONT SIDE (Main Recipe - While Cooking):**
- Recipe title, profile, and method
- Quick Reference Cheat Sheet (condensed key info)
- Ingredients list (with checkboxes)
- Execution steps (Phase 1, 2, 3, etc.)
- Minimal abbreviations (HP, NR, QR)

**📄 BACK SIDE (Reference Info - After Cooking):**
- Storage & Reheating instructions
- Chemistry Notes (why it works)
- Troubleshooting / What to Worry About
- Full Abbreviations glossary
- Version History

**Page Break Marker:** Use `<!-- PAGE_BREAK -->` or a clear `---` separator to indicate where the front side ends and back side begins.

**Why This Works:**
- **While cooking:** Follow the front side - everything you need is there
- **After cooking:** Flip to the back for storage, troubleshooting, and understanding
- **Consistent:** Same layout across all recipes = muscle memory
- **Laminated:** Front side gets most use, back side stays clean for reference

### Markdown Formatting Rules

1. **Page Breaks:** Use `<!-- PAGE_BREAK -->` to mark front/back separation
2. **Typography:** 
   - `#` for Recipe Titles
   - `##` for Phases (Prep/Cook/Drizzle)
   - `###` for Chemistry Notes
3. **Checkboxes:** All ingredients use `- [ ]` for dry-erase marking on laminated pages
4. **Bold Logic:** Bold all **Timings** and **Temperatures**
5. **High Contrast:** No light grey text - everything must be readable in a steamy kitchen

---

## 📖 How to Use This Repository

### Creating a New Recipe

1. Copy `templates/recipe_template.md` to `03_recipes/[recipe_name].md`
2. Fill in the template following the flavor chemistry rules
3. Reference `01_fundamentals/` for timing and flavor guidance
4. Test and iterate (document changes in Version History)

### Debugging a Recipe

1. Check `01_fundamentals/timing_charts.md` for correct timings
2. Review `02_techniques/core_techniques.md` for proper methods
3. Verify flavor profile consistency in `01_fundamentals/spices_and_flavor.md`
4. Document fixes in recipe's Version History

### Optimizing Flavor

1. Ensure acid/fat balance (add acid if dish is heavy)
2. Verify searing was done (builds fond)
3. Check that acids were added post-cook (not during pressure)
4. Confirm flavor profile consistency (no clashing spices)

---

## 🎓 Learning Path

### For Beginners (Start Here!)

1. **🎯 Master the Initiation Recipe:** `03_recipes/chipotle_burrito_bowl.md`
   - This is your **first recipe** - most thorough, teaches you everything
   - Familiar flavor (Chipotle-style) - you know what it should taste like
   - Includes all safety checks, troubleshooting, and explanations
   - Once you master this, you've learned the fundamentals!

2. **📖 Read the Fundamentals** (while your first meal cooks):
   - `01_fundamentals/spices_and_flavor.md` - Understand the chemistry
   - `02_techniques/core_techniques.md` - Learn the methods
   - `04_reference/glossary.md` - Quick reference for terms

3. **🚀 Apply to Other Recipes:**
   - Now that you know the basics, other recipes are streamlined
   - They reference back to the Initiation Recipe for detailed explanations
   - Focus on flavor profile differences, not re-learning basics

**The Philosophy:** Learn once, apply everywhere. The Initiation Recipe is your training ground. 🎓

### For Recipe Development

1. Use `templates/recipe_template.md` as starting point
2. Reference timing charts for accuracy
3. Follow flavor chemistry rules
4. Test and document iterations

---

## 🔄 Version Control

This repository uses Git to track:
- Recipe iterations and improvements
- Timing adjustments
- Flavor profile refinements
- Print layout optimizations

**Commit messages should be clear:** "Recipe: Chipotle Bowl v1.2 - Reduced rice water by 2tbsp for firmer texture"

---

## 🧪 Test Suite

This cookbook includes a pytest-based test suite to ensure consistency and accuracy.

### Quick Setup

```bash
# Option 1: Use setup script (recommended)
./setup.sh

# Option 2: Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_timing_consistency.py
```

**Test Coverage:**
- ✅ Timing consistency across all files
- ✅ Recipe format compliance
- ✅ Cross-reference validation
- ✅ Content completeness checks

**Current Status:** All 22 tests passing ✅

See `tests/README.md` for detailed documentation.

---

## 🎯 Current Focus

**Next Steps:**
1. Populate `03_recipes/` with initial recipes (Chipotle-style bowls, etc.)
2. Create print-ready versions in `05_print/`
3. Refine timing charts based on testing
4. Build substitution database

---

## 🤖 AI Assistant Protocol

When working with AI (Cursor) on this project:

- **Bias Check:** AI should evaluate if suggested seasonings fit the flavor profile
- **Efficiency Check:** AI should suggest PIP method or layering when appropriate
- **Substitution:** AI should always provide "Bachelor Alternatives" for specialized ingredients
- **Quality Focus:** AI should prioritize texture/quality over convenience when they conflict

**The AI has permission to correct:** "Hey, you suggested Balsamic for this Cumin-heavy dish, but Red Wine Vinegar or Lime would bridge the flavors better. Want to swap?"

---

## 📝 License & Notes

This is a personal cookbook project. Recipes are tested and refined through iteration. The goal is a practical, kitchen-ready manual that balances quality with bachelor-friendly simplicity.
