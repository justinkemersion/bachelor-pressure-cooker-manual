# The Bachelor's Pressure Cooker Manual

## 🎯 Mission

A high-utility, printable cookbook designed for the everyday bachelor using a pressure cooker (Instant Pot Rio or similar). This is a **Technical Manual for Flavor** - focusing on quality, repeatability, and understanding the chemistry behind great food.

### Core Principles

1. **Quality Over Convenience** - Separate cooking when needed to avoid rubbery chicken, mushy rice, or weird bean consistency
2. **Flavor Chemistry** - Understand spices, acids, and umami to build balanced dishes
3. **Meal Prep Built-In** - Every recipe includes storage and reheating guidance
4. **Pantry Flexibility** - Substitution guides help adapt recipes to what's on hand
5. **Print-Ready** - Designed for lamination and spiral binding

---

## 📁 Repository Structure

```
Bachelor-Cookbook/
├── 01_fundamentals/          # Core knowledge base
│   ├── timing_charts.md      # Pressure cooker timing reference
│   └── spices_and_flavor.md  # Spice, acid, and umami guide
│
├── 02_techniques/            # Cooking methods
│   └── core_techniques.md     # Searing, rice prep, PIP method, etc.
│
├── 03_recipes/               # Actual recipes
│   └── [recipe files]        # Individual recipe markdown files
│
├── 04_reference/             # Quick lookup tables
│   ├── glossary.md           # Abbreviations and terms
│   └── Timing_Dictionary.md  # Cook time quick reference table
│
├── 05_print/                 # Print-ready compiled versions
│   └── [generated files]     # PDF/HTML versions for printing
│
├── templates/                # Recipe templates
│   └── recipe_template.md    # Standard recipe format
│
└── README.md                 # This file
```

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

1. **Page Breaks:** Use `---` to indicate where pages should end
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

### For Beginners

1. Read `01_fundamentals/spices_and_flavor.md` - Understand the chemistry
2. Read `02_techniques/core_techniques.md` - Learn the methods
3. Start with simple recipes in `03_recipes/`
4. Reference `04_reference/glossary.md` for terms

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
