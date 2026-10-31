# Design System Inspired by Welcome

> Auto-extracted from `https://situ-kem.telkomuniversity.ac.id/tak/home` on 2026-10-31

## 1. Visual Theme & Atmosphere

High-contrast dark mode with vivid accents — feels modern, technical, and focused.

**Key Characteristics:**
- Inter as the heading font
- Open Sans as the body font for all running text
- Dark background (#e01a3f) as the primary canvas
- Primary accent `#4680ff` used for CTAs and brand highlights
- 4 shadow level(s) detected — tinted shadows
- Rounded corners (3px+) creating a friendly, approachable feel
- Tags: dark, rounded, colorful, compact, sans-serif

## 2. Color Palette & Roles

### Primary
- **Primary Accent** (`#4680ff`) · `--color-primary`: Brand color, CTA backgrounds, link text, interactive highlights.
- **Secondary Accent** (`#00bcd4`) · `--color-secondary`: Secondary brand, hover states, complementary highlights.
- **Background** (`#e01a3f`) · `--color-bg`: Page background, primary canvas.
- **Background Secondary** (`#ecf0f5`) · `--color-bg-secondary`: Cards, surfaces, alternating sections.

### Text
- **Text Primary** (`#373a3c`) · `--color-text`: Headings and body text.
- **Text Secondary** (`#999999`) · `--color-text-secondary`: Muted text, captions, placeholders.

### Borders & Surfaces
- **Border** (`#ecf0f5`) · `--color-border`: Dividers, outlines, input borders.

### Full Extracted Palette

| # | Hex | CSS Variable | Role | Area | Contrast |
|---|---|---|---|---|---|
| 1 | `#ffffff` | `--palette-1` | block | large | text-dark |
| 2 | `#ecf0f5` | `--palette-2` | block | large | text-dark |
| 3 | `#ff5252` | `--palette-3` | button | small | text-dark |
| 4 | `#4680ff` | `--palette-4` | text-accent | small | text-light |
| 5 | `#00bcd4` | `--palette-5` | badge | small | text-dark |
| 6 | `#8153fe` | `--palette-6` | badge | small | text-light |
| 7 | `#9ccc65` | `--palette-7` | badge | small | text-dark |
| 8 | `#101b33` | `--palette-8` | badge | small | text-light |
| 9 | `#e01a3f` | `--palette-9` | text-accent | small | text-light |

## 3. Typography Rules

- **Heading Font:** `Inter`, sans-serif
- **Body Font:** `Open Sans` (web font)

### Type Hierarchy

| Role | Font | Size | Weight | Line Height | Letter Spacing |
|---|---|---|---|---|---|
| H4 | Open Sans | 24px | 600 | 28.8px | normal |
| Body | Open Sans | 13px | 400 | 19.5px | normal |
| Small | Open Sans | 13px | 600 | 19.5px | normal |

### Type Scale

| Token | Size | Suggested Usage |
|---|---|---|
| Display | `28px` | headings |
| H1 | `24px` | headings |
| H2 | `19.2px` | headings |
| H3 | `16px` | headings |
| H4 | `14px` | headings |
| Body L | `13px` | body / supporting text |
| Body | `10px` | body / supporting text |
| Small | `9px` | body / supporting text |

## 4. Component Stylings

### Primary Button

```css
.btn-primary {
  background: transparent;
  color: #535763;
  border-radius: 8px;
  padding: 7px 10px;
  font-size: 14px;
  font-weight: 400;
  border: none;
  cursor: pointer;
}
```

### Card

```css
.card {
  background: #ffffff;
  border-radius: 8px;
  padding: 0px;
  box-shadow: rgba(0, 0, 0, 0.075) 0px 2px 4px 0px;
}
```

## 5. Layout Principles

- **Base spacing unit:** `7px` — use multiples (14px, 21px, 28px, etc.)

### Spacing Scale (extracted from real elements)

| Token | Value | Role |
|---|---|---|
| spacing-1 | `7px` | element |
| spacing-2 | `25px` | card |
| spacing-3 | `10px` | element |
| spacing-4 | `15px` | element |
| spacing-5 | `24px` | card |
| spacing-6 | `18px` | element |
| spacing-7 | `20px` | element |

### Border Radius Scale

| Token | Value | Element |
|---|---|---|
| radius-subtle | `3px` | subtle |
| radius-subtle | `4px` | subtle |
| radius-button | `8px` | button |
| radius-button | `6px` | button |
| radius-card | `60px` | card |
| radius-subtle | `2px` | subtle |

## 6. Depth & Elevation

| Level | Shadow | Usage |
|---|---|---|
| Low | `rgba(0, 0, 0, 0.28) 0px 1px 2px 0px` | Cards, subtle elevation |
| Mid | `rgba(73, 83, 87, 0.3) 0px 2px 10px -1px` | Dropdowns, popovers |
| Low | `rgba(0, 0, 0, 0.075) 0px 2px 4px 0px` | Cards, subtle elevation |
| Low | `rgba(0, 0, 0, 0.24) 0px 1px 2px 0px inset` | Cards, subtle elevation |

> **Note:** This site uses chromatic (color-tinted) shadows rather than pure black — this is a deliberate brand choice that adds warmth to elevation.

## 7. Do's and Don'ts

### Do
- Use `#e01a3f` as the primary background color
- Use `Inter` for all headings and `Open Sans` for body text
- Use `#4680ff` as the single dominant accent/CTA color
- Maintain `7px` as the base spacing unit — all gaps should be multiples
- Keep the overall feel dark — use dark surfaces throughout
- Use rounded corners (`3px`+) consistently for all interactive elements
- Embrace bold color combinations — playful energy is the point
- Apply the shadow system for elevation — use the extracted shadow values

### Don't
- Don't use colors outside the extracted palette without justification
- Don't substitute Inter/Open Sans with generic alternatives
- Don't use irregular spacing — stick to 7px grid
- Don't introduce bright white surfaces — they break the dark palette
- Don't use sharp corners — they feel hostile in this rounded design language
- Don't use oversized hero text — this brand uses restrained type
- Don't use pure black (#000000) for text — use `#373a3c` instead
- Don't add decorative elements not present in the original design — no badges, ribbons, banners, or ornaments unless the source site uses them
- Don't invent UI patterns the source site doesn't have — if the original has no NEW badge, don't add one just because a red is in the palette

## 8. Responsive Behavior

| Breakpoint | Width | Notes |
|---|---|---|
| Mobile | < 640px | Single column, stack sections, reduce font sizes ~80% |
| Tablet | 640–1024px | 2-column where appropriate, maintain spacing ratios |
| Desktop | 1024–1440px | Full layout as designed |
| Wide | > 1440px | Max-width container, center content |

- Touch targets: minimum 44×44px on mobile
- Maintain 7px base unit across breakpoints — only scale multipliers

## 9. Agent Prompt Guide

### Quick Color Reference

```
Background:  #e01a3f
Text:        #373a3c
Accent:      #4680ff
Secondary:   #00bcd4
Border:      #ecf0f5
```

### Example Prompts

1. "Build a hero section with a `#e01a3f` background, `Inter` heading in `#373a3c`, and a `#4680ff` CTA button."
2. "Create a pricing card using background `#ecf0f5`, border `#ecf0f5`, `Open Sans` for text, and 21px padding."
3. "Design a navigation bar — `#e01a3f` background, `#373a3c` links, `#4680ff` for active state."
4. "Build a feature grid with 3 columns, 21px gap, each card using the card component style."
5. "Create a footer with `#ecf0f5` background, `#373a3c` text, and 14px padding."

### Iteration Guide

1. Start with layout structure (sections, grid, spacing)
2. Apply colors from the palette — background first, then text, then accents
3. Set typography — font families, sizes from the type scale, weights
4. Add components — buttons, cards, inputs using the specs above
5. Apply border-radius consistently across all elements
6. Add shadows for depth — use the extracted shadow values, not defaults
7. Check responsive behavior — test mobile and tablet layouts
8. Final pass — verify all colors match, spacing is consistent, fonts are correct

## 10. CSS Custom Properties

> 28 custom properties extracted from `:root` / `html` stylesheets.

### Color Variables

| Variable | Value |
|---|---|
| `--blue` | `#4680ff` |
| `--indigo` | `#6610f2` |
| `--purple` | `#6f42c1` |
| `--pink` | `#e83e8c` |
| `--red` | `#ff5252` |
| `--orange` | `#fd7e14` |
| `--yellow` | `#ffba57` |
| `--green` | `#28a745` |
| `--teal` | `#20c997` |
| `--cyan` | `#00acc1` |
| `--white` | `#fff` |
| `--gray` | `#6c757d` |
| `--gray-dark` | `#343a40` |
| `--primary` | `#4680ff` |
| `--secondary` | `#6c757d` |
| `--success` | `#28a745` |
| `--info` | `#00acc1` |
| `--warning` | `#ffba57` |
| `--danger` | `#ff5252` |
| `--light` | `#f8f9fa` |
| `--dark` | `#343a40` |

### Spacing Variables

| Variable | Value |
|---|---|
| `--breakpoint-xs` | `0` |
| `--breakpoint-sm` | `576px` |
| `--breakpoint-md` | `768px` |
| `--breakpoint-lg` | `992px` |
| `--breakpoint-xl` | `1200px` |

### Typography Variables

| Variable | Value |
|---|---|
| `--font-family-sans-serif` | `"Open Sans",sans-serif` |
| `--font-family-monospace` | `SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace` |
