# Design, Copy, and Launch Standards

## 1. Visual & UI Guidelines
- **No Purple Gradients:** Use clean, professional, enterprise-grade color palettes (slate, deep navy, neutral grays, subtle accent blues or emeralds).
- **No Pill-Shaped Buttons:** Use standard rectangular rounded buttons with subtle borders/corners (e.g. `border-radius: 4px` to `8px`), never fully rounded capsules/pills (`rounded-full` / 9999px).
- **No Emoji Icons:** Use standard SVG/lucide icons or FontAwesome icons, never raw unicode emojis as interface icons.
- **No Over-The-Top Scroll Animations:** Keep UI fast, snappy, and functional. No slow reveals, parallex tricks, or bouncy entrances.
- **No Cursor Animations / Custom Trails:** Keep default system cursor.
- **Add Favicon:** Ensure `<link rel="icon" ...>` with an official SVG/PNG favicon is present on all pages.

## 2. Copy & Content Standards
- **No Vague Hero Copy:** Be direct, specific, and clear about the product's actual function and value proposition.
- **No Em Dashes (`—`):** Do not use em dashes in text copy. Use standard colons, commas, hyphens, or distinct sentences.
- **No Fake Reviews or Testimonials:** Do not include fabricated quotes or mock personas acting as reviewers.
- **No Fake Metrics / Counters:** No artificial "10,000+ Happy Customers" or ticking animated counters.
- **No AI Slop Photos or AI Slop Copy:** Use clean, concrete diagrams, clean typography, real workflow visuals, and authentic technical copy.
- **Remove Any "Made with AI" Tags:** All branding must be professional and direct.

## 3. Launch Checklist & Legal Pages
- **Privacy Policy:** Dedicated, accessible route & page (`/privacy-policy`).
- **Terms and Conditions:** Dedicated, accessible route & page (`/terms-and-conditions`).
- **Custom Domain Ready:** Clean configuration without hardcoded placeholder domains.
- **High Reliability:** Zero errors or untested breakage across templates, routes, and styles.
